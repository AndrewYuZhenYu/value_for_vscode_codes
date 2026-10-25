第12章 气体动理论
一、理想气体物态方程 ★★★★★
核心公式

- 物态方程：$pV=\nu RT=\dfrac{m}{M}RT$
- 微观形式：$p=nkT$
- 物质的量：$\nu=\dfrac{m}{M}=\dfrac{N}{N_A}$
- 分子数密度：$n=\dfrac{N}{V}$
- 质量密度：$\rho=nm_0$，$m_0=\dfrac{M}{N_A}$
  三个实验定律
- 等温（玻意耳）：$pV=C$
- 等容（查理）：$\dfrac{p}{T}=C$
- 等压（盖-吕萨克）：$\dfrac{V}{T}=C$
- 定量气体的综合关系：$\dfrac{p_1V_1}{T_1}=\dfrac{p_2V_2}{T_2}$
  混合气体
- 道尔顿分压定律：$p=p_1+p_2+\cdots$
- 分压强：$p_i=n_i kT$
  二、理想气体微观模型 ★★★★☆
  四个基本假设
- 分子的大小可忽略，视为质点
- 除碰撞瞬间外，分子间作用力可忽略
- 分子间及分子与器壁的碰撞均为完全弹性碰撞
- 分子服从经典运动规律
  平衡态统计假设
- 空间分布均匀：$n=N/V$
- 速度方向各向同性
  - $\overline{v_x}=\overline{v_y}=\overline{v_z}=0$
  - $\overline{v_x^2}=\overline{v_y^2}=\overline{v_z^2}=\dfrac{1}{3}\overline{v^2}$
- 注意：平均速度分量为零 $\ne$ 平均速率为零
  三、压强与温度的微观解释 ★★★★★
  压强
- 压强公式：$p=\dfrac{1}{3}nm_0\overline{v^2}$
- 动能形式：$p=\dfrac{2}{3}n\overline{\varepsilon}_{\mathrm{平}}$
- 微观本质：大量分子不断撞击器壁的统计平均效果
  温度
- 平均平动动能：$\boxed{\overline{\varepsilon}_{\mathrm{平}}=\dfrac{3}{2}kT}$
- 微观意义：温度反映分子热运动的剧烈程度
- 同温下不同理想气体的平均平动动能相等
- 温度具有统计意义，不能直接赋予单个分子
  方均根速率
- $v_{\mathrm{rms}}=\sqrt{\overline{v^2}}$
- $\boxed{v_{\mathrm{rms}}=\sqrt{\dfrac{3kT}{m_0}}=\sqrt{\dfrac{3RT}{M}}}$
- 密度形式：$v_{\mathrm{rms}}=\sqrt{\dfrac{3p}{\rho}}$
  四、能量均分与理想气体内能 ★★★★★
  自由度（刚性分子）
- 单原子分子：$i=3$（3 个平动）
- 双原子分子：$i=5$（3 个平动 + 2 个转动）
- 一般非线性多原子分子：$i=6$（3 个平动 + 3 个转动）
- 常温下按本章模型忽略振动自由度
  能量均分定理
- 每个平动或转动自由度的平均动能：$\dfrac{1}{2}kT$
- 平均平动动能：$\overline{\varepsilon}_{\mathrm{平}}=\dfrac{3}{2}kT$
- 平均总动能（刚性分子）：$\overline{\varepsilon}_{\mathrm{总}}=\dfrac{i}{2}kT$
- 区别：平动动能与 $i$ 无关；总动能与 $i$ 有关
  刚性理想气体的内能
- $\boxed{U=\dfrac{i}{2}\nu RT=\dfrac{i}{2}\dfrac{m}{M}RT}$
- 等价形式：$U=\dfrac{i}{2}pV$
- 内能变化（定量、定自由度）：$\Delta U=\dfrac{i}{2}\nu R(T_2-T_1)$
- 核心结论：一定量理想气体的内能只与温度有关
  - 等温：$\Delta U=0$
  - 升温：$\Delta U>0$
  - 降温：$\Delta U<0$
- 混合气体：$U=\sum_j\dfrac{i_j}{2}\nu_jRT$
  五、麦克斯韦速率分布 ★★★★★
  分布函数与积分
- 定义：$f(v)=\dfrac{dN}{N,dv}$（概率密度）
- 归一化：$\displaystyle\int_0^\infty f(v),dv=1$
- 区间占比：$\displaystyle\frac{\Delta N}{N}=\int_{v_1}^{v_2}f(v),dv$
- 平均速率：$\displaystyle\overline v=\int_0^\infty vf(v),dv$
- 区间平均速率：$\displaystyle\overline v_{12}=\frac{\int_{v_1}^{v_2}vf(v),dv}{\int_{v_1}^{v_2}f(v),dv}$
  三种统计速率（必背）
- 最概然速率：$\boxed{v_p=\sqrt{\dfrac{2RT}{M}}}$
- 平均速率：$\boxed{\overline v=\sqrt{\dfrac{8RT}{\pi M}}}$
- 方均根速率：$\boxed{v_{\mathrm{rms}}=\sqrt{\dfrac{3RT}{M}}}$
- 大小顺序：$\boxed{v_p<\overline v<v_{\mathrm{rms}}}$
- 记忆系数：$2<8/\pi<3$
- 共同关系：特征速率 $\propto\sqrt{T/M}$
  曲线变化规律
- 同种气体升温：峰向右移、降低，曲线变宽
- 同温下分子质量减小：峰向右移、降低，曲线变宽
- 曲线下总面积始终为 1
- 最概然速率是峰所在位置，不是平均速率
  完整分布函数（了解）
- $\displaystyle f(v)=4\pi\left(\frac{m_0}{2\pi kT}\right)^{3/2}v^2e^{-\frac{m_0v^2}{2kT}}$
  六、分子碰撞与平均自由程 ★★★★☆
  两个统计量
- 平均自由程 $\overline\lambda$：两次相邻碰撞之间自由路程的平均值
- 平均碰撞频率 $\overline Z$：一个分子单位时间内碰撞的平均次数
  核心公式
- 碰撞频率：$\boxed{\overline Z=\sqrt2\pi d^2n\overline v}$
- 平均自由程：$\boxed{\overline\lambda=\frac{\overline v}{\overline Z}=\frac{1}{\sqrt2\pi d^2n}}$
- 压强形式：$\boxed{\overline\lambda=\frac{kT}{\sqrt2\pi d^2p}}$
- $d$ 为分子的有效直径
  升温的影响（气体种类和数量不变）
- 等容升温：$\overline v\uparrow$，$\overline Z\uparrow$，$\overline\lambda$ 不变
- 恒压升温：$\overline v\uparrow$，$\overline Z\downarrow$，$\overline\lambda\uparrow$
- 比例关系：$\overline v\propto\sqrt T$，$\overline Z\propto n\sqrt T$，$\overline\lambda\propto 1/n$
  七、关键概念 ★★★☆☆
  状态与过程
- 平衡态：按本章条件，系统与外界无能量和物质交换，宏观性质不再随时间变化
- 稳恒态：宏观性质不随时间变，但可以有持续的能量流或物质流
- 准静态过程：所有中间状态都无限接近平衡态
- 热力学第零定律：分别与第三系统热平衡的两个系统也相互热平衡
  统计与温度
- 统计规律：单个分子的运动具有偶然性，大量分子的总体行为呈稳定规律
- 绝对零度：不能通过有限步骤达到 $0,\mathrm K$
- 玻尔兹曼分布（选学）：$n_B(r)=n_0e^{-\varepsilon_p(r)/(kT)}$
  - 分子处于较高势能位置的概率较低
    八、高频易错点 ★★★★★
- 平均平动动能 $\frac32kT$ $\ne$ 平均总动能 $\frac i2kT$
- 同温不同气体：平均平动动能相等，特征速率可以不同
- 温度升高 $\ne$ 每个分子的速率都增大
- $f(v)$ 是概率密度；区间面积 $\displaystyle\int_{v_1}^{v_2}f(v),dv$ 才是概率
- 最概然速率、平均速率、方均根速率不可混淆
- 漏气或充气：不能把定量气体的 $pV/T=C$ 直接用于前后两状态
- 摩尔质量 $M$ 在 SI 制中用 $\mathrm{kg/mol}$
- 温度必须用热力学温度 $\mathrm K$
  九、常用常量 ★★★★☆
- 气体常量：$R=8.31,\mathrm{J/(mol\cdot K)}$
- 玻尔兹曼常数：$k=1.38\times10^{-23},\mathrm{J/K}$
- 阿伏伽德罗常数：$N_A=6.02\times10^{23},\mathrm{mol^{-1}}$
- 温度换算：$T=t+273.15$（常规题可按教材取 $273$）
- 标准条件摩尔体积：$V_m=22.4,\mathrm{L/mol}$（按本章标准条件）
