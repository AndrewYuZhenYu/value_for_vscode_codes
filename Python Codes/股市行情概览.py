import tkinter as tk
from tkinter import ttk
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import threading
import time
from matplotlib.animation import FuncAnimation

# 指数代码映射：使用akshare或yfinance风格，兼容东方财富和Yahoo Finance
INDICES = {
    '上证指数': {'code': '000001', 'market': '1', 'type': 'cn'},  # SSE Composite
    '道琼斯指数': {'code': '^DJI', 'type': 'us'},  # Dow Jones
    '纳斯达克指数': {'code': '^IXIC', 'type': 'us'},  # Nasdaq
    '标普500': {'code': '^GSPC', 'type': 'us'},  # S&P 500
    '日经225': {'code': '^N225', 'type': 'jp'}  # Nikkei 225
}

class StockMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("全球股市实时监控与对比")
        self.root.geometry("1200x800")
        
        self.data = {name: {'prices': [], 'times': []} for name in INDICES}
        self.current_prices = {name: {'price': 0, 'change': 0, 'change_pct': 0} for name in INDICES}
        
        self.setup_ui()
        self.update_data_loop()
    
    def fetch_chinese_index(self, code, market='1'):
        """抓取东方财富上证等A股指数实时数据[1]"""
        url = f"https://push2.eastmoney.com/api/qt/stock/get?secid={market}.{code}&fields=f43,f44,f45,f46,f47,f58,f170"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            data = resp.json()['data']
            return {
                'price': float(data['f43']),  # 当前价
                'change': float(data['f44']),  # 涨跌额
                'change_pct': float(data['f45'])  # 涨跌幅
            }
        except:
            return None
    
    def fetch_us_index(self, symbol):
        """使用yfinance抓取美股指数，但由于无API，这里模拟Yahoo Finance方式[2][8]"""
        # 注意：实际使用需 pip install yfinance
        try:
            import yfinance as yf
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="1d")
            if not hist.empty:
                current = hist['Close'][-1]
                prev = hist['Close'][-2] if len(hist) > 1 else current
                change = current - prev
                change_pct = (change / prev) * 100
                return {'price': current, 'change': change, 'change_pct': change_pct}
        except ImportError:
            pass  # 优雅降级
        except:
            pass
        return None
    
    def fetch_index_data(self, name, info):
        """统一抓取接口"""
        if info['type'] == 'cn':
            return self.fetch_chinese_index(info['code'], info['market'])
        else:
            return self.fetch_us_index(info['code'])
    
    def update_data(self):
        """更新所有指数数据"""
        for name, info in INDICES.items():
            data = self.fetch_index_data(name, info)
            if data:
                self.current_prices[name] = data
                now = datetime.now()
                self.data[name]['prices'].append(data['price'])
                self.data[name]['times'].append(now)
                # 保留最近100个点
                if len(self.data[name]['prices']) > 100:
                    self.data[name]['prices'].pop(0)
                    self.data[name]['times'].pop(0)
        self.update_display()
    
    def setup_ui(self):
        # 实时价格表格
        frame1 = ttk.Frame(self.root)
        frame1.pack(fill='x', padx=10, pady=5)
        
        cols = ('指数', '当前价', '涨跌额', '涨跌幅(%)', '状态')
        self.tree = ttk.Treeview(frame1, columns=cols, show='headings', height=8)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(fill='x')
        
        # 状态颜色
        self.tree.tag_configure('up', background='lightgreen')
        self.tree.tag_configure('down', background='lightcoral')
        
        # 图表区域
        frame2 = ttk.Frame(self.root)
        frame2.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, frame2)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # 分析文本
        self.analysis_text = tk.Text(self.root, height=6, wrap='word')
        self.analysis_text.pack(fill='x', padx=10, pady=5)
    
    def update_display(self):
        # 更新表格
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for name, data in self.current_prices.items():
            change_pct = data['change_pct']
            tag = 'up' if change_pct > 0 else 'down'
            status = '📈上涨' if change_pct > 0 else '📉下跌'
            self.tree.insert('', 'end', values=(
                name, f"{data['price']:.2f}",
                f"{data['change']:.2f}", f"{change_pct:.2f}%", status
            ), tags=(tag,))
        
        # 更新图表
        self.ax.clear()
        for name in INDICES:
            if len(self.data[name]['prices']) > 1:
                times = mdates.date2num(self.data[name]['times'])
                self.ax.plot(times, self.data[name]['prices'], label=name, linewidth=2)
        
        self.ax.legend()
        self.ax.set_title('全球主要指数实时对比 (最近100次更新)', fontsize=14)
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        self.ax.tick_params(axis='x', rotation=45)
        self.fig.tight_layout()
        self.canvas.draw()
        
        # 行情分析
        self.generate_analysis()
    
    def generate_analysis(self):
        """生成行情分析报告"""
        text = "📊 最新全球股市行情分析 (更新时间: " + datetime.now().strftime('%H:%M:%S') + "):\n\n"
        
        risers = []
        fallers = []
        for name, data in self.current_prices.items():
            if data['change_pct'] > 0:
                risers.append((name, data['change_pct']))
            else:
                fallers.append((name, data['change_pct']))
        
        if risers:
            text += "🚀 **上涨指数**:\n"
            for name, pct in sorted(risers, key=lambda x: x[1], reverse=True):
                text += f"  {name}: +{pct:.2f}%\n"
        
        if fallers:
            text += "\n📉 **下跌指数**:\n"
            for name, pct in sorted(fallers, key=lambda x: x[1]):
                text += f"  {name}: {pct:.2f}%\n"
        
        # 整体趋势判断
        changes = [data['change_pct'] for data in self.current_prices.values()]
        avg_change = sum(changes) / len(changes)
        if avg_change > 0:
            text += f"\n🌍 **整体市场**: 看涨 (平均涨幅: +{avg_change:.2f}%)"
        else:
            text += f"\n🌍 **整体市场**: 看跌 (平均跌幅: {avg_change:.2f}%)"
        
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(1.0, text)
    
    def update_data_loop(self):
        """后台数据更新线程"""
        def loop():
            while True:
                self.update_data()
                time.sleep(30)  # 每30秒更新一次，避免频繁请求
        
        thread = threading.Thread(target=loop, daemon=True)
        thread.start()

def main():
    root = tk.Tk()
    app = StockMonitor(root)
    root.mainloop()

if __name__ == "__main__":
    main()