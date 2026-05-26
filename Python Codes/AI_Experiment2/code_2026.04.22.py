# ===== 修复 VS Code 终端 GBK 编码问题 =====
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
# ==========================================

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import accuracy_score, confusion_matrix

import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

from sklearn.datasets import load_diabetes

# 加载糖尿病数据集
diabetes = load_diabetes()
diabetes_df = pd.DataFrame(data=diabetes.data, columns=diabetes.feature_names)
diabetes_df['target'] = diabetes.target

print('数据集形状（样本数×特征数）：', diabetes_df.shape)
print('数据集缺失值检查：', diabetes_df.isnull().sum())

X = diabetes_df.drop('target', axis=1)
y = diabetes_df['target']

# ===== 第一张图：相关性热力图 =====
correlation_matrix = diabetes_df.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix,
            annot=True,
            cmap='coolwarm',
            fmt='.2f',
            center=0,
            vmin=-1, vmax=1)
plt.title('糖尿病数据集特征相关性热力图\n(红色=正相关，蓝色=负相关，颜色越深相关性越强)')
plt.tight_layout()
plt.savefig('heatmap.png', dpi=150, bbox_inches='tight')
print('\n>>> 热力图已弹出，查看完请关闭窗口，程序会继续运行 <<<\n')
plt.show()   # ← 阻塞，等你关掉窗口后才继续

# ===== 标准化 =====
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print('标准化前特征均值（示例）：', X.iloc[:, 0].mean())
print('标准化后特征均值（示例）：', round(X_scaled[:, 0].mean(), 2))

# ===== 数据集划分 =====
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.3, random_state=42
)
print('训练集样本数：', X_train.shape[0])
print('测试集样本数：', X_test.shape[0])

# ===== 训练模型 =====
lr = LinearRegression()
lr.fit(X_train, y_train)
print('线性回归模型训练完成！')

rf = RandomForestRegressor(random_state=42)
rf.fit(X_train, y_train)
print('随机森林回归模型训练完成！')

xgb_reg = xgb.XGBRegressor(random_state=42, objective='reg:squarederror')
xgb_reg.fit(X_train, y_train)
print('XGBoost回归模型训练完成！')


def evaluate_model(model, model_name):
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f'\n{model_name}评估结果：')
    print(f'均方误差（MSE）：{mse:.4f}（越小越好）')
    print(f'决定系数（R²）：{r2:.4f}（越接近1越好）')
    return y_pred


y_pred_lr = evaluate_model(lr, '线性回归')
y_pred_rf = evaluate_model(rf, '随机森林回归')
y_pred_xgb = evaluate_model(xgb_reg, 'XGBoost回归')

# ===== 第二张图：预测值vs真实值 =====
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.scatter(y_test, y_pred_lr, alpha=0.6, color='steelblue')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel('真实病情指标')
plt.ylabel('预测病情指标')
plt.title('线性回归 预测值vs真实值')

plt.subplot(1, 3, 2)
plt.scatter(y_test, y_pred_rf, alpha=0.6, color='green')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel('真实病情指标')
plt.ylabel('预测病情指标')
plt.title('随机森林回归 预测值vs真实值')

plt.subplot(1, 3, 3)
plt.scatter(y_test, y_pred_xgb, alpha=0.6, color='orange')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel('真实病情指标')
plt.ylabel('预测病情指标')
plt.title('XGBoost回归 预测值vs真实值')

plt.tight_layout()
plt.savefig('predictions.png', dpi=150, bbox_inches='tight')
print('\n>>> 预测对比图已弹出，查看完关闭窗口即可结束程序 <<<\n')
plt.show()








#asjfiasl;dfjwkeoiquierhuvndslfuckwocaosinima过后草的