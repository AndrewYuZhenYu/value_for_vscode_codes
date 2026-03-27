
import pandas as pd
import numpy as np
def clean_temperature_data(input_file, output_file):
 # 1. 读取 CSV 文件，指定 Time 为字符串、TMP 为浮点型
 df = pd.read_csv(input_file, dtype={'Time': str, 'TMP': 
float})
 # 2. 统计处理前缺失值数量
 initial_missing_count = df['TMP'].isna().sum()
 print(f"处理前缺失值数量：{initial_missing_count}")
# //处理前缺失值数量：8（北京）
 # 3. 定义异常值条件：温度超出[-80, 80]℃判定为异常
 outlier_condition = (df['TMP'] > 80) | (df['TMP'] < -80)
 outlier_count = outlier_condition.sum()
 print(f"识别出的异常值数量：{outlier_count}")
# //识别出的异常值数量：8（北京）
 # 4. 将异常值替换为缺失值
 df.loc[outlier_condition, 'TMP'] = np.nan
# //最后输出可查看
 # 5. 统计处理后缺失值总数
 final_missing_count = df['TMP'].isna().sum()
 print(f"处理后缺失值总数：{final_missing_count}")
# //处理后缺失值总数：16（北京）
 # 6. 保存清理后的数据
 df.to_csv(output_file, index=False)
 print(f"清理后的数据已保存至：{output_file}")
# 主程序执行
if __name__ == "__main__":
 # 北京数据清洗（南京/广州只需修改这两个文件名）
 input_filename = 'Beijing_dirty.csv'
 cleaned_filename = 'Beijing_cleaned.csv'
 clean_temperature_data(input_filename, cleaned_filename)