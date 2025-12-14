import os
import sys

def batch_rename_plt_to_txt(directory='.'):
    """
    批量将指定目录下的所有 .plt 文件后缀名修改为 .txt
    
    Args:
        directory (str): 要操作的目录路径。'.' 表示当前脚本所在的目录。
    """
    
    # 获取指定目录下的所有文件和文件夹名称
    try:
        file_list = os.listdir(directory)
    except FileNotFoundError:
        print(f"❌ 错误：找不到指定的目录 '{directory}'。")
        return
    except Exception as e:
        print(f"❌ 错误：读取目录时发生异常: {e}")
        return

    print(f"🔍 正在检查目录 '{os.path.abspath(directory)}' 中的文件...")
    
    renamed_count = 0
    
    # 遍历文件列表
    for filename in file_list:
        
        # 1. 检查文件是否以 .plt 结尾 (忽略大小写)
        if filename.lower().endswith('.plt'):
            
            # 2. 构造新的文件名
            # os.path.splitext(filename)[0] 会获取文件名（不包含旧后缀）
            base_name = os.path.splitext(filename)[0]
            new_filename = base_name + '.txt'
            
            # 3. 构造完整路径 (确保操作正确)
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)
            
            # 4. 执行重命名操作
            try:
                os.rename(old_path, new_path)
                print(f"✅ 成功重命名：'{filename}' -> '{new_filename}'")
                renamed_count += 1
            except Exception as e:
                print(f"⚠️ 警告：重命名文件 '{filename}' 失败。原因: {e}")

    if renamed_count == 0:
        print("\nℹ️ 目录中没有找到需要重命名的 .plt 文件。")
    else:
        print(f"\n🎉 批量重命名完成。共修改了 {renamed_count} 个文件。")


# --- 运行程序 ---
# 我们使用 '.' (点) 来表示当前脚本所在的文件夹
if __name__ == "__main__":
    # 如果没有提供参数，默认操作当前目录
    if len(sys.argv) > 1:
        target_directory = 'E:\MachineLearning\data\py\I-Vpredict\Dates\Id_Vds'
    else:
        target_directory = 'E:\MachineLearning\data\py\I-Vpredict\Dates\Id_Vds'
        
    batch_rename_plt_to_txt(target_directory)