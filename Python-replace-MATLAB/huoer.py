import numpy as np
import plotly.graph_objects as go


# ============================
# 创建画布
# ============================

fig = go.Figure()


# ============================
# 参数
# ============================

L = 6      # 长度
W = 3      # 宽度
T = 2      # 厚度


# ============================
# 霍尔元件长方体
# ============================

vertices = np.array([
    [0,0,0],
    [L,0,0],
    [L,W,0],
    [0,W,0],
    [0,0,T],
    [L,0,T],
    [L,W,T],
    [0,W,T]
])


faces = [
    [0,1,2,3],
    [4,5,6,7],
    [0,1,5,4],
    [1,2,6,5],
    [2,3,7,6],
    [3,0,4,7]
]


x=[]
y=[]
z=[]

for f in faces:
    for i in f:
        x.append(vertices[i,0])
        y.append(vertices[i,1])
        z.append(vertices[i,2])
    x.append(None)
    y.append(None)
    z.append(None)



fig.add_trace(
    go.Mesh3d(
        x=x,
        y=y,
        z=z,
        color="cyan",
        opacity=0.35,
        name="Hall element"
    )
)



# ============================
# 电流方向 I
# ============================

fig.add_trace(
    go.Cone(
        x=[1],
        y=[W/2],
        z=[T/2],

        u=[3],
        v=[0],
        w=[0],

        colorscale="reds",
        showscale=False,

        sizemode="absolute",
        sizeref=0.8,

        name="Current I"
    )
)


fig.add_trace(
    go.Scatter3d(
        x=[0.5],
        y=[W/2],
        z=[T/2],

        mode="text",

        text=["I →"],

        textfont=dict(
            size=20,
            color="red"
        )
    )
)



# ============================
# 磁场 B
# ============================

for xx in np.linspace(0.8,L-0.8,6):

    fig.add_trace(
        go.Cone(

            x=[xx],
            y=[W/2],
            z=[T+1],

            u=[0],
            v=[0],
            w=[-1],

            colorscale="blues",

            showscale=False,

            sizemode="absolute",

            sizeref=0.5
        )
    )


fig.add_trace(
    go.Scatter3d(

        x=[L/2],
        y=[W/2],
        z=[T+1.4],

        mode="text",

        text=["B ↓"],

        textfont=dict(
            size=22,
            color="cyan"
        )
    )
)



# ============================
# 霍尔电场 EH
# ============================


fig.add_trace(

    go.Cone(

        x=[L/2],
        y=[W/2],
        z=[0.5],

        u=[0],
        v=[1.5],
        w=[0],

        colorscale="reds",

        showscale=False,

        sizeref=0.6

    )
)



fig.add_trace(

go.Scatter3d(

x=[L/2],
y=[W+0.5],
z=[0.5],

mode="text",

text=["E_H"],

textfont=dict(

size=20,

color="orange"

)

)

)



# ============================
# 电荷运动轨迹
# ============================


for y0 in np.linspace(0.5,W-0.5,5):

    fig.add_trace(

        go.Scatter3d(

            x=np.linspace(1,L-1,30),

            y=np.ones(30)*y0,

            z=np.ones(30)*T/2,

            mode="lines",

            line=dict(

                color="white",

                width=2,

                dash="dot"

            ),

            showlegend=False

        )

    )



# ============================
# 三维尺寸标注
# ============================


fig.add_trace(

go.Scatter3d(

x=[0,L],

y=[-0.5,-0.5],

z=[0,0],

mode="lines+text",

text=["0","L"],

line=dict(width=5,color="yellow"),

name="Length"

)

)



fig.add_trace(

go.Scatter3d(

x=[L,L],

y=[0,W],

z=[-0.5,-0.5],

mode="lines+text",

text=["0","w"],

line=dict(width=5,color="yellow")

)

)


fig.add_trace(

go.Scatter3d(

x=[-0.5,-0.5],

y=[0,0],

z=[0,T],

mode="lines+text",

text=["0","t"],

line=dict(width=5,color="yellow")

)

)



# ============================
# 右侧推导公式
# ============================


formula = r"""

<b style='font-size:24px;color:#66ccff'>
Hall Effect Derivation
</b>

<br><br>

<b>1. Lorentz Force</b>

<br>

$$
F_L=q(v_d\times B)
$$

<br>

<b>2. Force Balance</b>

<br>

$$
qE_H=qv_dB
$$


$$
E_H=v_dB
$$


<br>

<b>3. Hall Voltage</b>


$$
V_H=E_H w
$$


$$
V_H=v_dBw
$$


<br>

<b>4. Current relation</b>


$$
J=nqv_d
$$


$$
v_d=\frac{I}{nqA}
$$


where


$$
A=wt
$$


<br>

<b>5. Final result</b>


$$
\boxed{
V_H=
\frac{IB}{nqt}
}
$$


"""



fig.add_annotation(

text=formula,

xref="paper",

yref="paper",

x=0.78,

y=0.5,

showarrow=False,

align="left",

font=dict(

size=16,

color="white"

),

bgcolor="rgba(10,20,40,0.85)",

bordercolor="#3399ff",

borderwidth=2

)



# ============================
# 布局
# ============================


fig.update_layout(

title=dict(

text="Hall Effect : Physical Model and Derivation",

font=dict(size=28,color="white")

),


paper_bgcolor="#050b18",

plot_bgcolor="#050b18",


scene=dict(

xaxis=dict(
showgrid=False,
title="x"
),

yaxis=dict(
showgrid=False,
title="y"
),

zaxis=dict(
showgrid=False,
title="z"
),


camera=dict(

eye=dict(

x=1.5,

y=1.5,

z=1.2

)

)

),


width=1600,

height=900,


showlegend=False

)



# ============================
# 输出
# ============================


fig.write_html(

"Hall_effect_visualization.html"

)


fig.show()