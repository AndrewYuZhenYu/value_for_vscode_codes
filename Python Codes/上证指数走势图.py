import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class ShanghaiIndexVisualizer:
    def __init__(self):
        self.data = None
        self.last_update = None
        
    def try_yfinance(self, days=30):
        """尝试使用yfinance获取数据"""
        try:
            import yfinance as yf
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            data = yf.download("000001.SS", start=start_date, end=end_date)
            return self._clean_data(data) if not data.empty else None
        except:
            return None
    
    def try_akshare(self, days=30):
        """尝试使用akshare获取数据"""
        try:
            import akshare as ak
            # 获取上证指数日线数据
            stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol="sh000001")
            
            if stock_zh_index_daily_df.empty:
                return None
            
            # 获取最近N天的数据
            recent_data = stock_zh_index_daily_df.tail(days * 2).copy()  # 多取一些，以防有缺失
            
            # 转换索引为日期格式
            if recent_data.index.name == 'date':
                recent_data.index = pd.to_datetime(recent_data.index)
            else:
                # 尝试找日期列
                for col in recent_data.columns:
                    if 'date' in col.lower() or '日期' in col:
                        recent_data.index = pd.to_datetime(recent_data[col])
                        break
            
            recent_data = recent_data.sort_index()
            
            # 尝试识别数据列
            result_data = pd.DataFrame(index=recent_data.index)
            
            # 识别开盘价列
            for col in recent_data.columns:
                col_str = str(col).lower()
                if 'open' in col_str or '开盘' in col_str or 'open' in str(col):
                    result_data['Open'] = pd.to_numeric(recent_data[col], errors='coerce')
                    break
            
            # 识别收盘价列
            for col in recent_data.columns:
                col_str = str(col).lower()
                if 'close' in col_str or '收盘' in col_str or 'close' in str(col):
                    result_data['Close'] = pd.to_numeric(recent_data[col], errors='coerce')
                    break
            
            # 识别最高价列
            for col in recent_data.columns:
                col_str = str(col).lower()
                if 'high' in col_str or '最高' in col_str or 'high' in str(col):
                    result_data['High'] = pd.to_numeric(recent_data[col], errors='coerce')
                    break
            
            # 识别最低价列
            for col in recent_data.columns:
                col_str = str(col).lower()
                if 'low' in col_str or '最低' in col_str or 'low' in str(col):
                    result_data['Low'] = pd.to_numeric(recent_data[col], errors='coerce')
                    break
            
            # 识别成交量列
            for col in recent_data.columns:
                col_str = str(col).lower()
                if 'volume' in col_str or '成交' in col_str or 'vol' in col_str:
                    result_data['Volume'] = pd.to_numeric(recent_data[col], errors='coerce')
                    break
            
            # 如果数据为空或缺少必要列，返回None
            if result_data.empty or 'Close' not in result_data.columns:
                return None
            
            # 获取最近的days天数据
            final_data = result_data.tail(days).copy()
            
            # 处理缺失值：用前向填充
            for col in final_data.columns:
                if final_data[col].isnull().any():
                    final_data[col] = final_data[col].ffill()
            
            return self._clean_data(final_data)
            
        except Exception as e:
            print(f"akshare错误: {e}")
            return None
    
    def _clean_data(self, data):
        """清洗数据，处理NaN值"""
        if data is None or data.empty:
            return None
        
        # 确保索引是日期类型
        if not isinstance(data.index, pd.DatetimeIndex):
            try:
                data.index = pd.to_datetime(data.index)
            except:
                # 如果无法转换，创建新的日期索引
                data.index = pd.date_range(end=datetime.now(), periods=len(data), freq='D')
        
        # 确保必要的列存在
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in required_cols:
            if col not in data.columns:
                if col == 'Volume':
                    data[col] = np.random.randint(1000000, 5000000, size=len(data))
                elif col == 'Close':
                    # 如果没有收盘价，使用随机数据
                    base = 3000
                    data[col] = base + np.random.randn(len(data)) * 50
                    # 生成其他价格数据
                    if 'Open' not in data.columns:
                        data['Open'] = data['Close'] * (1 + np.random.randn(len(data)) * 0.01)
                    if 'High' not in data.columns:
                        data['High'] = data[['Open', 'Close']].max(axis=1) * (1 + np.random.rand(len(data)) * 0.01)
                    if 'Low' not in data.columns:
                        data['Low'] = data[['Open', 'Close']].min(axis=1) * (1 - np.random.rand(len(data)) * 0.01)
                elif col in ['Open', 'High', 'Low']:
                    # 如果缺少这些列，基于收盘价生成
                    if 'Close' in data.columns:
                        if col == 'Open':
                            data[col] = data['Close'].shift(1).fillna(data['Close'] * 0.99)
                        elif col == 'High':
                            data[col] = data[['Open', 'Close']].max(axis=1) * (1 + np.random.rand(len(data)) * 0.02)
                        elif col == 'Low':
                            data[col] = data[['Open', 'Close']].min(axis=1) * (1 - np.random.rand(len(data)) * 0.02)
        
        # 处理NaN值
        for col in data.columns:
            if data[col].isnull().any():
                if col == 'Volume':
                    data[col] = data[col].fillna(np.random.randint(1000000, 5000000))
                else:
                    data[col] = data[col].ffill().bfill()
        
        # 确保没有NaN值
        data = data.dropna()
        
        # 确保数据按日期排序
        data = data.sort_index()
        
        return data[required_cols]
    
    def generate_mock_data(self, days=30):
        """生成模拟数据用于演示"""
        print("使用模拟数据生成图表...")
        
        end_date = datetime.now()
        dates = pd.date_range(end=end_date, periods=days, freq='B')  # 工作日
        
        # 生成模拟的指数数据
        np.random.seed(42)
        base_price = 3000
        returns = np.random.normal(0.0005, 0.015, days)  # 微小正期望
        
        prices = [base_price]
        for i in range(1, days):
            new_price = prices[-1] * (1 + returns[i])
            prices.append(new_price)
        
        # 生成OHLC数据
        data = pd.DataFrame(index=dates[:len(prices)])
        data['Close'] = prices
        
        # 生成其他价格
        for i in range(len(prices)):
            close = prices[i]
            if i == 0:
                open_price = close * (1 + np.random.normal(0, 0.005))
            else:
                open_price = prices[i-1]
            
            high = max(open_price, close) * (1 + abs(np.random.normal(0, 0.005)))
            low = min(open_price, close) * (1 - abs(np.random.normal(0, 0.005)))
            volume = np.random.randint(2000000, 8000000)
            
            data.loc[data.index[i], 'Open'] = open_price
            data.loc[data.index[i], 'High'] = high
            data.loc[data.index[i], 'Low'] = low
            data.loc[data.index[i], 'Volume'] = volume
        
        # 确保数据顺序正确
        data = data.sort_index()
        
        return self._clean_data(data)
    
    def get_data(self, days=30, use_mock=False):
        """获取上证指数数据"""
        if use_mock:
            self.data = self.generate_mock_data(days)
            self.last_update = datetime.now()
            return self.data
        
        print("正在尝试获取上证指数数据...")
        
        # 尝试akshare
        print("尝试 akshare...")
        data = self.try_akshare(days)
        
        if data is not None and not data.empty:
            print(f"✓ 成功从 akshare 获取 {len(data)} 天数据")
            self.data = data
            self.last_update = datetime.now()
            return data
        
        # 如果akshare失败，尝试yfinance
        print("akshare失败，尝试 yfinance...")
        data = self.try_yfinance(days)
        
        if data is not None and not data.empty:
            print(f"✓ 成功从 yfinance 获取 {len(data)} 天数据")
            self.data = data
            self.last_update = datetime.now()
            return data
        
        # 如果都失败，使用模拟数据
        print("所有在线数据源都失败，使用模拟数据...")
        self.data = self.generate_mock_data(days)
        self.last_update = datetime.now()
        return self.data
    
    def create_visualization(self, figsize=(14, 10)):
        """创建可视化图表"""
        if self.data is None or self.data.empty:
            print("没有数据可展示")
            return None
        
        # 创建图形和子图
        fig, axes = plt.subplots(3, 1, figsize=figsize, 
                                gridspec_kw={'height_ratios': [3, 1, 1]})
        
        # 提取并清理数据
        data = self.data.copy()
        data = data.dropna()
        
        if data.empty:
            print("数据为空，无法生成图表")
            return None
        
        dates = data.index
        close_prices = data['Close']
        open_prices = data['Open']
        high_prices = data['High']
        low_prices = data['Low']
        volumes = data['Volume']
        
        ax1, ax2, ax3 = axes
        
        # 计算技术指标（跳过NaN）
        ma5 = close_prices.rolling(window=5, min_periods=1).mean()
        ma10 = close_prices.rolling(window=10, min_periods=1).mean()
        daily_change = close_prices.pct_change() * 100
        daily_change = daily_change.fillna(0)
        cumulative_change = (close_prices / close_prices.iloc[0] - 1) * 100
        
        # 1. 主价格图表
        # 绘制价格线
        ax1.plot(dates, close_prices, label='收盘价', color='black', linewidth=2, alpha=0.7)
        
        # 绘制K线（简化版）
        valid_indices = []
        for i in range(len(dates)):
            # 检查数据是否有效
            if (pd.notna(close_prices.iloc[i]) and pd.notna(open_prices.iloc[i]) and 
                pd.notna(high_prices.iloc[i]) and pd.notna(low_prices.iloc[i])):
                valid_indices.append(i)
                color = 'red' if close_prices.iloc[i] >= open_prices.iloc[i] else 'green'
                ax1.plot([dates[i], dates[i]], [low_prices.iloc[i], high_prices.iloc[i]], 
                        color=color, linewidth=1, alpha=0.5)
                ax1.plot([dates[i], dates[i]], [open_prices.iloc[i], close_prices.iloc[i]], 
                        color=color, linewidth=3, alpha=0.8)
        
        # 绘制移动平均线
        ax1.plot(dates, ma5, label='5日均线', color='blue', linewidth=1.5)
        ax1.plot(dates, ma10, label='10日均线', color='orange', linewidth=1.5)
        
        # 设置主图表属性
        date_range = f"{dates[0].strftime('%Y-%m-%d')} 至 {dates[-1].strftime('%Y-%m-%d')}"
        ax1.set_title(f'上证指数走势图 ({date_range})', fontsize=16, fontweight='bold', pad=20)
        ax1.set_ylabel('指数点位', fontsize=12)
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.legend(loc='upper left')
        
        # 标注最新价格
        last_close = close_prices.iloc[-1]
        last_change = cumulative_change.iloc[-1]
        ax1.annotate(f'{last_close:.2f} ({last_change:+.2f}%)', 
                    xy=(dates[-1], last_close),
                    xytext=(-50, 10),
                    textcoords='offset points',
                    fontsize=12,
                    fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
        
        # 2. 成交量图表
        volume_colors = []
        valid_dates = []
        valid_volumes = []
        
        for i in range(len(dates)):
            if i in valid_indices and pd.notna(volumes.iloc[i]):
                volume_colors.append('red' if close_prices.iloc[i] >= open_prices.iloc[i] else 'green')
                valid_dates.append(dates[i])
                valid_volumes.append(volumes.iloc[i])
        
        if valid_volumes:
            ax2.bar(valid_dates, valid_volumes, color=volume_colors, alpha=0.7)
        ax2.set_ylabel('成交量', fontsize=12)
        ax2.grid(True, alpha=0.3, linestyle='--')
        
        # 3. 涨跌幅图表
        valid_changes = []
        change_dates = []
        change_colors = []
        
        for i in range(len(dates)):
            if pd.notna(daily_change.iloc[i]):
                valid_changes.append(daily_change.iloc[i])
                change_dates.append(dates[i])
                change_colors.append('red' if daily_change.iloc[i] >= 0 else 'green')
        
        if valid_changes:
            ax3.bar(change_dates, valid_changes, color=change_colors, alpha=0.7)
        ax3.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax3.set_ylabel('日涨跌幅(%)', fontsize=12)
        ax3.set_xlabel('日期', fontsize=12)
        ax3.grid(True, alpha=0.3, linestyle='--')
        
        # 设置所有x轴日期格式
        date_format = mdates.DateFormatter('%m-%d')
        for ax in axes:
            ax.xaxis.set_major_formatter(date_format)
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(dates)//10)))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, fontsize=9)
        
        # 添加统计信息框
        if len(valid_indices) > 0:
            stats_text = f"""
统计概览:
起始点位: {close_prices.iloc[valid_indices[0]]:.2f}
最新点位: {last_close:.2f}
累计涨跌: {last_change:.2f}%
区间最高: {high_prices.iloc[valid_indices].max():.2f}
区间最低: {low_prices.iloc[valid_indices].min():.2f}
数据天数: {len(valid_indices)}
数据更新: {self.last_update.strftime('%Y-%m-%d %H:%M')}
            """
        else:
            stats_text = "数据无效"
        
        plt.figtext(0.02, 0.02, stats_text, fontsize=9,
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
        
        plt.tight_layout()
        return fig
    
    def create_simple_chart(self, figsize=(12, 6)):
        """创建简化版趋势图"""
        if self.data is None or self.data.empty:
            print("没有数据可展示")
            return None
        
        # 清理数据
        data = self.data.copy()
        data = data.dropna()
        
        if data.empty:
            print("数据为空，无法生成图表")
            return None
        
        fig, ax = plt.subplots(figsize=figsize)
        
        dates = data.index
        close_prices = data['Close']
        
        # 计算涨跌幅
        cumulative_change = (close_prices / close_prices.iloc[0] - 1) * 100
        
        # 绘制价格曲线
        ax.plot(dates, close_prices, linewidth=2.5, color='darkblue', label='上证指数')
        
        # 填充价格区域
        ax.fill_between(dates, close_prices, close_prices.min(), 
                        alpha=0.2, color='blue')
        
        # 标记关键点（确保数据有效）
        if not close_prices.empty:
            max_val = close_prices.max()
            min_val = close_prices.min()
            
            # 找到最大值和最小值的索引（可能有多个）
            max_indices = close_prices[close_prices == max_val].index
            min_indices = close_prices[close_prices == min_val].index
            
            # 取第一个出现的
            if len(max_indices) > 0:
                max_idx = max_indices[0]
                ax.plot(max_idx, max_val, 'r^', markersize=10, label='最高点')
            
            if len(min_indices) > 0:
                min_idx = min_indices[0]
                ax.plot(min_idx, min_val, 'gv', markersize=10, label='最低点')
        
        # 设置图表属性
        ax.set_title('上证指数近一个月走势图', fontsize=16, fontweight='bold')
        ax.set_xlabel('日期', fontsize=12)
        ax.set_ylabel('指数点位', fontsize=12)
        
        # 设置日期格式
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(dates)//8)))
        plt.xticks(rotation=45)
        
        # 添加网格
        ax.grid(True, alpha=0.3, linestyle=':')
        
        # 添加标注
        if not close_prices.empty:
            last_close = close_prices.iloc[-1]
            last_change = cumulative_change.iloc[-1]
            change_color = 'red' if last_change >= 0 else 'green'
            
            ax.annotate(f'最新: {last_close:.2f}\n涨跌: {last_change:+.2f}%',
                       xy=(dates[-1], last_close),
                       xytext=(-80, 20),
                       textcoords='offset points',
                       fontsize=11,
                       fontweight='bold',
                       color=change_color,
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9))
        
        ax.legend(loc='upper left')
        plt.tight_layout()
        return fig
    
    def save_chart(self, filename=None):
        """保存图表"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'上证指数_{timestamp}.png'
        
        fig = self.create_visualization()
        if fig:
            fig.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"图表已保存: {filename}")
            plt.close(fig)
            return True
        return False
    
    def show_summary(self):
        """显示数据摘要"""
        if self.data is None:
            print("暂无数据")
            return
        
        # 清理数据
        data = self.data.copy()
        data = data.dropna()
        
        if data.empty:
            print("数据无效")
            return
        
        print("\n" + "="*60)
        print("上证指数数据摘要")
        print("="*60)
        
        print(f"数据期间: {data.index[0].date()} 至 {data.index[-1].date()}")
        print(f"数据天数: {len(data)}")
        print(f"最新收盘: {data['Close'].iloc[-1]:.2f}")
        
        if len(data) > 1:
            change_pct = (data['Close'].iloc[-1]/data['Close'].iloc[0]-1)*100
            print(f"期间涨跌: {change_pct:+.2f}%")
        else:
            print(f"期间涨跌: 数据不足")
        
        print(f"最高点位: {data['High'].max():.2f}")
        print(f"最低点位: {data['Low'].min():.2f}")
        
        if 'Volume' in data.columns:
            print(f"平均成交量: {data['Volume'].mean():,.0f}")
        
        print("="*60)

def main():
    """主程序"""
    print("上证指数可视化分析程序")
    print("-" * 40)
    
    # 创建可视化器实例
    visualizer = ShanghaiIndexVisualizer()
    
    # 获取数据（优先使用akshare，如果失败则使用模拟数据）
    try:
        data = visualizer.get_data(days=30, use_mock=False)
    except Exception as e:
        print(f"获取数据时出错: {e}")
        print("使用模拟数据...")
        data = visualizer.get_data(days=30, use_mock=True)
    
    if data is not None:
        # 显示数据摘要
        visualizer.show_summary()
        
        # 创建并显示详细图表
        print("\n正在生成详细图表...")
        try:
            fig1 = visualizer.create_visualization()
            if fig1:
                plt.show(block=False)
                print("✓ 详细图表生成成功")
        except Exception as e:
            print(f"生成详细图表时出错: {e}")
        
        # 创建并显示简化图表
        print("正在生成简化图表...")
        try:
            fig2 = visualizer.create_simple_chart()
            if fig2:
                plt.show(block=False)
                print("✓ 简化图表生成成功")
        except Exception as e:
            print(f"生成简化图表时出错: {e}")
        
        # 保存图表
        try:
            save = input("\n是否保存图表？(y/n): ").lower()
            if save == 'y':
                if visualizer.save_chart():
                    print("✓ 图表保存成功")
                else:
                    print("✗ 图表保存失败")
        except:
            pass
        
        # 保持图表显示
        print("\n显示图表中...")
        plt.show()
        
    else:
        print("无法获取数据")

if __name__ == "__main__":
    main()