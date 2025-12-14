import tensorflow as tf
from tensorflow.keras import layers, models, callbacks, optimizers
import numpy as np
import pandas as pd
import os # 用于文件操作

# --- 1. 模拟数据生成器 (不变) ---
def generate_simulated_dataset(num_samples=1000):
    # ... (数据生成逻辑不变)
    X_curves = np.random.rand(num_samples, 7, 6, 17).astype(np.float32)
    X_lg = np.random.rand(num_samples, 7).astype(np.float32)
    Y_params = np.random.rand(num_samples, 28).astype(np.float32)
    return [X_curves, X_lg], Y_params

# --- 2. 构建全球参数提取模型 (不变) ---
def build_global_parameter_extractor():
    # ... (模型构建逻辑不变)
    curve_input = layers.Input(shape=(7, 6, 17), name="Curve_Data_Input")
    flat_curves = layers.Flatten()(curve_input)
    x = layers.Dense(8000, activation='relu', name="Hidden_Layer_1")(flat_curves)
    x = layers.Dense(8000, activation='relu', name="Hidden_Layer_2")(x)
    x = layers.Dense(8000, activation='relu', name="Hidden_Layer_3")(x)
    lg_input = layers.Input(shape=(7,), name="Gate_Length_Input")
    combined = layers.Concatenate(name="Feature_Fusion")([x, lg_input])
    predictions = layers.Dense(28, activation='sigmoid', name="Parameter_Output")(combined)
    
    model = models.Model(inputs=[curve_input, lg_input], outputs=predictions)
    
    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-5),
        loss='mse',
        metrics=['mae']
    )
    return model

# --- 3. 运行训练流程并保存结果 (新增保存逻辑) ---

# 定义保存文件的路径和名称
MODEL_FILE_NAME = 'bsim_extractor_model.h5'
HISTORY_FILE_NAME = 'training_history.csv'

# 生成模拟数据
(train_X, train_lg), train_Y = generate_simulated_dataset(num_samples=2000)

# 初始化模型
model = build_global_parameter_extractor()

# 定义回调函数
callbacks_list = [
    callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, verbose=1),
    callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True, verbose=1),
    # 新增回调：每轮训练后自动保存模型，只保存最优权重
    callbacks.ModelCheckpoint(
        filepath=MODEL_FILE_NAME, 
        monitor='val_loss', 
        save_best_only=True, 
        verbose=1
    )
]

# 开始训练
history = model.fit(
    x=[train_X, train_lg], 
    y=train_Y,
    epochs=2, 
    batch_size=32,
    validation_split=0.1,
    callbacks=callbacks_list
)

# -----------------------------------------------------
# **核心结果保存步骤：**
# -----------------------------------------------------

# 1. 保存训练历史数据到 CSV 文件
# 将 history 对象转换为 pandas DataFrame 并保存
history_df = pd.DataFrame(history.history)
history_df.to_csv(HISTORY_FILE_NAME, index=False)
print(f"\n✅ 训练历史已保存到文件: {os.path.abspath(HISTORY_FILE_NAME)}")

# 2. 最终保存训练好的模型（如果未使用 ModelCheckpoint，则需要这行）
# model.save(MODEL_FILE_NAME) 

# -----------------------------------------------------
# **如何使用训练好的模型进行预测？**
# -----------------------------------------------------

# 假设您有一组新的曲线数据 (1个样本)
new_curve_data = np.random.rand(1, 7, 6, 17).astype(np.float32)
new_lg_data = np.random.rand(1, 7).astype(np.float32)

# 使用模型进行预测，结果存储在一个名为 `predicted_params` 的 NumPy 数组中
predicted_params = model.predict([new_curve_data, new_lg_data])

print("\n--- 预测结果示例 (28个归一化参数) ---")
print(predicted_params)

# 如果您之前保存了模型，需要加载模型
# from tensorflow.keras.models import load_model
# loaded_model = load_model(MODEL_FILE_NAME)
# loaded_predictions = loaded_model.predict([new_curve_data, new_lg_data])

print(f"\n程序运行完毕，训练好的模型权重存储在: {os.path.abspath(MODEL_FILE_NAME)}")

# 保存预测结果到文件
np.savetxt('predicted_bsim_parameters.txt', predicted_params, fmt='%.6f')