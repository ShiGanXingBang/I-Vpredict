import numpy as np # 导入数学计算的工具
import re          # 导入处理文本（找规律）的工具
import pandas as pd # 导入处理表格数据的工具 (新增)

def parse_plt_to_tensor(file_list, output_csv_name='extracted_id_data.csv'):
    """
    函数功能：解析 .plt 文件，提取电流 (Id) 数据，进行归一化，
            并转换成神经网络需要的张量格式。最后保存归一化数据到 CSV 文件。
            
    file_list：要处理的文件名列表。
    output_csv_name：要保存的 CSV 文件名。
    """
    
    all_device_data = [] 
    
    # ------------------ (1-4 步：数据提取) ------------------
    for file_path in file_list:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"❌ 错误：找不到文件 '{file_path}'，请确保文件在当前目录下。")
            continue
            
        data_match = re.search(r'Data\s*\{([\s\S]*)\}', content)
        if not data_match:
            print(f"⚠️ 文件 '{file_path}' 中找不到 'Data' 块，跳过此文件。")
            continue
            
        raw_values = re.findall(r'[-+]?\d*\.\d+[eE][-+]?\d+', data_match.group(1))
        float_values = [float(v) for v in raw_values]
        
        num_variables = 32 
        num_points = len(float_values) // num_variables 
        
        id_curve = [] 
        for i in range(num_points):
            # Id 是第 31 个变量 (索引 30)
            try:
                 id_val = float_values[i * num_variables + 30] 
                 id_curve.append(id_val)
            except IndexError:
                 print(f"⚠️ 文件 '{file_path}' 数据点不足或格式错误。")
                 break

        if id_curve:
             all_device_data.append(id_curve) 
        else:
             print(f"❌ 文件 '{file_path}' 未能提取到有效的 Id 曲线数据。")
             
    # ------------------ (5 步：整理和归一化) ------------------
    if not all_device_data:
        print("❌ 无法创建张量：没有从文件中提取到任何有效数据。")
        return None, None
        
    data_array = np.array(all_device_data) 
    
    # 归一化处理
    data_min = data_array.min()  
    data_max = data_array.max()  
    
    # 避免除以零：如果所有电流值都相同 (即 min == max)，则归一化为全零或全一。
    if data_max == data_min:
         normalized_data = np.zeros_like(data_array)
         print("ℹ️ 警告：所有电流值相同，归一化结果为零。")
    else:
         normalized_data = (data_array - data_min) / (data_max - data_min)
    
    # ------------------ (6 步：保存 CSV 文件) ------------------
    
    # 创建表格，以便保存到 CSV
    # 每一行是一个器件的 Id 曲线，每一列是一个采样点
    column_names = [f'Point_{i+1}' for i in range(normalized_data.shape[1])]
    row_index = [f'{file.split(".")[0]}' for file in file_list if file.split(".")[0] in ['Id-Vds23n23_des', 'Id-Vds26n26_des', 'Id-Vds27n27_des']]
    
    df = pd.DataFrame(normalized_data, index=row_index, columns=column_names)
    df.to_csv(output_csv_name)
    
    print(f"🎉 归一化后的数据已成功保存到文件: {output_csv_name}")
    print("\n--- CSV 文件内容预览 ---")
    print(df.head())
    
    # ------------------ (7 步：调整张量形状) ------------------
    # 最终形状 (1, 器件数, 曲线数, 采样点数) -> (1, 3, 1, 20)
    final_tensor = normalized_data.reshape(1, normalized_data.shape[0], 1, normalized_data.shape[1])
    
    return final_tensor, df

# --- 使用程序 ---

# 设定你要处理的文件名字
# 假设您已将文件名修改为 .txt 或程序能直接读取 .plt 文件
files = ['Id-Vds23n23_des.plt', 'Id-Vds26n26_des.plt', 'Id-Vds27n27_des.plt']

# 运行函数，获取最终的神经网络输入数据，并保存 CSV
input_tensor, data_frame = parse_plt_to_tensor(files)

if input_tensor is not None:
    print("\n✅ 数据提取和保存完成！")
    print("提取后的张量形状 (就是数据矩阵的规格):", input_tensor.shape)