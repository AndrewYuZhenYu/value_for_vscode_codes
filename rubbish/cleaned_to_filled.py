import pandas as pd


def fill_missing_temperatures(input_file, output_file):
    # 1. 读取CSV文件
    df = pd.read_csv(input_file)

    # 2. 将 Time 列转换为 datetime 格式，方便按时间顺序处理
    # 格式 '%Y%m%d%H' 对应例如 '2023102514' (2023年10月25日14时)
    df['Time'] = pd.to_datetime(df['Time'].astype(str), format='%Y%m%d%H')

    # 3. 按时间进行排序，确保数据是按时间先后顺序排列的
    df = df.sort_values('Time').reset_index(drop=True)

    # 4. 使用线性插值填充 TMP 列的缺失值
    # method='linear' 表示线性插值
    # limit_direction='both' 表示如果数据的开头或结尾有缺失值，也会向后或向前进行平推填充
    df['TMP'] = df['TMP'].interpolate(method='linear', limit_direction='both')

    # 5. 将 Time 列转换回原来的文本格式 (YYYYMMDDHH)
    df['Time'] = df['Time'].dt.strftime('%Y%m%d%H')

    # 6. 保存为新的CSV文件，不保存行索引
    df.to_csv(output_file, index=False)


# 使用示例
if __name__ == "__main__":
    # 替换为你的实际文件名
    input_csv_path = 'Guangzhou_cleaned.csv'
    output_csv_path = 'Guangzhou_filled.csv'

    fill_missing_temperatures(input_csv_path, output_csv_path)