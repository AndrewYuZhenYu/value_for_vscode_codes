import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# ==========================================
# 0. 准备工作：设置中文字体与统一配色
# ==========================================
# 设置中文字体，防止图表中的中文显示为方块
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 定义统一的城市配色字典
city_colors = {
    '北京': '#1f77b4',  # 蓝色
    '南京': '#ff7f0e',  # 橙色
    '广州': '#2ca02c'  # 绿色
}

# ==========================================
# 1. 数据读取与预处理
# ==========================================
df_bj = pd.read_csv('Beijing_filled.csv')
df_nj = pd.read_csv('Nanjing_filled.csv')
df_gz = pd.read_csv('Guangzhou_filled.csv')

df_bj['City'] = '北京'
df_nj['City'] = '南京'
df_gz['City'] = '广州'

df_all = pd.concat([df_bj, df_nj, df_gz], ignore_index=True)
df_all['Time'] = pd.to_datetime(df_all['Time'], format='%Y%m%d%H')

# ==========================================
# 2. 关键统计量对比
# ==========================================
print("=" * 40)
print("三个城市一周温度关键统计量对比 (单位: ℃)")
print("=" * 40)
stats = df_all.groupby('City')['TMP'].describe()[['mean', 'std', 'min', '25%', '50%', '75%', 'max']]
stats = stats.round(2)
print(stats)
print("=" * 40)

# ==========================================
# 3. 数据可视化 (随时间变化曲线 & 小提琴图)
# ==========================================
fig, axes = plt.subplots(2, 1, figsize=(12, 12), gridspec_kw={'height_ratios': [2, 1.5]})

# --- 图1：随时间变化曲线对比 ---
sns.lineplot(
    data=df_all,
    x='Time',
    y='TMP',
    hue='City',
    palette=city_colors,
    ax=axes[0],
    linewidth=2
)
axes[0].set_title('北京、南京、广州一周逐小时温度变化曲线', fontsize=16)
axes[0].set_xlabel('时间', fontsize=12)
axes[0].set_ylabel('温度 (℃)', fontsize=12)
axes[0].grid(True, linestyle='--', alpha=0.6)
axes[0].legend(title='城市')

# --- 图2：小提琴图对比 ---
sns.violinplot(
    data=df_all,
    x='City',
    y='TMP',
    hue='City',
    palette=city_colors,
    ax=axes[1],
    inner='quartile',
    legend=False
)
axes[1].set_title('北京、南京、广州一周温度分布对比 (小提琴图)', fontsize=16)
axes[1].set_xlabel('城市', fontsize=12)
axes[1].set_ylabel('温度 (℃)', fontsize=12)
axes[1].grid(True, axis='y', linestyle='--', alpha=0.6)

# --- 在小提琴图中添加分位数文字标识 ---
# 获取X轴上城市的顺序
cities = df_all['City'].unique()

# 定义文字的背景框样式，使其在彩色背景上更清晰
bbox_props = dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.7)

for i, city in enumerate(cities):
    # 从之前计算好的 stats 中提取四分位数
    q1 = stats.loc[city, '25%']
    median = stats.loc[city, '50%']
    q3 = stats.loc[city, '75%']

    # 在图上添加文字 (x坐标稍微向右偏移0.08，避免挡住中间的虚线)
    axes[1].text(i + 0.08, q1, f'Q1: {q1}', va='center', ha='left', fontsize=10, bbox=bbox_props)
    axes[1].text(i + 0.08, median, f'中位数: {median}', va='center', ha='left', fontsize=10, fontweight='bold',
                 bbox=bbox_props)
    axes[1].text(i + 0.08, q3, f'Q3: {q3}', va='center', ha='left', fontsize=10, bbox=bbox_props)

plt.tight_layout()
plt.show()