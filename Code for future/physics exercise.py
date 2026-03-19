import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, Slider
import matplotlib.patches as patches

class PhysicsVisualizer:
    def __init__(self):
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(1, 3, figsize=(18, 6))
        self.fig.suptitle('物理定律可视化 - 动量守恒与动能定理', fontsize=16, fontweight='bold')
        
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 物理参数
        self.m1 = 2.0  # 物体1质量
        self.m2 = 1.0  # 物体2质量
        self.v1_initial = 3.0  # 物体1初速度
        self.v2_initial = -1.0  # 物体2初速度
        
        # 动画参数
        self.time = 0
        self.dt = 0.05
        self.animation_running = False
        
        # 数据存储
        self.time_data = []
        self.momentum1_data = []
        self.momentum2_data = []
        self.total_momentum_data = []
        self.kinetic1_data = []
        self.kinetic2_data = []
        self.total_kinetic_data = []
        
        self.setup_plots()
        self.setup_controls()
        
    def setup_plots(self):
        """设置三个子图"""
        # 子图1: 碰撞过程可视化
        self.ax1.set_xlim(0, 10)
        self.ax1.set_ylim(0, 5)
        self.ax1.set_title('弹性碰撞过程', fontweight='bold')
        self.ax1.set_xlabel('位置 (m)')
        self.ax1.grid(True, alpha=0.3)
        
        # 子图2: 动量变化
        self.ax2.set_xlim(0, 10)
        self.ax2.set_ylim(-10, 10)
        self.ax2.set_title('动量变化', fontweight='bold')
        self.ax2.set_xlabel('时间 (s)')
        self.ax2.set_ylabel('动量 (kg·m/s)')
        self.ax2.grid(True, alpha=0.3)
        
        # 子图3: 动能变化
        self.ax3.set_xlim(0, 10)
        self.ax3.set_ylim(0, 20)
        self.ax3.set_title('动能变化', fontweight='bold')
        self.ax3.set_xlabel('时间 (s)')
        self.ax3.set_ylabel('动能 (J)')
        self.ax3.grid(True, alpha=0.3)
        
        # 初始化绘图对象
        self.ball1, = self.ax1.plot([], [], 'ro', markersize=15, label=f'球1 (m={self.m1}kg)')
        self.ball2, = self.ax1.plot([], [], 'bo', markersize=10, label=f'球2 (m={self.m2}kg)')
        self.ax1.legend()
        
        # 连接线（表示弹簧/相互作用力）
        self.connection_line, = self.ax1.plot([], [], 'k-', linewidth=2, alpha=0.5)
        
        # 速度矢量
        self.arrow1 = None
        self.arrow2 = None
        
        # 动量曲线
        self.line_momentum1, = self.ax2.plot([], [], 'r-', label='球1动量', linewidth=2)
        self.line_momentum2, = self.ax2.plot([], [], 'b-', label='球2动量', linewidth=2)
        self.line_total_momentum, = self.ax2.plot([], [], 'k--', label='总动量', linewidth=3)
        self.ax2.legend()
        
        # 动能曲线
        self.line_kinetic1, = self.ax3.plot([], [], 'r-', label='球1动能', linewidth=2)
        self.line_kinetic2, = self.ax3.plot([], [], 'b-', label='球2动能', linewidth=2)
        self.line_total_kinetic, = self.ax3.plot([], [], 'g-', label='总动能', linewidth=3)
        self.ax3.legend()
        
        # 理论值线
        self.theoretical_momentum = self.ax2.axhline(y=self.m1*self.v1_initial + self.m2*self.v2_initial, 
                                                  color='purple', linestyle=':', alpha=0.7, 
                                                  label='理论总动量')
        self.ax2.legend()
        
    def setup_controls(self):
        """设置控制按钮和滑块"""
        # 调整滑块位置
        ax_slider1 = plt.axes([0.1, 0.02, 0.2, 0.03])
        ax_slider2 = plt.axes([0.4, 0.02, 0.2, 0.03])
        ax_slider3 = plt.axes([0.7, 0.02, 0.2, 0.03])
        
        # 质量滑块
        self.slider_m1 = Slider(ax_slider1, '球1质量', 0.5, 5.0, valinit=self.m1)
        self.slider_m2 = Slider(ax_slider2, '球2质量', 0.5, 5.0, valinit=self.m2)
        
        # 速度滑块
        self.slider_v1 = Slider(ax_slider3, '球1初速', -5.0, 5.0, valinit=self.v1_initial)
        
        # 连接滑块事件
        self.slider_m1.on_changed(self.update_parameters)
        self.slider_m2.on_changed(self.update_parameters)
        self.slider_v1.on_changed(self.update_parameters)
        
        # 控制按钮
        ax_start = plt.axes([0.02, 0.1, 0.08, 0.04])
        ax_reset = plt.axes([0.02, 0.05, 0.08, 0.04])
        
        self.btn_start = Button(ax_start, '开始')
        self.btn_reset = Button(ax_reset, '重置')
        
        self.btn_start.on_clicked(self.start_animation)
        self.btn_reset.on_clicked(self.reset_animation)
        
        # 添加文本框显示物理量
        self.text_box = self.fig.text(0.02, 0.85, '', fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
        
    def update_parameters(self, val):
        """更新物理参数"""
        self.m1 = self.slider_m1.val
        self.m2 = self.slider_m2.val
        self.v1_initial = self.slider_v1.val
        
        # 更新标签
        self.ball1.set_label(f'球1 (m={self.m1:.1f}kg)')
        self.ball2.set_label(f'球2 (m={self.m2:.1f}kg)')
        self.ax1.legend()
        
        # 更新理论值
        theoretical = self.m1 * self.v1_initial + self.m2 * (-1.0)  # 假设球2初始速度为-1
        self.theoretical_momentum.set_ydata([theoretical, theoretical])
        
        self.reset_animation()
        
    def calculate_collision(self, x1, x2, v1, v2):
        """计算碰撞后的速度（弹性碰撞）"""
        # 弹性碰撞公式
        v1_final = ((self.m1 - self.m2) * v1 + 2 * self.m2 * v2) / (self.m1 + self.m2)
        v2_final = ((self.m2 - self.m1) * v2 + 2 * self.m1 * v1) / (self.m1 + self.m2)
        
        return v1_final, v2_final
        
    def init_animation(self):
        """初始化动画"""
        self.ball1.set_data([], [])
        self.ball2.set_data([], [])
        self.connection_line.set_data([], [])
        
        self.line_momentum1.set_data([], [])
        self.line_momentum2.set_data([], [])
        self.line_total_momentum.set_data([], [])
        
        self.line_kinetic1.set_data([], [])
        self.line_kinetic2.set_data([], [])
        self.line_total_kinetic.set_data([], [])
        
        self.time_data = []
        self.momentum1_data = []
        self.momentum2_data = []
        self.total_momentum_data = []
        self.kinetic1_data = []
        self.kinetic2_data = []
        self.total_kinetic_data = []
        
        self.time = 0
        return self.ball1, self.ball2, self.connection_line, \
               self.line_momentum1, self.line_momentum2, self.line_total_momentum, \
               self.line_kinetic1, self.line_kinetic2, self.line_total_kinetic
        
    def animate(self, frame):
        """动画更新函数"""
        if not self.animation_running:
            return self.ball1, self.ball2, self.connection_line, \
                   self.line_momentum1, self.line_momentum2, self.line_total_momentum, \
                   self.line_kinetic1, self.line_kinetic2, self.line_total_kinetic
        
        # 更新时间
        self.time += self.dt
        
        # 初始位置
        if self.time < 2:  # 接近阶段
            x1 = 1 + self.v1_initial * self.time
            x2 = 8 + (-1.0) * self.time
            v1 = self.v1_initial
            v2 = -1.0
            
            # 绘制连接线表示相互作用
            if abs(x2 - x1) < 3:
                self.connection_line.set_data([x1 + 0.5, x2 - 0.5], [2.5, 2.5])
            else:
                self.connection_line.set_data([], [])
                
        elif self.time < 4:  # 碰撞阶段
            collision_progress = (self.time - 2) / 2
            
            # 碰撞动画效果
            x1 = 4 + collision_progress * 0.5
            x2 = 5 - collision_progress * 0.5
            
            # 碰撞瞬间交换速度
            if collision_progress < 0.5:
                v1 = self.v1_initial
                v2 = -1.0
            else:
                v1, v2 = self.calculate_collision(0, 0, self.v1_initial, -1.0)
                
            self.connection_line.set_data([x1 + 0.5, x2 - 0.5], [2.5, 2.5])
            
        else:  # 分离阶段
            separation_time = self.time - 4
            v1, v2 = self.calculate_collision(0, 0, self.v1_initial, -1.0)
            
            x1 = 4.5 + v1 * separation_time
            x2 = 4.5 + v2 * separation_time
            self.connection_line.set_data([], [])
        
        # 边界检查
        if x1 < 0.5: x1 = 0.5
        if x1 > 9.5: x1 = 9.5
        if x2 < 0.5: x2 = 0.5
        if x2 > 9.5: x2 = 9.5
        
        # 更新球的位置
        self.ball1.set_data([x1], [2.5])
        self.ball2.set_data([x2], [2.5])
        
        # 计算物理量
        p1 = self.m1 * v1
        p2 = self.m2 * v2
        total_p = p1 + p2
        
        k1 = 0.5 * self.m1 * v1**2
        k2 = 0.5 * self.m2 * v2**2
        total_k = k1 + k2
        
        # 存储数据
        self.time_data.append(self.time)
        self.momentum1_data.append(p1)
        self.momentum2_data.append(p2)
        self.total_momentum_data.append(total_p)
        self.kinetic1_data.append(k1)
        self.kinetic2_data.append(k2)
        self.total_kinetic_data.append(total_k)
        
        # 限制数据点数量
        max_points = 200
        if len(self.time_data) > max_points:
            self.time_data = self.time_data[-max_points:]
            self.momentum1_data = self.momentum1_data[-max_points:]
            self.momentum2_data = self.momentum2_data[-max_points:]
            self.total_momentum_data = self.total_momentum_data[-max_points:]
            self.kinetic1_data = self.kinetic1_data[-max_points:]
            self.kinetic2_data = self.kinetic2_data[-max_points:]
            self.total_kinetic_data = self.total_kinetic_data[-max_points:]
        
        # 更新图表
        self.line_momentum1.set_data(self.time_data, self.momentum1_data)
        self.line_momentum2.set_data(self.time_data, self.momentum2_data)
        self.line_total_momentum.set_data(self.time_data, self.total_momentum_data)
        
        self.line_kinetic1.set_data(self.time_data, self.kinetic1_data)
        self.line_kinetic2.set_data(self.time_data, self.kinetic2_data)
        self.line_total_kinetic.set_data(self.time_data, self.total_kinetic_data)
        
        # 动态调整坐标轴范围
        if self.time_data:
            self.ax2.set_xlim(0, max(10, self.time))
            self.ax3.set_xlim(0, max(10, self.time))
            
            # 调整y轴范围
            all_momenta = self.momentum1_data + self.momentum2_data + self.total_momentum_data
            if all_momenta:
                margin = max(2, max(abs(min(all_momenta)), abs(max(all_momenta))) * 0.1)
                self.ax2.set_ylim(min(all_momenta) - margin, max(all_momenta) + margin)
            
            all_kinetic = self.kinetic1_data + self.kinetic2_data + self.total_kinetic_data
            if all_kinetic:
                self.ax3.set_ylim(0, max(all_kinetic) * 1.1)
        
        # 更新文本框
        theoretical_p = self.m1 * self.v1_initial + self.m2 * (-1.0)
        momentum_error = abs(total_p - theoretical_p) / abs(theoretical_p) * 100 if theoretical_p != 0 else 0
        
        text_info = f"""实时数据:
时间: {self.time:.2f}s
球1速度: {v1:.2f} m/s
球2速度: {v2:.2f} m/s
总动量: {total_p:.2f} kg·m/s
总动能: {total_k:.2f} J
动量误差: {momentum_error:.2f}%
动量守恒成立: {'是' if momentum_error < 1 else '否'}"""
        
        self.text_box.set_text(text_info)
        
        # 绘制速度矢量
        if self.arrow1:
            self.arrow1.remove()
        if self.arrow2:
            self.arrow2.remove()
            
        scale = 2
        self.arrow1 = self.ax1.arrow(x1, 2.5, v1 * scale, 0, head_width=0.3, 
                                    head_length=0.2, fc='r', ec='r', alpha=0.7)
        self.arrow2 = self.ax1.arrow(x2, 2.5, v2 * scale, 0, head_width=0.3, 
                                    head_length=0.2, fc='b', ec='b', alpha=0.7)
        
        return self.ball1, self.ball2, self.connection_line, \
               self.line_momentum1, self.line_momentum2, self.line_total_momentum, \
               self.line_kinetic1, self.line_kinetic2, self.line_total_kinetic, \
               self.arrow1, self.arrow2
        
    def start_animation(self, event):
        """开始/暂停动画"""
        self.animation_running = not self.animation_running
        self.btn_start.label.set_text('暂停' if self.animation_running else '开始')
        
    def reset_animation(self, event=None):
        """重置动画"""
        self.animation_running = False
        self.btn_start.label.set_text('开始')
        self.init_animation()
        
    def show_explanation(self):
        """显示物理原理解释"""
        explanation = """
物理定律说明:

🔵 动量守恒定律:
• 在一个封闭系统中，如果没有外力作用，系统的总动量保持不变
• 数学表达式: m₁v₁ + m₂v₂ = m₁v₁' + m₂v₂'
• 在我们的演示中，可以看到总动量曲线保持水平

🔵 动能定理:
• 合外力对物体做的功等于物体动能的变化
• 数学表达式: W = ΔK = K₂ - K₁
• 在弹性碰撞中，总动能也守恒

🔵 弹性碰撞特点:
• 动量守恒 ✓
• 动能守恒 ✓
• 碰撞前后相对速度大小相等，方向相反

调节参数观察:
• 改变质量比，观察动量分配
• 改变初速度，观察能量转换
• 观察数值计算的精度
        """
        
        print(explanation)
        
        # 在图上添加说明
        fig_explain, ax_explain = plt.subplots(figsize=(10, 8))
        ax_explain.text(0.05, 0.95, explanation, transform=ax_explain.transAxes, 
                       fontsize=11, verticalalignment='top', fontfamily='monospace')
        ax_explain.axis('off')
        plt.tight_layout()
        plt.show()

def main():
    """主函数"""
    print("🎯 物理定律可视化程序")
    print("=" * 50)
    print("本程序演示动量守恒和动能定理")
    print("使用说明:")
    print("1. 调节滑块改变物理参数")
    print("2. 点击'开始'按钮观察碰撞过程")
    print("3. 观察右侧图表中的动量和动能变化")
    print("4. 查看实时数据验证物理定律")
    print("=" * 50)
    
    visualizer = PhysicsVisualizer()
    
    # 创建动画
    anim = FuncAnimation(visualizer.fig, visualizer.animate, frames=1000,
                        init_func=visualizer.init_animation, blit=False, interval=50)
    
    # 添加说明按钮
    ax_explain_btn = plt.axes([0.02, 0.15, 0.08, 0.04])
    btn_explain = Button(ax_explain_btn, '物理原理')
    btn_explain.on_clicked(lambda x: visualizer.show_explanation())
    
    plt.tight_layout(rect=[0, 0.1, 1, 0.95])
    plt.show()

if __name__ == "__main__":
    main()