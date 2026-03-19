import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ==========================================
#        👇 用户配置区域 (在这里修改) 👇
# ==========================================

# 1. 设定三个星体的质量 (Mass)
# 建议尝试：中间大两边小 (类似太阳系)，或者三个一样大
# M_LEFT   = 1.0    # 左边星星的质量
# M_CENTER = 2.0    # 中间星星的质量
# M_RIGHT  = 1.0    # 右边星星的质量

# M_LEFT = 5.0
# M_CENTER = 0.01
# M_RIGHT = 5.0

# M_LEFT = 0.1
# M_CENTER = 100.0
# M_RIGHT = 0.2
# D_LEFT = 2.0
# D_RIGHT = 3.5
# V_SCALE = 6.0 #(需要较高的速度才能维持轨道)
M_LEFT = 1.0
M_CENTER = 1.0
M_RIGHT = 1.0
V_SCALE = 0.8 #(中等速度，容易导致不稳定)
# 2. 设定距离 (Distance)
# 以中间星星为原点(0,0)
D_LEFT   = 1.0    # 左星 距离 中间星 的距离 (必须 > 0)
D_RIGHT  = 1.0    # 右星 距离 中间星 的距离 (必须 > 0)

# 3. 设定初速度倍率 (Velocity)
# 这是一个比例系数。
# 如果设为 0，星星会直接垂直撞向中间。
# 如果设得太大，星星会直接飞出屏幕。
# 尝试在 0.5 到 1.5 之间调整。
V_SCALE  = 0.8    

# 4. 模拟设置
STEPS    = 3000   # 模拟的总步数
DT       = 0.005  # 时间流逝速度 (越小越精确，但也越慢)

# ==========================================
#        👆 配置结束 (下面是程序逻辑) 👆
# ==========================================

G = 1.0 # 引力常数

def get_initial_state():
    # 1. 定义质量数组
    masses = np.array([M_LEFT, M_CENTER, M_RIGHT])
    
    # 2. 定义位置 (都在X轴上)
    # 左星在负半轴，中星在原点，右星在正半轴
    pos = np.array([
        [-D_LEFT, 0.0],  # Left
        [0.0, 0.0],      # Center
        [D_RIGHT, 0.0]   # Right
    ])
    
    # 3. 定义初速度 (垂直于直线的切向速度，让它们转起来)
    # 简单的物理直觉：越重的且距离越远的，需要的速度可能不同
    # 这里我们给一个基础的旋转趋势：左星向下，右星向上 (逆时针旋转趋势)
    
    v_left  = np.array([0.0, -1.0]) * V_SCALE
    v_right = np.array([0.0,  1.0]) * V_SCALE
    v_center= np.array([0.0,  0.0]) # 假设中间先不动
    
    vel = np.array([v_left, v_center, v_right])
    
    # --- 关键修正：动量守恒修正 ---
    # 如果左边是重达100吨的恒星，右边是1吨的行星，系统整体会飘走。
    # 这里计算质心速度，然后让所有星体减去这个速度，保证系统视觉上保持在中心。
    total_mass = np.sum(masses)
    momentum = np.sum(vel * masses[:, np.newaxis], axis=0)
    v_com = momentum / total_mass
    vel = vel - v_com # 修正速度
    
    return masses, pos, vel

def compute_acc(positions, masses):
    n = len(masses)
    acc = np.zeros_like(positions)
    for i in range(n):
        for j in range(n):
            if i != j:
                r_vec = positions[j] - positions[i]
                r_dist = np.linalg.norm(r_vec)
                # 软化因子防止除以0
                if r_dist < 0.05: continue
                acc[i] += G * masses[j] * r_vec / (r_dist**3)
    return acc

# --- 初始化模拟 ---
masses, current_pos, current_vel = get_initial_state()
trajectory = np.zeros((STEPS, 3, 2))

# --- 开始数值积分 (Verlet积分法思路，简化版) ---
print("正在计算物理轨迹...")
for t in range(STEPS):
    trajectory[t] = current_pos
    
    # 计算加速度
    acc = compute_acc(current_pos, masses)
    
    # 更新速度和位置
    current_vel += acc * DT
    current_pos += current_vel * DT

print("计算完成，正在生成动画...")

# --- 绘图与动画 ---
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_facecolor('black')

# 自动调整视野范围：根据最远的星星距离再留点余地
max_dist = max(D_LEFT, D_RIGHT) * 2.0
ax.set_xlim(-max_dist, max_dist)
ax.set_ylim(-max_dist, max_dist)
ax.set_aspect('equal')

lines = [ax.plot([], [], '-', lw=1.5, alpha=0.7)[0] for _ in range(3)]
points = [ax.plot([], [], 'o')[0] for _ in range(3)]

# 根据质量设置点的大小 (质量越大，点越大)
min_size, max_size = 5, 20
norm_mass = (masses - masses.min()) / (masses.max() - masses.min() + 1e-10) # 归一化
point_sizes = min_size + norm_mass * (max_size - min_size)

colors = ['#FF4444', '#FFFF44', '#4444FF'] # 左红，中黄，右蓝

for i in range(3):
    points[i].set_color(colors[i])
    points[i].set_markersize(point_sizes[i])
    lines[i].set_color(colors[i])

def init():
    for line, point in zip(lines, points):
        line.set_data([], [])
        point.set_data([], [])
    return lines + points

def update(frame):
    # 这里的 speedup 决定了动画播放快慢，跳过几帧画一次
    speedup = 4 
    idx = frame * speedup
    if idx >= STEPS: return lines + points
    
    for i in range(3):
        # 画星球
        points[i].set_data([trajectory[idx, i, 0]], [trajectory[idx, i, 1]])
        
        # 画轨迹 (最近150个点)
        tail = 150
        start = max(0, idx - tail)
        lines[i].set_data(trajectory[start:idx, i, 0], trajectory[start:idx, i, 1])
        
    return lines + points

ani = FuncAnimation(fig, update, frames=STEPS//4, init_func=init, blit=True, interval=20)

plt.title(f"M={masses}, Dist=[{D_LEFT}, {D_RIGHT}]")
plt.grid(False)
plt.show()