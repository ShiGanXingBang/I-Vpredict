import numpy as np
import re
import pandas as pd
import os
from pathlib import Path

def extract_all_parameters_from_txt(file_path):
    """
    从 txt 文件中提取指定的参数值（所有数据点）
    
    参数：
    file_path：txt 文件的路径
    
    返回：
    dict：包含提取参数的字典，每个参数对应一个列表
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 错误：无法读取文件 '{file_path}'：{e}")
        return None
    
    # 提取 Info 块中的数据集名称
    info_match = re.search(r'Info\s*\{([\s\S]*?)\}', content)
    if not info_match:
        print(f"⚠️ 文件 '{file_path}' 中找不到 'Info' 块。")
        return None
    
    info_content = info_match.group(1)
    
    # 提取 datasets 列表中的所有数据集名称
    datasets_match = re.search(r'datasets\s*=\s*\[([\s\S]*?)\]', info_content)
    if not datasets_match:
        print(f"⚠️ 文件 '{file_path}' 中找不到 'datasets' 列表。")
        return None
    
    datasets_str = datasets_match.group(1)
    # 提取所有被引号包围的数据集名称
    dataset_names = re.findall(r'"([^"]+)"', datasets_str)
    
    # 确定要提取的参数的索引
    target_params = [
        "substrate OuterVoltage",
        "gate InnerVoltage",
        "drain InnerVoltage",
        "drain eCurrent"
    ]
    
    param_indices = {}
    for param in target_params:
        if param in dataset_names:
            param_indices[param] = dataset_names.index(param)
        else:
            print(f"⚠️ 参数 '{param}' 未在文件 '{file_path}' 中找到。")
    
    if not param_indices:
        print(f"❌ 文件 '{file_path}' 中没有找到任何指定的参数。")
        return None
    
    # 提取 Data 块中的数据
    data_match = re.search(r'Data\s*\{([\s\S]*?)\}', content)
    if not data_match:
        print(f"⚠️ 文件 '{file_path}' 中找不到 'Data' 块。")
        return None
    
    # 提取所有科学计数法数值
    raw_values = re.findall(r'[-+]?\d*\.\d+[eE][-+]?\d+', data_match.group(1))
    float_values = [float(v) for v in raw_values]
    
    # 计算数据点数量（根据数据集数量）
    num_variables = len(dataset_names)
    num_points = len(float_values) // num_variables
    
    if num_points == 0:
        print(f"❌ 文件 '{file_path}' 中没有数据点。")
        return None
    
    # 提取指定参数的所有值
    param_values = {}
    for param, idx in param_indices.items():
        values = []
        for i in range(num_points):
            try:
                val = float_values[i * num_variables + idx]
                values.append(val)
            except IndexError:
                print(f"⚠️ 数据索引越界：file={file_path}, param={param}, i={i}")
                break
        
        param_values[param] = values
    
    return param_values

def process_all_txt_files(folder_path):
    """
    处理文件夹内所有的 txt 文件，为每个文件生成一个 CSV
    
    参数：
    folder_path：txt 文件所在的文件夹路径
    """
    # 获取所有 txt 文件
    txt_files = list(Path(folder_path).glob('*.txt'))
    
    if not txt_files:
        print(f"❌ 在文件夹 '{folder_path}' 中找不到任何 .txt 文件。")
        return
    
    print(f"ℹ️ 找到 {len(txt_files)} 个 .txt 文件\n")
    
    successful_count = 0
    
    for file_path in txt_files:
        print(f"📄 正在处理: {file_path.name}")
        
        params = extract_all_parameters_from_txt(str(file_path))
        
        if params:
            # 检查所有参数列表长度是否相同
            list_lengths = [len(v) for v in params.values()]
            if len(set(list_lengths)) > 1:
                print(f"⚠️ 文件 '{file_path.name}' 中参数列表长度不一致")
                continue
            
            # 创建 DataFrame
            df = pd.DataFrame(params)
            
            # 获取 Csv 输出文件夹路径（与 Txt 文件夹同级）
            parent_folder = os.path.dirname(folder_path)
            csv_folder = os.path.join(parent_folder, 'Csv')
            os.makedirs(csv_folder, exist_ok=True)
            
            # 生成输出文件名（去掉 .txt 后缀，加上 _extracted.csv）
            output_filename = f"{file_path.stem}_extracted.csv"
            output_path = os.path.join(csv_folder, output_filename)
            
            # 保存为 CSV
            df.to_csv(output_path, index=False, encoding='utf-8')
            
            print(f"✅ 成功保存到: {output_filename}")
            print(f"   数据行数: {len(df)}")
            print(f"   参数列数: {len(df.columns)}\n")
            
            successful_count += 1
        else:
            print(f"⚠️ 无法从 '{file_path.name}' 提取参数\n")
    
    print(f"\n🎉 处理完成！")
    print(f"成功处理: {successful_count}/{len(txt_files)} 个文件")

# --- 主程序 ---
if __name__ == "__main__":
    # 获取脚本所在的文件夹（Id_Vds）
    script_folder = os.path.dirname(os.path.abspath(__file__))
    
    # 设置输入文件夹为 Txt 子文件夹
    txt_folder = os.path.join(script_folder, 'Txt')
    
    print(f"📂 输入文件夹: {txt_folder}\n")
    print("=" * 60)
    
    # 处理所有 txt 文件
    process_all_txt_files(txt_folder)
