import numpy as np # 导入数学计算的工具
import re          # 导入处理文本（找规律）的工具
import pandas as pd # 导入处理表格数据的工具
import os          # 导入文件操作工具
from pathlib import Path # 导入路径处理工具

def convert_plt_to_txt(plt_folder, output_folder='Txt'):
    """
    函数功能：将文件夹中所有的 .plt 文件转换为 .txt 文件
            
    plt_folder：包含 .plt 文件的文件夹路径
    output_folder：输出文件夹名称
    """
    
    # 创建输出文件夹
    output_path = os.path.join(plt_folder, output_folder)
    os.makedirs(output_path, exist_ok=True)
    
    print(f"📂 输入文件夹: {plt_folder}")
    print(f"📂 输出文件夹: {output_path}\n")
    
    # 获取所有 .plt 文件
    plt_files = list(Path(plt_folder).glob('*.plt'))
    
    if not plt_files:
        print(f"❌ 在文件夹 '{plt_folder}' 中找不到任何 .plt 文件。")
        return
    
    print(f"ℹ️ 找到 {len(plt_files)} 个 .plt 文件\n")
    
    successful_count = 0
    
    for plt_file in plt_files:
        try:
            # 读取 .plt 文件
            with open(plt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 生成输出文件名（替换后缀为 .txt）
            output_filename = f"{plt_file.stem}.txt"
            output_file_path = os.path.join(output_path, output_filename)
            
            # 保存为 .txt 文件
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 已转换: {plt_file.name} → {output_filename}")
            successful_count += 1
            
        except Exception as e:
            print(f"❌ 转换失败: {plt_file.name} - {e}")
    
    print(f"\n🎉 转换完成！")
    print(f"成功转换: {successful_count}/{len(plt_files)} 个文件")
    print(f"📁 输出位置: {output_path}")

# --- 主程序 ---
if __name__ == "__main__":
    # 获取当前脚本所在的文件夹
    current_folder = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 60)
    print("PLT 文件转换为 TXT 文件")
    print("=" * 60 + "\n")
    
    # 执行转换
    convert_plt_to_txt(current_folder, output_folder='Txt')