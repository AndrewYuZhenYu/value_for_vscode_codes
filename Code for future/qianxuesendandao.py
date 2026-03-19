import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button
from mpl_toolkits.mplot3d import Axes3D
import warnings
warnings.filterwarnings('ignore')

# 关键修复：删除后端强制设置，让matplotlib自动选择系统兼容的后端
# 解决中文显示（直接用系统支持的字体）
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

class QianXuesenTrajectory:
    def __init__(self):
        # 1. 创建画布（固定大小，避免布局挤压）
        self.fig = plt.figure(figsize=(12, 8))
        self.fig.suptitle('钱学森弹道可视化', fontsize=16)
        
        # 2. 划分子图（简单网格，避免复杂gs布局导致报错）
        # 3D轨迹图（占左边大部分区域）
        self.ax3d = plt.subplot(121, projection='3d')
        # 高度-速度图（占右边）
        self.ax_h = plt.subplot(222)
        self.ax_v = plt.subplot(224)

        # 3. 弹道基础参数（简化，避免计算复杂导致无数据）
        self.angle = 45  # 发射角度
        self.v0 = 2000   # 初始速度 m/s
        self.g = 9.8
        self.t_max = 500 # 最大计算时间
        self.dt = 1      # 增大时间步长，减少计算量

        # 4. 初始化数据（必须有初始值，避免空白）
        self.t_list = np.array([0])
        self.x_list = np.array([0])
        self.h_list = np.array([0])
        self.v_list = np.array([0])

        # 5. 绘制初始内容（确保一打开就有图）
        self._init_plots()
        # 6. 添加控件（放在画布底部，避免遮挡）
        self._add_controls()
        # 7. 生成初始轨迹
        self._calc_trajectory()

    def _init_plots(self):
        """初始化绘图元素，确保有初始显示"""
        # 3D轨迹图设置
        self.ax3d.set_xlabel('X (km)')
        self.ax3d.set_ylabel('Y (km)')
        self.ax3d.set_zlabel('高度 (km)')
        self.ax3d.set_xlim(0, 1000)
        self.ax3d.set_ylim(-100, 100)
        self.ax3d.set_zlim(0, 200)
        self.ax3d.view_init(elev=15, azim=45)  # 固定视角，必能看到内容

        # 初始轨迹和弹丸点
        self.line3d, = self.ax3d.plot([0], [0], [0], 'r-', linewidth=2)
        self.point, = self.ax3d.plot([0], [0], [0], 'bo', markersize=8)

        # 高度-时间图
        self.ax_h.set_title('高度-时间')
        self.ax_h.set_xlabel('t (s)')
        self.ax_h.set_ylabel('h (km)')
        self.ax_h.grid(True, alpha=0.3)
        self.line_h, = self.ax_h.plot([0], [0], 'b-')

        # 速度-时间图
        self.ax_v.set_title('速度-时间')
        self.ax_v.set_xlabel('t (s)')
        self.ax_v.set_ylabel('v (km/s)')
        self.ax_v.grid(True, alpha=0.3)
        self.line_v, = self.ax_v.plot([0], [0], 'g-')

    def _add_controls(self):
        """添加简单控件，放在画布底部，不遮挡子图"""
        # 调整控件位置：底部留出空间
        plt.subplots_adjust(bottom=0.25)

        # 角度滑块
        ax_angle = plt.axes([0.1, 0.15, 0.3, 0.03])
        self.slider_angle = Slider(ax_angle, '角度(°)', 30, 60, valinit=self.angle)
        self.slider_angle.on_changed(self._update_params)

        # 速度滑块
        ax_v0 = plt.axes([0.1, 0.1, 0.3, 0.03])
        self.slider_v0 = Slider(ax_v0, '初速度(m/s)', 1000, 3000, valinit=self.v0)
        self.slider_v0.on_changed(self._update_params)

        # 播放/暂停按钮
        ax_play = plt.axes([0.6, 0.15, 0.1, 0.04])
        self.btn_play = Button(ax_play, '播放')
        self.btn_play.on_clicked(self._toggle_play)

        # 重置按钮
        ax_reset = plt.axes([0.75, 0.15, 0.1, 0.04])
        self.btn_reset = Button(ax_reset, '重置')
        self.btn_reset.on_clicked(self._reset)

        # 运行状态
        self.is_running = False
        self.current_idx = 0

    def _calc_trajectory(self):
        """简化轨迹计算，确保能生成有效数据"""
        theta = np.radians(self.angle)
        vx0 = self.v0 * np.cos(theta)
        vz0 = self.v0 * np.sin(theta)

        t = 0
        x = 0
        h = 0
        vx = vx0
        vz = vz0

        t_list = []
        x_list = []
        h_list = []
        v_list = []

        while t < self.t_max and h >= 0:
            t_list.append(t)
            x_list.append(x / 1000)  # 转km
            h_list.append(h / 1000)  # 转km
            v = np.sqrt(vx**2 + vz**2) / 1000  # 转km/s
            v_list.append(v)

            # 简单物理模型（忽略空气阻力，确保计算不报错）
            ax = 0  # 无水平加速度
            az = -self.g  # 重力加速度

            # 更新状态
            vx += ax * self.dt
            vz += az * self.dt
            x += vx * self.dt
            h += vz * self.dt
            t += self.dt

        # 保存数据
        self.t_list = np.array(t_list)
        self.x_list = np.array(x_list)
        self.h_list = np.array(h_list)
        self.v_list = np.array(v_list)

        # 更新初始显示
        self.line3d.set_data(self.x_list, np.zeros_like(self.x_list))
        self.line3d.set_3d_properties(self.h_list)
        self.line_h.set_data(self.t_list, self.h_list)
        self.line_v.set_data(self.t_list, self.v_list)

        # 自适应坐标轴范围
        self.ax_h.set_xlim(0, self.t_max)
        self.ax_h.set_ylim(0, max(self.h_list) * 1.1)
        self.ax_v.set_xlim(0, self.t_max)
        self.ax_v.set_ylim(0, max(self.v_list) * 1.1)

    def _update_params(self, val):
        """更新参数并重新计算轨迹"""
        self.angle = self.slider_angle.val
        self.v0 = self.slider_v0.val
        self._calc_trajectory()
        self.current_idx = 0

    def _toggle_play(self, event):
        """播放/暂停切换"""
        self.is_running = not self.is_running
        self.btn_play.label.set_text('暂停' if self.is_running else '播放')

    def _reset(self, event):
        """重置所有参数"""
        self.slider_angle.reset()
        self.slider_v0.reset()
        self.is_running = False
        self.btn_play.label.set_text('播放')
        self.current_idx = 0

    def _animate(self, frame):
        """动画更新函数（极简逻辑，避免卡顿）"""
        if not self.is_running or len(self.x_list) == 0:
            return self.line3d, self.point, self.line_h, self.line_v

        # 更新当前索引
        self.current_idx = (self.current_idx + 1) % len(self.x_list)
        idx = self.current_idx

        # 更新弹丸位置
        self.point.set_data([self.x_list[idx]], [0])
        self.point.set_3d_properties([self.h_list[idx]])

        # 更新已走轨迹
        self.line3d.set_data(self.x_list[:idx+1], np.zeros_like(self.x_list[:idx+1]))
        self.line3d.set_3d_properties(self.h_list[:idx+1])

        return self.line3d, self.point, self.line_h, self.line_v

def main():
    try:
        viz = QianXuesenTrajectory()
        # 创建动画（低帧率，确保稳定）
        anim = FuncAnimation(
            viz.fig,
            viz._animate,
            interval=50,
            blit=True,
            repeat=True
        )
        plt.show()
    except Exception as e:
        print(f"运行错误: {e}")
        print("解决方案：")
        print("1. 确保安装最新版matplotlib: pip install --upgrade matplotlib")
        print("2. 关闭其他占用窗口的程序")

if __name__ == "__main__":
    main()