# 参数提取脚本

## 功能说明

此脚本 `extract_parameters.py` 用于从 DF-ISE 格式的 `.txt` 文件中提取指定的参数，并将数据导出为 CSV 文件。

### 提取的参数

- `substrate OuterVoltage` - 基底外电压
- `gate InnerVoltage` - 栅极内电压
- `drain InnerVoltage` - 漏极内电压
- `drain eCurrent` - 漏极电子电流

### 输出格式

- **每个 txt 文件** 生成一个 **单独的 CSV 文件**
- CSV 文件名格式：`{原文件名}_extracted.csv`
- 例如：`Id-Vds23n23_des.txt` → `Id-Vds23n23_des_extracted.csv`

### 数据特点

- 每个 CSV 文件包含该原文件中 **所有数据点** 的参数值
- 数据行数对应原 txt 文件中的数据点数
- 每行数据代表一个时间点的参数值
- `drain InnerVoltage` 和 `drain eCurrent` 是一一对应的

### 使用方法

将此脚本放在包含 `.txt` 文件的文件夹中，然后运行：

```bash
python extract_parameters.py
```

或使用指定的 Python 环境：

```bash
& E:/Users/anaconda3/envs/Machinelearning/python.exe extract_parameters.py
```

### 输出示例

脚本运行后，会在同一文件夹中生成 CSV 文件，如：
- `Id-Vds23n23_des_extracted.csv`
- `Id-Vds26n26_des_extracted.csv`
- `Id-Vds27n27_des_extracted.csv`

每个 CSV 文件的内容示例：

| substrate OuterVoltage | gate InnerVoltage | drain InnerVoltage | drain eCurrent    |
|------------------------|-------------------|--------------------|-------------------|
| -1.80000000000000E+00  | 9.00000000000000E-01 | 9.00000000000000E-02 | -9.44881916301548E-08 |
| -1.80000000000000E+00  | 9.00000000000000E-01 | 1.80000000000000E-01 | -9.72661462275190E-08 |
| ...                    | ...               | ...                | ...               |

### 注意事项

1. 脚本自动检测所有 `.txt` 文件，无需手动指定
2. 如果某个 txt 文件的参数列表长度不一致，该文件会被跳过
3. 如果找不到指定的参数，会显示警告信息并继续处理其他文件
