import plotly.graph_objects as go
import numpy as np

# ==========================================
# 基于 Plotly 的长直螺线管与安培环路 3D 渲染
# ==========================================

# 1. 生成螺线管参数方程数据
t = np.linspace(0, 12 * np.pi, 1000) # 6圈线圈
R = 2      # 线圈半径
L_max = 20 # 螺线管总长度
z = np.linspace(0, L_max, 1000)
x = R * np.cos(t)
y = R * np.sin(t)

fig = go.Figure()

# 2. 渲染螺线管 (金铜色高光材质)
fig.add_trace(go.Scatter3d(
    x=x, y=y, z=z,
    mode='lines',
    name='螺线管 (Solenoid)',
    line=dict(
        color='#B87333', # 铜色
        width=8,         # 增加线条粗细提升实体感
    )
))

# 3. 渲染安培环路 (半透明蓝色矩形)
# 定义矩形四个顶点: a->b->c->d->a
loop_x = [0, 0, R*1.5, R*1.5, 0]
loop_y = [0, 0, 0, 0, 0]
loop_z = [5, 15, 15, 5, 5]

fig.add_trace(go.Scatter3d(
    x=loop_x, y=loop_y, z=loop_z,
    mode='lines+markers',
    name='安培环路 abcd',
    line=dict(color='#00BFFF', width=4, dash='dash'),
    marker=dict(size=4, color='red'),
    surfaceaxis=1, # 填充内部
    surfacecolor='rgba(0, 191, 255, 0.1)'
))

# 4. 渲染中心轴线磁场 B
fig.add_trace(go.Scatter3d(
    x=[0, 0], y=[0, 0], z=[-2, L_max+2],
    mode='lines',
    name='磁感应强度 B',
    line=dict(color='red', width=6)
))

# 5. 场景质感与视角优化
fig.update_layout(
    title="长直螺线管与安培环路定理 (Plotly WebGL 渲染)",
    scene=dict(
        xaxis=dict(visible=False), # 隐藏杂乱的网格线，凸显主体
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        aspectmode='data', # 强制保持真实物理比例，防止拉伸变形
        camera=dict(
            eye=dict(x=1.5, y=-2.5, z=0.5) # 设定完美的初始等轴测视角
        )
    ),
    paper_bgcolor='white',
    margin=dict(l=0, r=0, b=0, t=40)
)

# 这一步会直接在你的浏览器中弹出一个极其丝滑的交互式 3D 页面
fig.show()