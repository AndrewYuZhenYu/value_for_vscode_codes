"""
半圆弧形槽物理模拟 — 完整动画可视化
========================================
展示:
1. 滑块 m 从半圆槽顶端 a 下滑到底部 b 的完整过程
2. 槽 M 在光滑地面上向反方向滑动 (动量守恒)
3. **核心亮点**: 支持力 N (沿径向指向圆心) 与滑块实际速度方向成钝角
   —— 这是"槽对滑块做负功"的直接几何证明
4. 实时展示: 能量、动量、角度等物理量
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import FancyArrowPatch, Wedge, Rectangle, Circle
from matplotlib.lines import Line2D
import matplotlib as mpl
import matplotlib.font_manager as fm

# ---- 中文字体配置 ----
# 尝试找系统中可用的中文字体
def setup_chinese_font():
    candidates = ['Noto Sans CJK SC', 'Noto Sans CJK JP', 'Noto Serif CJK SC', 
                  'WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'SimHei', 'Microsoft YaHei']
    available = {f.name for f in fm.fontManager.ttflist}
    for c in candidates:
        if c in available:
            mpl.rcParams['font.sans-serif'] = [c] + mpl.rcParams['font.sans-serif']
            return c
    return None

chinese_font = setup_chinese_font()
mpl.rcParams['axes.unicode_minus'] = False

# ========== 物理参数 ==========
R = 1.0
M = 3.0
m = 1.0
g = 9.8

# ========== 运动方程 (含推导见 physics_simulation.py) ==========
def theta_dot_squared(theta):
    denom = R * (M + m * np.cos(theta)**2)
    return 2 * g * (M + m) * np.sin(theta) / denom

def dynamics(state, t):
    theta, theta_dot, X, X_dot = state
    A = m * R**2 * (M + m * np.cos(theta)**2) / (M + m)
    A_prime = -m**2 * R**2 * np.sin(2*theta) / (M + m)
    theta_ddot = (m * g * R * np.cos(theta) - 0.5 * A_prime * theta_dot**2) / A
    X_ddot = -m * R * (np.cos(theta) * theta_dot**2 + np.sin(theta) * theta_ddot) / (M + m)
    return np.array([theta_dot, theta_ddot, X_dot, X_ddot])

def rk4_step(state, t, dt, f):
    k1 = f(state, t)
    k2 = f(state + 0.5*dt*k1, t + 0.5*dt)
    k3 = f(state + 0.5*dt*k2, t + 0.5*dt)
    k4 = f(state + dt*k3, t + dt)
    return state + dt * (k1 + 2*k2 + 2*k3 + k4) / 6

# ========== 数值求解 ==========
theta0 = 0.01
theta_dot0 = np.sqrt(theta_dot_squared(theta0))
state = np.array([theta0, theta_dot0, 0.0, -m*R*np.sin(theta0)*theta_dot0/(M+m)])

dt = 0.0005
t_max = 3.0
n_steps = int(t_max / dt)

times, thetas, Xs, theta_dots, X_dots = [], [], [], [], []
t = 0.0
for i in range(n_steps):
    times.append(t); thetas.append(state[0]); theta_dots.append(state[1])
    Xs.append(state[2]); X_dots.append(state[3])
    if state[0] > np.pi - 0.01:
        break
    state = rk4_step(state, t, dt, dynamics)
    t += dt

times = np.array(times)
thetas = np.array(thetas)
Xs = np.array(Xs)
theta_dots = np.array(theta_dots)
X_dots = np.array(X_dots)

# 派生量
x_m = Xs - R * np.cos(thetas)
y_m = R - R * np.sin(thetas)
vx_m = X_dots + R * np.sin(thetas) * theta_dots
vy_m = -R * np.cos(thetas) * theta_dots
v_mag = np.sqrt(vx_m**2 + vy_m**2)

# 支持力单位方向 (从滑块指向圆心)
Nx = np.cos(thetas)
Ny = np.sin(thetas)

# 速度单位方向
vsafe = np.where(v_mag > 1e-9, v_mag, 1.0)
vx_hat = vx_m / vsafe
vy_hat = vy_m / vsafe

# N 与 v 的夹角
cos_ang = Nx*vx_hat + Ny*vy_hat
angles = np.degrees(np.arccos(np.clip(cos_ang, -1, 1)))

# 能量 (验证守恒)
KE_M = 0.5 * M * X_dots**2
KE_m = 0.5 * m * (vx_m**2 + vy_m**2)
PE = m * g * y_m
E_total = KE_M + KE_m + PE

# 动量 (验证守恒)
P_x = M * X_dots + m * vx_m

# 功
W_N_on_m = cos_ang  # 每瞬时 N·v 的符号 (对时间做积分可得总功)

# ========== 选择动画帧 ==========
# 均匀抽取约 200 帧 (保证流畅)
n_frames = 120
idx = np.linspace(0, len(times)-1, n_frames).astype(int)

# ========== 创建图形 ==========
fig = plt.figure(figsize=(16, 9), facecolor='#0f1419')

# 布局: 左大图 + 右侧三个小图
gs = fig.add_gridspec(3, 3, width_ratios=[2.0, 2.0, 1.4],
                      height_ratios=[1, 1, 1],
                      left=0.05, right=0.97, top=0.93, bottom=0.07,
                      hspace=0.45, wspace=0.25)

ax_main = fig.add_subplot(gs[:, 0:2])    # 主动画
ax_angle = fig.add_subplot(gs[0, 2])     # N-v 夹角随时间
ax_energy = fig.add_subplot(gs[1, 2])    # 能量
ax_work = fig.add_subplot(gs[2, 2])      # N·v 符号

# 主动画区
ax_main.set_xlim(-2.2, 2.2)
ax_main.set_ylim(-0.4, 1.9)
ax_main.set_aspect('equal')
ax_main.set_facecolor('#0f1419')
ax_main.tick_params(colors='#8892a0', labelsize=9)
for spine in ax_main.spines.values():
    spine.set_color('#2a3441')

# 地面
ground_y = 0.0
ax_main.axhline(y=ground_y, color='#3d4a5c', lw=2, zorder=1)
# 地面剖面线
for gx in np.linspace(-2.2, 2.2, 40):
    ax_main.plot([gx, gx-0.08], [ground_y, ground_y-0.08], 
                 color='#3d4a5c', lw=1, zorder=1)

# 标题
ax_main.text(0, 1.78, 'Semi-circular Trough on Frictionless Surface', 
             ha='center', fontsize=13, color='#e8eef5', weight='bold')
ax_main.text(0, 1.65, u'半圆弧槽在光滑水平面上 — 滑块下滑过程', 
             ha='center', fontsize=11, color='#a8b4c4')

# --- 右侧小图样式 ---
def style_subplot(ax, title_en, title_cn):
    ax.set_facecolor('#0f1419')
    ax.tick_params(colors='#8892a0', labelsize=8)
    for spine in ax.spines.values():
        spine.set_color('#2a3441')
    ax.set_title(f'{title_en}\n{title_cn}', color='#e8eef5', fontsize=9, pad=6)
    ax.grid(True, alpha=0.15, color='#3d4a5c')

style_subplot(ax_angle, 'Angle between N and v', u'支持力 N 与速度 v 的夹角')
ax_angle.set_xlabel('t (s)', color='#8892a0', fontsize=8)
ax_angle.set_ylabel(u'角度 (°)', color='#8892a0', fontsize=8)
ax_angle.axhline(y=90, color='#f59e0b', ls='--', lw=1, alpha=0.6)
ax_angle.text(times[-1]*0.98, 91, '90°', color='#f59e0b', fontsize=8, ha='right')

style_subplot(ax_energy, 'Energy Conservation', u'能量守恒验证')
ax_energy.set_xlabel('t (s)', color='#8892a0', fontsize=8)
ax_energy.set_ylabel('E (J)', color='#8892a0', fontsize=8)

style_subplot(ax_work, u'Power: N·v (sign of work rate)', u'支持力瞬时功率的符号')
ax_work.set_xlabel('t (s)', color='#8892a0', fontsize=8)
ax_work.set_ylabel(u'N̂·v̂', color='#8892a0', fontsize=8)
ax_work.axhline(y=0, color='#f59e0b', ls='--', lw=1, alpha=0.6)

# ========== 生成槽的形状 ==========
def make_trough_patch(X_center):
    """生成半圆形槽(下半圆挖空)的轮廓点"""
    # 外轮廓: 一个方盒子, 内部挖掉一个半圆
    # 我们画两部分: 外框线 + 内弧线
    # 槽的几何: 圆心在 (X_center, R), 半径 R
    # 实体部分: y ∈ [0, R+0.1], x ∈ [X_center-R-0.15, X_center+R+0.15]
    #           挖掉半圆: (x-X_center)^2 + (y-R)^2 = R^2, y <= R
    pass  # 我们直接在 update 函数中画

# ========== 绘图元素 (初始化) ==========

# 槽: 用 fill_between 画出 "外框 - 内半圆" 的实心区域
trough_fill = ax_main.fill([], [], color='#4a5d7a', alpha=0.85, zorder=3, 
                           edgecolor='#6b8cae', lw=1.5)[0]

# 槽的圆心标记 (半透明点)
center_marker, = ax_main.plot([], [], 'o', color='#6b8cae', markersize=4, 
                               alpha=0.6, zorder=4)
# 从圆心到滑块的虚线 (显示径向 = N 方向)
radial_line, = ax_main.plot([], [], '--', color='#6b8cae', lw=0.8, alpha=0.5, zorder=4)

# 滑块 m
block_size = 0.12
block = Rectangle((0, 0), block_size, block_size, 
                  facecolor='#f59e0b', edgecolor='#fbbf24', lw=1.5, zorder=10)
ax_main.add_patch(block)

# 标签 M 和 m
label_M = ax_main.text(0, 0.05, 'M', fontsize=14, color='#e8eef5', 
                        weight='bold', ha='center', zorder=5)
label_m = ax_main.text(0, 0, 'm', fontsize=10, color='#0f1419', 
                        weight='bold', ha='center', va='center', zorder=11)

# a 点和 b 点标记
label_a = ax_main.text(0, 0, 'a', fontsize=11, color='#ef4444', 
                        weight='bold', ha='right', va='bottom', zorder=6)
label_b = ax_main.text(0, 0, 'b', fontsize=11, color='#10b981', 
                        weight='bold', ha='center', va='top', zorder=6)

# 支持力 N 箭头 (从滑块指向圆心方向, 即径向向上/向内)
N_arrow = FancyArrowPatch((0, 0), (0, 0), arrowstyle='-|>', 
                           mutation_scale=20, color='#60a5fa', lw=2.5, zorder=15)
ax_main.add_patch(N_arrow)
N_label = ax_main.text(0, 0, 'N', fontsize=13, color='#60a5fa', 
                        weight='bold', zorder=16)

# 速度 v 箭头 (滑块实际速度方向)
v_arrow = FancyArrowPatch((0, 0), (0, 0), arrowstyle='-|>', 
                          mutation_scale=20, color='#f43f5e', lw=2.5, zorder=15)
ax_main.add_patch(v_arrow)
v_label = ax_main.text(0, 0, 'v', fontsize=13, color='#f43f5e', 
                        weight='bold', zorder=16)

# 夹角扇形 (高亮显示钝角)
angle_wedge = Wedge((0, 0), 0.15, 0, 0, facecolor='#fbbf24', alpha=0.3, 
                    edgecolor='#fbbf24', lw=1, zorder=14)
ax_main.add_patch(angle_wedge)

# 文字信息面板
info_box = ax_main.text(-2.1, 1.52, '', fontsize=10, color='#e8eef5',
                         va='top', ha='left',
                         bbox=dict(boxstyle='round,pad=0.5', 
                                  facecolor='#1a2332', edgecolor='#2a3441', alpha=0.9),
                         zorder=20)

# 角度和功率判定结果
verdict_box = ax_main.text(2.1, 1.52, '', fontsize=10, color='#e8eef5',
                            va='top', ha='right',
                            bbox=dict(boxstyle='round,pad=0.5',
                                     facecolor='#1a2332', edgecolor='#2a3441', alpha=0.9),
                            zorder=20)

# ========== 右侧小图的动态线 ==========
line_angle, = ax_angle.plot([], [], color='#fbbf24', lw=1.5)
angle_point, = ax_angle.plot([], [], 'o', color='#f59e0b', markersize=6)
ax_angle.set_xlim(0, times[-1])
ax_angle.set_ylim(85, max(angles.max()+2, 100))

# 能量
ax_energy.plot(times, KE_M, color='#60a5fa', lw=1, alpha=0.7, label='KE (M)')
ax_energy.plot(times, KE_m, color='#f43f5e', lw=1, alpha=0.7, label='KE (m)')
ax_energy.plot(times, PE, color='#10b981', lw=1, alpha=0.7, label='PE')
ax_energy.plot(times, E_total, color='#e8eef5', lw=1.5, label='Total')
ax_energy.legend(loc='center right', fontsize=7, facecolor='#1a2332', 
                  edgecolor='#2a3441', labelcolor='#e8eef5')
energy_line = ax_energy.axvline(x=0, color='#f59e0b', lw=1, alpha=0.7)
ax_energy.set_xlim(0, times[-1])

# N·v 符号
ax_work.fill_between(times, 0, cos_ang, where=(cos_ang < 0), 
                     color='#f43f5e', alpha=0.4, label='N does -W (钝角)')
ax_work.fill_between(times, 0, cos_ang, where=(cos_ang >= 0),
                     color='#10b981', alpha=0.4, label='N does +W (锐角)')
ax_work.plot(times, cos_ang, color='#fbbf24', lw=1.2)
work_point, = ax_work.plot([], [], 'o', color='#f59e0b', markersize=6)
ax_work.legend(loc='upper right', fontsize=7, facecolor='#1a2332',
                edgecolor='#2a3441', labelcolor='#e8eef5')
work_vline = ax_work.axvline(x=0, color='#f59e0b', lw=1, alpha=0.7)
ax_work.set_xlim(0, times[-1])
ax_work.set_ylim(cos_ang.min()-0.05, max(cos_ang.max()+0.05, 0.1))


# ========== 动画更新 ==========
def update(frame):
    i = idx[frame]
    theta = thetas[i]
    X = Xs[i]
    xm_i = x_m[i]
    ym_i = y_m[i]
    
    # --- 画槽 ---
    # 外矩形 + 内半圆挖空 的多边形
    left = X - R - 0.15
    right = X + R + 0.15
    top = R + 0.12
    # 外轮廓 (逆时针): 左下 -> 右下 -> 右上 -> 左上 -> 回到左下
    # 然后在上面挖一个下半圆 (从右上内侧走圆弧到左上内侧)
    # 为了用 fill 实现挖空, 我们构造一个多边形, 把外框和内弧连起来
    
    # 外部路径 (逆时针): 
    outer = [(left, 0), (right, 0), (right, top), (X+R, top)]
    # 从 (X+R, top) 沿下半圆弧走到 (X-R, top) (顺时针, 即内部是空的)
    arc_angles = np.linspace(0, np.pi, 60)  # 从 0 到 pi
    # 圆心 (X, R), 半径 R
    # 角度 0 对应 (X+R, R), 角度 pi 对应 (X-R, R)
    # 但我们要从 (X+R, top) 走到圆弧顶部再到 (X-R, top)
    # 实际上顶部位置 y = R, 从 (X+R, R) 开始走下半圆到 (X-R, R)
    # 为了让视觉更自然, 我们加一段从 (X+R, top) 到 (X+R, R) 的短竖线
    outer.append((X+R, R))
    arc_points = [(X + R*np.cos(a), R - R*np.sin(a)) for a in arc_angles]
    outer.extend(arc_points)
    outer.append((X-R, top))
    outer.append((left, top))
    outer.append((left, 0))
    
    xs, ys = zip(*outer)
    trough_fill.set_xy(list(zip(xs, ys)))
    
    # 圆心
    center_marker.set_data([X], [R])
    
    # 径向虚线
    radial_line.set_data([X, xm_i], [R, ym_i])
    
    # --- 滑块 ---
    block.set_xy((xm_i - block_size/2, ym_i - block_size/2))
    
    # 标签
    label_M.set_position((X, 0.08))
    label_m.set_position((xm_i, ym_i))
    label_a.set_position((X - R - 0.02, R + 0.02))
    label_b.set_position((X, -0.12))
    
    # --- 支持力 N 箭头 (从滑块指向圆心方向) ---
    N_len = 0.5
    Nx_i = np.cos(theta)
    Ny_i = np.sin(theta)
    N_end = (xm_i + N_len * Nx_i, ym_i + N_len * Ny_i)
    N_arrow.set_positions((xm_i, ym_i), N_end)
    N_label.set_position((N_end[0] + 0.05*Nx_i, N_end[1] + 0.05*Ny_i))
    
    # --- 速度 v 箭头 ---
    v_len_scale = 0.12
    v_i = v_mag[i]
    v_len = max(min(v_i * v_len_scale, 0.6), 0.15)  # 限制长度范围
    vhx = vx_hat[i]
    vhy = vy_hat[i]
    v_end = (xm_i + v_len * vhx, ym_i + v_len * vhy)
    v_arrow.set_positions((xm_i, ym_i), v_end)
    v_label.set_position((v_end[0] + 0.05*vhx, v_end[1] + 0.05*vhy - 0.02))
    
    # --- 夹角扇形 ---
    # 计算 N 和 v 的角度 (弧度, 从 x 轴逆时针)
    ang_N = np.arctan2(Ny_i, Nx_i)
    ang_v = np.arctan2(vhy, vhx)
    # Wedge 使用度数
    ang_N_deg = np.degrees(ang_N)
    ang_v_deg = np.degrees(ang_v)
    # 我们希望扇形从 v 指向 N (或反之), 取较小的弧
    # Wedge(center, r, theta1, theta2) 从 theta1 逆时针到 theta2
    # 为简单起见, 画 [min(N,v), max(N,v)] 或 [max, min+360]
    a1, a2 = min(ang_N_deg, ang_v_deg), max(ang_N_deg, ang_v_deg)
    if a2 - a1 > 180:
        a1, a2 = a2, a1 + 360
    angle_wedge.set_center((xm_i, ym_i))
    angle_wedge.set_radius(0.12)
    angle_wedge.set_theta1(a1)
    angle_wedge.set_theta2(a2)
    # 根据是否为钝角改变颜色
    if angles[i] > 90:
        angle_wedge.set_facecolor('#f43f5e')
        angle_wedge.set_edgecolor('#f43f5e')
    else:
        angle_wedge.set_facecolor('#10b981')
        angle_wedge.set_edgecolor('#10b981')
    angle_wedge.set_alpha(0.35)
    
    # --- 文字信息 ---
    phase = u"下滑阶段 (a→b)" if theta < np.pi/2 else u"上升阶段 (b→a')"
    info_text = (f"t = {times[i]:.3f} s\n"
                 f"θ = {np.degrees(theta):6.2f}°\n"
                 f"X_M = {X:+.3f} m\n"
                 f"x_m = {xm_i:+.3f} m\n"
                 f"v_m = {v_i:.3f} m/s\n"
                 f"v_M = {X_dots[i]:+.3f} m/s\n"
                 f"阶段: {phase}")
    info_box.set_text(info_text)
    
    # 判定: N 与 v 的夹角
    ang_i = angles[i]
    if ang_i > 90.5:
        v_sign = u"钝角 → N 做负功"
        v_color = '#f43f5e'
    elif ang_i < 89.5:
        v_sign = u"锐角 → N 做正功"
        v_color = '#10b981'
    else:
        v_sign = u"≈ 直角 → N 不做功"
        v_color = '#fbbf24'
    
    verdict_text = (f"∠(N, v) = {ang_i:6.2f}°\n"
                    f"N̂·v̂ = {cos_ang[i]:+.4f}\n"
                    f"{v_sign}\n"
                    f"\n"
                    f"动量: P_x = {P_x[i]:+.4f}\n"
                    f"总能: E = {E_total[i]:.4f} J")
    verdict_box.set_text(verdict_text)
    verdict_box.set_color(v_color)
    
    # --- 右侧小图 ---
    current_times = times[:i+1]
    line_angle.set_data(current_times, angles[:i+1])
    angle_point.set_data([times[i]], [angles[i]])
    
    energy_line.set_xdata([times[i], times[i]])
    
    work_vline.set_xdata([times[i], times[i]])
    work_point.set_data([times[i]], [cos_ang[i]])
    
    return (trough_fill, center_marker, radial_line, block, label_M, label_m,
            label_a, label_b, N_arrow, N_label, v_arrow, v_label, angle_wedge,
            info_box, verdict_box, line_angle, angle_point, energy_line, 
            work_vline, work_point)


# ========== 创建动画 ==========
print("正在生成动画...")
anim = animation.FuncAnimation(fig, update, frames=n_frames, 
                                interval=40, blit=False, repeat=True)

# 保存为 GIF
output_path = '/mnt/user-data/outputs/semi_circular_trough_simulation.gif'
import os
os.makedirs('/mnt/user-data/outputs', exist_ok=True)

print(f"正在保存到 {output_path} ...")
anim.save(output_path, writer='pillow', fps=20, dpi=75)
print("完成!")

# 同时保存一张关键帧静态图 (滑块在下滑途中, 钝角最明显的位置)
max_angle_idx = np.argmax(angles[:len(angles)//2])  # 下滑阶段钝角最大时
print(f"\n钝角最大的时刻: t = {times[max_angle_idx]:.3f}s, θ = {np.degrees(thetas[max_angle_idx]):.2f}°, ∠(N,v) = {angles[max_angle_idx]:.2f}°")

# 跳到该帧并保存静态图
frame_idx_for_static = np.argmin(np.abs(idx - max_angle_idx))
update(frame_idx_for_static)
static_path = '/mnt/user-data/outputs/key_frame_obtuse_angle.png'
fig.savefig(static_path, dpi=120, facecolor='#0f1419', bbox_inches='tight')
print(f"关键帧已保存到 {static_path}")

plt.close(fig)
print("\n全部完成!")