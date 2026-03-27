import pandas as pd
import numpy as np


def clean_temperature_data(input_file, output_file):
    # 1. 读取包含异常和缺失数据的CSV文件
    # 保持 Time 为字符串格式
    df = pd.read_csv(input_file, dtype={'Time': str, 'TMP': float})

    # 记录处理前的缺失值数量
    initial_missing_count = df['TMP'].isna().sum()

    # 2. 定义异常值条件
    # 设定合理的温度范围，例如 -80℃ 到 80℃。
    # 超出这个范围的值将被判定为异常值。
    # 注意：isna() 的数据在进行 > 或 < 比较时会返回 False，所以不会被误判
    outlier_condition = (df['TMP'] > 80) | (df['TMP'] < -80)

    # 统计识别出的异常值数量
    outlier_count = outlier_condition.sum()

    # 3. 将识别出的异常值替换为缺失值 (np.nan)
    df.loc[outlier_condition, 'TMP'] = np.nan

    # 记录处理后的缺失值总数
    final_missing_count = df['TMP'].isna().sum()

    # 4. 保存清理后的数据到新文件
    df.to_csv(output_file, index=False)

# 使用示例
if __name__ == "__main__":
    # 输入文件为脏数据文件
    input_filename = 'Guangzhou_dirty.csv'
    # 输出文件为清理后的新文件
    cleaned_filename = 'Guangzhou_cleaned.csv'

    clean_temperature_data(input_filename, cleaned_filename)