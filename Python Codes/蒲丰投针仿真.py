'''
Author: AndrewYuZhenYu zhenyu_yu@outlook.com
Date: 2026-03-09 20:23:02
LastEditors: AndrewYuZhenYu zhenyu_yu@outlook.com
LastEditTime: 2026-03-09 20:28:05
FilePath: \VSCODE_NEW\Python Codes\蒲丰投针仿真.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
'''蒲丰投针实验（Buffon's Needle Experiment）是一个非常经典的蒙特卡洛（Monte Carlo）模拟实验。通过随机投掷针来估算圆周率，既直观又充满数学之美。
实验的数学原理很简单：假设地板上画有等距的平行线，间距为 t，我们随机投掷长度为 l（要求 l \le t）的针。针与直线相交的概率 P 与 \pi 的关系为：
因此，如果我们投掷 N 次，有 C 次相交，概率 P 就可以用频率 C/N 来近似，从而推导出求 \pi 的公式：
为了让你看到“针的具体位置”、“可视化”以及“\pi 值随次数增加的变化”，我为你编写了以下 Python 代码。它使用了 numpy 进行高效的数值计算，并用 matplotlib 绘制了两个图表：一个是投针的物理过程，另一个是 \pi 值的收敛曲线。
Python 模拟代码
你可以直接在安装了 numpy 和 matplotlib 的 Python 环境中运行这段代码：'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

def simulate_buffon_needle(num_needles=2000, line_spacing=2.0, needle_length=1.5, board_size=20):
    """
    模拟蒲丰投针实验
    num_needles: 投针总数
    line_spacing: 平行线间距 (t)
    needle_length: 针的长度 (l)
    board_size: 模拟区域的大小
    """
    
    # 1. 随机生成针的中心坐标 (x, y) 和 旋转角度 theta
    x_centers = np.random.uniform(0, board_size, num_needles)
    y_centers = np.random.uniform(0, board_size, num_needles)
    angles = np.random.uniform(0, np.pi, num_needles)
    
    # 2. 计算针的两个端点坐标
    dx = (needle_length / 2) * np.cos(angles)
    dy = (needle_length / 2) * np.sin(angles)
    
    x1 = x_centers - dx
    y1 = y_centers - dy
    x2 = x_centers + dx
    y2 = y_centers + dy
    
    # 3. 判断是否与平行线相交
    # 如果针的两个端点 y 坐标跨越了平行线（平行线 y = k * line_spacing），则相交
    # 用向下取整的方式判断：如果两个端点除以间距后的整数部分不同，说明跨越了整数倍的间距
    crosses = np.floor(y1 / line_spacing) != np.floor(y2 / line_spacing)
    
    # 4. 计算随着投针次数增加的 Pi 的估算值
    cum_crosses = np.cumsum(crosses)
    # 为了避免除以 0 的错误，将前面累加相交次数为 0 的部分替换为 1（仅影响极前期的计算）
    cum_crosses = np.where(cum_crosses == 0, 1, cum_crosses)
    
    n_array = np.arange(1, num_needles + 1)
    pi_estimates = (2 * needle_length * n_array) / (line_spacing * cum_crosses)
    
    # 5. 可视化
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # --- 图 1：投针物理模拟 ---
    ax1.set_title(f"Buffon's Needle Simulation (N={num_needles})")
    ax1.set_xlim(0, board_size)
    ax1.set_ylim(0, board_size)
    ax1.set_aspect('equal')
    
    # 画平行线
    for y in np.arange(0, board_size + line_spacing, line_spacing):
        ax1.axhline(y, color='gray', linestyle='--', alpha=0.5)
        
    # 准备线段数据并按是否相交分类颜色
    segments = [((x1[i], y1[i]), (x2[i], y2[i])) for i in range(num_needles)]
    colors = ['red' if c else 'blue' for c in crosses]
    
    # 使用 LineCollection 批量高效绘图
    lc = LineCollection(segments, colors=colors, linewidths=1.5, alpha=0.7)
    ax1.add_collection(lc)
    ax1.text(0.5, -0.1, "Red: Crossed lines | Blue: Did not cross", 
             ha='center', va='center', transform=ax1.transAxes, fontsize=12)
    
    # --- 图 2：Pi 值收敛过程 ---
    ax2.set_title("Estimation of Pi as Drop Count Increases")
    ax2.plot(n_array, pi_estimates, color='purple', label='Estimated Pi')
    ax2.axhline(np.pi, color='green', linestyle='-', linewidth=2, label=f'True Pi ({np.pi:.5f})')
    
    ax2.set_xlabel("Number of Needles Thrown")
    ax2.set_ylabel("Estimated Pi Value")
    # 限制 y 轴范围，让图表在初期的大幅波动后更容易看清收敛
    ax2.set_ylim(2.5, 4.0) 
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    final_pi = pi_estimates[-1]
    ax2.text(0.5, 0.05, f"Final Estimated Pi: {final_pi:.5f}", 
             ha='center', va='center', transform=ax2.transAxes, 
             fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

    plt.tight_layout()
    plt.show()

# 运行模拟
if __name__ == "__main__":
    simulate_buffon_needle(num_needles=3000000, line_spacing=2.0, needle_length=1.5, board_size=20)
'''
运行后你会看到什么？
 * 左侧图表（投针情况）：你将看到一个限定区域内的物理模拟。灰色的虚线代表地板上的平行线。红色的线代表那些跨越了平行线的针，蓝色的线代表没有碰到平行线的针。
 * 右侧图表（\pi 的收敛）：随着横轴（投针次数）增加，紫色的曲线展示了 \pi 的计算值是如何变化的。绿色的水平实线是真实的 \pi 值。你会发现，在最初的几十次投掷中，估算值可能会剧烈波动（甚至跳出图表范围），但随着样本量增加到上千次，紫色曲线会逐渐贴近绿色实线。
如果想看更密集的视觉效果或者更精确的收敛，你可以在最后一行代码中把 num_needles=2000 改成更大的数字（比如 5000 甚至 10000）。
需要我帮你解释一下代码中是如何使用向量化操作（避免低效的 for 循环）来快速判断成千上万根针是否与直线相交的吗？'''