import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

plt.rcParams['font.family'] = 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 网格
x = np.linspace(0, 1, 60)
y = np.linspace(0, 1, 60)
X, Y = np.meshgrid(x, y)

mask = (X + Y <= 1) & (X >= 0) & (Y >= 0)

Z_top = np.where(mask, X + Y, np.nan)
Z_bot = np.where(mask, X * Y, np.nan)

# 上曲面 z = x+y
ax.plot_surface(X, Y, Z_top, color='steelblue', alpha=0.7, linewidth=0)

# 下曲面 z = xy
ax.plot_surface(X, Y, Z_bot, color='tomato', alpha=0.7, linewidth=0)

# 侧面 x=0: y从0到1, z从0到y
t = np.linspace(0, 1, 60)
T1, Z1 = np.meshgrid(t, t)
X_s1 = np.zeros_like(T1)
Y_s1 = T1
Z_s1_top = np.where(T1 <= 1, T1, np.nan)       # z = y
Z_s1_bot = np.zeros_like(T1)                    # z = 0
mask_s1 = (Z1 >= Z_s1_bot) & (Z1 <= Z_s1_top)
Z_s1 = np.where(mask_s1, Z1, np.nan)
ax.plot_surface(X_s1, Y_s1, Z_s1, color='mediumseagreen', alpha=0.6, linewidth=0)

# 侧面 y=0: x从0到1, z从0到x
X_s2 = T1
Y_s2 = np.zeros_like(T1)
Z_s2_top = np.where(T1 <= 1, T1, np.nan)
mask_s2 = (Z1 >= 0) & (Z1 <= Z_s2_top)
Z_s2 = np.where(mask_s2, Z1, np.nan)
ax.plot_surface(X_s2, Y_s2, Z_s2, color='mediumseagreen', alpha=0.6, linewidth=0)

# 侧面 x+y=1
s = np.linspace(0, 1, 60)
S, Zz = np.meshgrid(s, np.linspace(0, 1, 60))
X_s3 = S
Y_s3 = 1 - S
Z_bot3 = S * (1 - S)
Z_top3 = np.ones_like(S)
mask_s3 = (Zz >= Z_bot3) & (Zz <= Z_top3)
Z_s3 = np.where(mask_s3, Zz, np.nan)
ax.plot_surface(X_s3, Y_s3, Z_s3, color='mediumpurple', alpha=0.6, linewidth=0)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('z=x+y（蓝）与 z=xy（红）围成的立体\n区域: x≥0, y≥0, x+y≤1')

from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='steelblue',     alpha=0.7, label='上曲面 z = x+y'),
    Patch(facecolor='tomato',        alpha=0.7, label='下曲面 z = xy'),
    Patch(facecolor='mediumseagreen',alpha=0.6, label='侧面 x=0 / y=0'),
    Patch(facecolor='mediumpurple',  alpha=0.6, label='侧面 x+y=1'),
]
ax.legend(handles=legend_elements, loc='upper left')

ax.view_init(elev=25, azim=45)
plt.tight_layout()
plt.savefig('solid.png', dpi=150)
plt.show()