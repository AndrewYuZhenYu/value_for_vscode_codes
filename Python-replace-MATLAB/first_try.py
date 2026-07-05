import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
from mpl_toolkits.mplot3d import Axes3D

# ================= 运行前环境配置 =================
# 智能检测系统可用的中文字体（macOS / Windows / Linux）
_candidate_fonts = [
    'PingFang SC',      # macOS 现代系统字体（首选）
    'Heiti SC',         # macOS 黑体
    'STHeiti',          # macOS 华文黑体
    'Arial Unicode MS', # macOS 通用字体
    'SimHei',           # Windows 黑体
    'Microsoft YaHei',  # Windows 雅黑
    'Noto Sans CJK SC', # Linux
    'WenQuanYi Micro Hei', # Linux
]
_available = {f.name for f in font_manager.fontManager.ttflist}
_selected_font = 'sans-serif'  # fallback
for _font in _candidate_fonts:
    if _font in _available:
        _selected_font = _font
        break
print(f"✅ 使用字体: {_selected_font}")

plt.rcParams.update({
    'font.sans-serif': [_selected_font, 'DejaVu Sans', 'Arial'],
    'font.family': 'sans-serif',
    'axes.unicode_minus': True,      # 使用 ASCII 负号，兼容性最好
    'mathtext.fontset': 'stix',      # 数学公式使用 STIX 字体，与中文兼容
    'figure.dpi': 120,               # 高清输出
    'savefig.dpi': 200,
    'savefig.bbox': 'tight',
    'axes.grid.axis': 'both',
    'grid.alpha': 0.3,
})

# ================= 创建画布 =================
fig = plt.figure(figsize=(15, 7.5), facecolor='white', dpi=120)
fig.suptitle('电磁学模型对比与安培环路推导', fontsize=17,
             fontweight='bold', y=0.98)

# ================= 1. 长直螺线管子图 =================
ax1 = fig.add_subplot(1, 2, 1, projection='3d', computed_zorder=False)
ax1.view_init(elev=20, azim=35)

# --- 铁芯 (Cylinder) ---
z_core = np.linspace(-5, 5, 120)
theta_core = np.linspace(0, 2 * np.pi, 80)
Z_c, Theta_c = np.meshgrid(z_core, theta_core)
X_c = 1.3 * np.cos(Theta_c)
Y_c = 1.3 * np.sin(Theta_c)
ax1.plot_surface(Z_c, X_c, Y_c, color='#B0B0B0', alpha=0.25,
                 edgecolor='none', antialiased=True, shade=True)

# --- 线圈 (Coil Helix) ---
R, L, N = 1.5, 10, 16
t = np.linspace(0, N * 2 * np.pi, 3000)
x_coil = np.linspace(-L/2, L/2, 3000)
y_coil = R * np.cos(t)
z_coil = R * np.sin(t)
ax1.plot(x_coil, y_coil, z_coil, color='#D4752B', linewidth=2.8,
         label='线圈', antialiased=True)

# --- 磁感线 (Magnetic Field Lines) ---
yb = np.linspace(-1, 1, 5)
zb = np.linspace(-1, 1, 5)
Y_m, Z_m = np.meshgrid(yb, zb)
mask = (Y_m**2 + Z_m**2) < 1.1**2
Y_m, Z_m = Y_m[mask], Z_m[mask]
X_m = -4.5 * np.ones_like(Y_m)
U_m, V_m, W_m = 9.0 * np.ones_like(Y_m), np.zeros_like(Y_m), np.zeros_like(Y_m)
ax1.quiver(X_m, Y_m, Z_m, U_m, V_m, W_m, color='#DC143C', linewidth=1.5,
           arrow_length_ratio=0.08, alpha=0.85, label='$B$ 磁场')

# --- 安培环路 (Ampere Loop) ---
xl = np.array([-2.5, 2.5, 2.5, -2.5, -2.5])
yl = np.array([0, 0, 0, 0, 0])
zl = np.array([0, 0, 2.8, 2.8, 0])
ax1.plot(xl, yl, zl, color='#1E6EB8', linestyle='--', linewidth=2.8,
         label='安培环路', antialiased=True)

# --- 环路顶点标签 ---
_label_opts = dict(fontsize=12, fontweight='bold', color='#333333')
ax1.text(-2.5, 0, -0.6, 'a', **_label_opts)
ax1.text(2.5, 0, -0.6, 'b', **_label_opts)
ax1.text(2.5, 0, 3.5, 'c', **_label_opts)
ax1.text(-2.5, 0, 3.5, 'd', **_label_opts)

# --- 左侧精美公式框 ---
left_formula = (
    "长直螺线管安培环路定理" + "\n"
    r"$\oint_C \mathbf{B}\!\cdot\! d\mathbf{l}=\mu_0 I_{\mathrm{in}}$" + "\n"
    r"$\int_a^b Bdl=\mu_0(nL_{ab}I)$" + "\n"
    r"$BL_{ab}=\mu_0 nL_{ab}I$" + "\n"
    r"$\Rightarrow\ \mathbf{B}=\mu_0 nI$"
)
ax1.text2D(0.04, 0.60, left_formula, transform=ax1.transAxes, fontsize=10.5,
           bbox=dict(facecolor='#FFFEF5', edgecolor='#C0B880', alpha=0.92,
                     boxstyle='round,pad=0.7', linewidth=1.2),
           linespacing=1.6)

# --- 子图润色 ---
ax1.set_title('长直螺线管磁场与安培环路', fontsize=13, fontweight='bold', pad=10)
ax1.set_xlabel('X 轴', fontsize=10)
ax1.set_ylabel('Y 轴', fontsize=10)
ax1.set_zlabel('Z 轴', fontsize=10)
ax1.set_xlim([-6, 6])
ax1.set_ylim([-4, 4])
ax1.set_zlim([-4, 6])
ax1.legend(loc='upper right', fontsize=9, framealpha=0.85,
           edgecolor='gray', fancybox=True)
ax1.grid(True, linestyle=':', alpha=0.35)
# 设置 3D 面板颜色
ax1.xaxis.pane.fill = False
ax1.yaxis.pane.fill = False
ax1.zaxis.pane.fill = False
ax1.xaxis.pane.set_edgecolor('gray')
ax1.yaxis.pane.set_edgecolor('gray')
ax1.zaxis.pane.set_edgecolor('gray')

# ================= 2. 螺绕环子图 =================
ax2 = fig.add_subplot(1, 2, 2, projection='3d', computed_zorder=False)
ax2.view_init(elev=30, azim=20)

# --- 环形铁芯 (Torus Surface) ---
Rt, rt = 4, 0.9
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, 2 * np.pi, 60)
U_t, V_t = np.meshgrid(u, v)
Xt = (Rt + rt * np.cos(V_t)) * np.cos(U_t)
Yt = (Rt + rt * np.cos(V_t)) * np.sin(U_t)
Zt = rt * np.sin(V_t)
ax2.plot_surface(Xt, Yt, Zt, color='#A8A8A8', alpha=0.30,
                 edgecolor='none', antialiased=True, shade=True)

# --- 环形线圈 (Toroidal Coil Helix) ---
turns = 45
tt = np.linspace(0, 2 * np.pi, 3000)
theta = turns * tt
xc = (Rt + np.cos(theta)) * np.cos(tt)
yc = (Rt + np.cos(theta)) * np.sin(tt)
zc = np.sin(theta)
ax2.plot(xc, yc, zc, color='#1A8040', linewidth=2.2,
         label='线圈', antialiased=True)

# --- 内部磁场方向 (Quiver Tangent) ---
tb = np.linspace(0, 2 * np.pi, 20)
X_b, Y_b, Z_b = Rt * np.cos(tb), Rt * np.sin(tb), np.zeros_like(tb)
U_b, V_b, W_b = -np.sin(tb), np.cos(tb), np.zeros_like(tb)
ax2.quiver(X_b, Y_b, Z_b, U_b, V_b, W_b, color='#DC143C', linewidth=2.0,
           arrow_length_ratio=0.15, alpha=0.85, label='$B$ 磁场')

# --- 安培环路 (Circular Ampere Loop) ---
tl = np.linspace(0, 2 * np.pi, 400)
xl_t, yl_t, zl_t = Rt * np.cos(tl), Rt * np.sin(tl), np.zeros_like(tl)
ax2.plot(xl_t, yl_t, zl_t, color='#17A0B8', linestyle='--', linewidth=2.8,
         label='安培环路', antialiased=True)

# --- 右侧精美公式框 ---
right_formula = (
    "螺绕环安培环路定理" + "\n"
    r"$\oint_C \mathbf{B}\!\cdot\! d\mathbf{l}=\mu_0 I_{\mathrm{in}}$" + "\n"
    r"$B(2\pi r)=\mu_0 NI$" + "\n"
    r"$\Rightarrow B=\frac{\mu_0 NI}{2\pi r}$" + "\n"
    r"$\bullet\ $ 磁场集中在环内" + "\n"
    r"$\bullet\ $ 环外 $B=0$"
)
ax2.text2D(0.04, 0.56, right_formula, transform=ax2.transAxes, fontsize=10.5,
           bbox=dict(facecolor='#F0FAF5', edgecolor='#80B8A0', alpha=0.92,
                     boxstyle='round,pad=0.7', linewidth=1.2),
           linespacing=1.6)

# --- 子图润色 ---
ax2.set_title('螺绕环磁场与安培环路', fontsize=13, fontweight='bold', pad=10)
ax2.set_xlabel('X 轴', fontsize=10)
ax2.set_ylabel('Y 轴', fontsize=10)
ax2.set_zlabel('Z 轴', fontsize=10)
ax2.set_xlim([-7, 7])
ax2.set_ylim([-7, 7])
ax2.set_zlim([-4, 6])
ax2.legend(loc='upper right', fontsize=9, framealpha=0.85,
           edgecolor='gray', fancybox=True)
ax2.grid(True, linestyle=':', alpha=0.35)
# 设置 3D 面板颜色
ax2.xaxis.pane.fill = False
ax2.yaxis.pane.fill = False
ax2.zaxis.pane.fill = False
ax2.xaxis.pane.set_edgecolor('gray')
ax2.yaxis.pane.set_edgecolor('gray')
ax2.zaxis.pane.set_edgecolor('gray')

# --- 全局布局 ---
plt.subplots_adjust(left=0.04, right=0.96, top=0.90, bottom=0.06,
                    wspace=0.15)
plt.show()
