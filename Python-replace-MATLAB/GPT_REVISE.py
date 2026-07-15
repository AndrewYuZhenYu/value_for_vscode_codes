import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import font_manager


# ==================================================
# 字体设置（Mac / Windows 自动适配）
# ==================================================

fonts = [f.name for f in font_manager.fontManager.ttflist]

if "PingFang SC" in fonts:
    plt.rcParams["font.sans-serif"] = ["PingFang SC"]
elif "Microsoft YaHei" in fonts:
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
elif "SimHei" in fonts:
    plt.rcParams["font.sans-serif"] = ["SimHei"]

plt.rcParams["axes.unicode_minus"] = False



# ==================================================
# 全局风格
# ==================================================

plt.rcParams["figure.dpi"] = 160


fig = plt.figure(
    figsize=(15,7),
    facecolor="#05070d"
)


fig.suptitle(
    "电磁学模型：安培环路定理与磁场分布",
    fontsize=18,
    color="white",
    fontweight="bold"
)



# ==================================================
# 左：长直螺线管
# ==================================================

ax1 = fig.add_subplot(
    121,
    projection="3d",
    facecolor="#05070d"
)


ax1.view_init(
    elev=25,
    azim=35
)



# ---------- 铁芯 ----------

z = np.linspace(-5,5,120)

theta = np.linspace(
    0,
    2*np.pi,
    80
)


Z,Theta = np.meshgrid(
    z,
    theta
)


X = 1.3*np.cos(Theta)

Y = 1.3*np.sin(Theta)



ax1.plot_surface(

    Z,
    X,
    Y,

    color="#64748b",

    alpha=0.18,

    linewidth=0

)



# ---------- 线圈 ----------


N = 18


t = np.linspace(
    0,
    N*2*np.pi,
    3000
)


coil_x = np.linspace(
    -5,
    5,
    3000
)


coil_y = 1.55*np.cos(t)

coil_z = 1.55*np.sin(t)



ax1.plot(

    coil_x,
    coil_y,
    coil_z,

    color="#f5b942",

    linewidth=3

)



# ---------- 磁场箭头 ----------


yy,zz = np.meshgrid(

    np.linspace(-0.9,0.9,5),

    np.linspace(-0.9,0.9,5)

)


xx = np.ones_like(yy)*(-4)



ax1.quiver(

    xx,
    yy,
    zz,

    np.ones_like(xx)*8,

    np.zeros_like(xx),

    np.zeros_like(xx),

    color="#00eaff",

    linewidth=1.5,

    arrow_length_ratio=0.12

)




# ---------- 安培环路 ----------


loop_x = np.array(
    [-2.5,2.5,2.5,-2.5,-2.5]
)


loop_y = np.zeros(5)


loop_z = np.array(
    [0,0,2.5,2.5,0]
)


ax1.plot(

    loop_x,
    loop_y,
    loop_z,

    "--",

    color="#ff3b81",

    linewidth=2.5

)




# ---------- 公式 ----------


eq1 = (

r"$\oint_C \vec{B}\cdot d\vec{l}=\mu_0 I$"

"\n\n"

r"$BL=\mu_0 nLI$"

"\n\n"

r"$\Rightarrow B=\mu_0 nI$"

)



ax1.text2D(

    0.03,
    0.65,

    eq1,

    transform=ax1.transAxes,

    fontsize=15,

    color="white",

    bbox=dict(

        facecolor="#111827",

        edgecolor="#00eaff",

        alpha=0.9

    )

)



ax1.set_title(

    "长直螺线管磁场",

    color="white",

    fontsize=14

)




# ==================================================
# 右：螺绕环
# ==================================================

ax2 = fig.add_subplot(

    122,

    projection="3d",

    facecolor="#05070d"

)



ax2.view_init(

    elev=35,

    azim=30

)




# ---------- 环形铁芯 ----------


R = 4

r = 0.9



u = np.linspace(

    0,

    2*np.pi,

    150

)


v = np.linspace(

    0,

    2*np.pi,

    80

)



U,V = np.meshgrid(

    u,

    v

)


Xt = (

    R+r*np.cos(V)

)*np.cos(U)


Yt = (

    R+r*np.cos(V)

)*np.sin(U)


Zt = r*np.sin(V)



ax2.plot_surface(

    Xt,
    Yt,
    Zt,

    color="#64748b",

    alpha=0.22,

    linewidth=0

)



# ---------- 环形线圈 ----------


turns = 45


tt = np.linspace(

    0,

    2*np.pi,

    4000

)


angle = turns*tt



xc = (

    R+np.cos(angle)

)*np.cos(tt)


yc = (

    R+np.cos(angle)

)*np.sin(tt)


zc = np.sin(angle)



ax2.plot(

    xc,
    yc,
    zc,

    color="#22c55e",

    linewidth=3

)




# ---------- 磁场方向 ----------


a = np.linspace(

    0,

    2*np.pi,

    24

)



ax2.quiver(

    R*np.cos(a),

    R*np.sin(a),

    np.zeros_like(a),


    -np.sin(a),

    np.cos(a),

    np.zeros_like(a),


    color="#00eaff",

    linewidth=2,

    arrow_length_ratio=0.15

)




# ---------- 公式 ----------


eq2 = (

r"$\oint_C \vec{B}\cdot d\vec{l}=\mu_0NI$"

"\n\n"

r"$B(2\pi r)=\mu_0NI$"

"\n\n"

r"$B=\frac{\mu_0NI}{2\pi r}$"

)



ax2.text2D(

    0.03,
    0.65,

    eq2,

    transform=ax2.transAxes,

    fontsize=15,

    color="white",

    bbox=dict(

        facecolor="#111827",

        edgecolor="#22c55e",

        alpha=0.9

    )

)




ax2.set_title(

    "螺绕环磁场",

    color="white",

    fontsize=14

)




# ==================================================
# 最终美化
# ==================================================


for ax in [ax1,ax2]:

    ax.set_axis_off()

    ax.set_box_aspect(

        [1,1,1]

    )



plt.tight_layout()

plt.show()