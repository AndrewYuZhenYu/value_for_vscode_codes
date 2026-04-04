import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 设置中文字体（防止图形中的中文乱码）
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False

def analyze_bank_statement(file_path):
    # 1. 加载数据
    # 注意：根据实际导出的Excel，可能需要调整 skiprow 参数
    df = pd.read_excel(file_path)

    # 2. 数据清洗
    # 去除列名中的换行符
    df.columns = [c.replace('\n', '') for c in df.columns]
    
    # 转换金额：去除逗号并转为浮点数
    df['金额'] = df['金额'].replace(',', '', regex=True).astype(float)
    df['余额'] = df['余额'].replace(',', '', regex=True).astype(float)
    
    # 转换日期
    df['记账日期'] = pd.to_datetime(df['记账日期'])
    df['月份'] = df['记账日期'].dt.to_period('M')

    # 3. 消费分类逻辑 (可以根据你的消费习惯自行添加关键词)
    def categorize(row):
        target = str(row['对方账户名']) + str(row['附言'])
        if any(word in target for word in ['食堂', '美团', '饿了么', '餐饮', '瑞幸', '塔斯汀', '麦当劳', '蜜雪冰城']):
            return '餐饮美食'
        if any(word in target for word in ['一卡通', '地铁', '公交', '企鹅科技', '哈啰', '滴滴']):
            return '交通出行'
        if any(word in target for word in ['抖音', '网易', '游戏', '汽水音乐', 'Bilibili', 'BUFF']):
            return '休闲娱乐'
        if any(word in target for word in ['北京交通大学', '云裳物联', '电费', '校园卡']):
            return '校园生活'
        if any(word in target for word in ['京东', '淘宝', '拼多多', '超市', '便利店']):
            return '购物消费'
        if row['金额'] > 0:
            return '收入/转账'
        return '其他支出'

    df['消费类别'] = df.apply(categorize, axis=1)

    # 4. 基础统计
    total_income = df[df['金额'] > 0]['金额'].sum()
    total_expense = df[df['金额'] < 0]['金额'].sum()
    
    print(f"--- 统计简报 ---")
    print(f"总收入: {total_income:.2f} 元")
    print(f"总支出: {abs(total_expense):.2f} 元")
    print(f"净收支: {total_income + total_expense:.2f} 元")

    # 5. 可视化绘制
    fig = plt.figure(figsize=(15, 12))

    # 子图1：月度收支趋势
    ax1 = plt.subplot(2, 2, 1)
    monthly_stats = df.groupby(['月份', df['金额'] > 0])['金额'].sum().unstack().fillna(0)
    monthly_stats.columns = ['支出', '收入']
    monthly_stats['支出'] = monthly_stats['支出'].abs()
    monthly_stats.plot(kind='bar', ax=ax1, color=['#ff9999','#66b3ff'])
    plt.title('月度收支对比')
    plt.xticks(rotation=45)

    # 子图2：支出分类占比
    ax2 = plt.subplot(2, 2, 2)
    expense_df = df[df['金额'] < 0]
    category_dist = expense_df.groupby('消费类别')['金额'].sum().abs()
    category_dist.plot(kind='pie', autopct='%1.1f%%', startangle=140, cmap='Pastel1')
    plt.title('支出分类占比')
    plt.ylabel('')

    # 子图3：余额变动曲线
    ax3 = plt.subplot(2, 1, 2)
    plt.plot(df['记账日期'], df['余额'], marker='o', markersize=2, linestyle='-', color='#4CAF50')
    plt.fill_between(df['记账日期'], df['余额'], color='#4CAF50', alpha=0.1)
    plt.title('账户余额变动趋势')
    plt.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.show()

    # 6. 导出分析结果
    # 筛选出大额支出（例如大于100元）
    big_expenses = df[df['金额'] < -100].sort_values(by='金额')
    big_expenses.to_excel('中银流水2026.04.04.xlsx', index=False)
    print("大额支出分析已导出至 '中银流水2026.04.xlsx'")

# 使用方法：将下面的路径替换为你导出的 Excel 文件名
# analyze_bank_statement('你的流水文件.xlsx')