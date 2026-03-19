import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

class DragLensVisualizer:
    def __init__(self):
        self.init_plot()
        
    def init_plot(self):
        """初始化带滑块的图形界面"""
        # 创建图形和子图
        self.fig, (self.ax_main, self.ax_chart) = plt.subplots(1, 2, figsize=(15, 6))
        plt.subplots_adjust(bottom=0.25)
        
        # 初始参数
        self.focal_length_init = 5.0
        self.object_distance_init = 10.0
        
        # 创建滑块区域
        slider_axes = [
            plt.axes([0.2, 0.15, 0.65, 0.03]),  # 焦距滑块
            plt.axes([0.2, 0.10, 0.65, 0.03])   # 物距滑块
        ]
        
        # 创建滑块
        self.f_slider = Slider(slider_axes[0], '焦距 f (cm)', 1.0, 15.0, 
                              valinit=self.focal_length_init, valstep=0.1)
        self.d_slider = Slider(slider_axes[1], '物距 d₀ (cm)', 1.0, 25.0, 
                              valinit=self.object_distance_init, valstep=0.1)
        
        # 创建按钮
        button_axes = [
            plt.axes([0.3, 0.02, 0.1, 0.04]),   # 重置按钮
            plt.axes([0.6, 0.02, 0.1, 0.04])    # 动画按钮
        ]
        
        self.reset_button = Button(button_axes[0], '重置')
        self.animate_button = Button(button_axes[1], '动画演示')
        
        # 绑定事件
        self.f_slider.on_changed(self.update_plot)
        self.d_slider.on_changed(self.update_plot)
        self.reset_button.on_clicked(self.reset_parameters)
        self.animate_button.on_clicked(self.animate_focal_change)
        
        # 初始绘图
        self.update_plot()
        
        # 显示图形
        plt.show()
    
    def lens_formula(self, do, f):
        """透镜公式计算"""
        if abs(do - f) < 1e-6:
            return float('inf')
        return 1 / (1/f - 1/do)
    
    def magnification(self, do, di):
        """计算放大率"""
        return abs(di / do)
    
    def update_plot(self, val=None):
        """更新绘图（滑块拖动时调用）"""
        # 获取当前滑块值
        self.focal_length = self.f_slider.val
        self.object_distance = self.d_slider.val
        
        # 清除图形
        self.ax_main.clear()
        self.ax_chart.clear()
        
        # 计算像距和放大率
        image_distance = self.lens_formula(self.object_distance, self.focal_length)
        magnification = self.magnification(self.object_distance, image_distance)
        
        # 绘制主图（光学示意图）
        self.plot_optical_diagram(image_distance, magnification)
        
        # 绘制图表（成像规律）
        self.plot_imaging_chart()
        
        # 更新标题显示当前参数
        self.fig.suptitle(f'凸透镜成像可视化 - f={self.focal_length:.1f}cm, d₀={self.object_distance:.1f}cm', 
                         fontsize=14, fontweight='bold')
        
        # 刷新图形
        self.fig.canvas.draw_idle()
    
    def plot_optical_diagram(self, image_distance, magnification):
        """绘制光学示意图"""
        ax = self.ax_main
        
        # 设置坐标系
        ax.set_xlim(-20, 30)
        ax.set_ylim(-8, 8)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title('光学示意图', fontsize=12)
        ax.set_xlabel('距离 (cm)')
        ax.set_ylabel('高度 (cm)')
        
        # 透镜位置
        lens_pos = 0
        
        # 绘制透镜
        ax.plot([lens_pos, lens_pos], [-1, 1], 'k-', linewidth=8)
        ax.text(lens_pos, 1.5, '凸透镜', ha='center', fontsize=14, fontweight='bold')
        
        # 焦点
        f_left = lens_pos - self.focal_length
        f_right = lens_pos + self.focal_length
        ax.plot([f_left, f_left], [-0.5, 0.5], 'ro-', linewidth=3, markersize=8)
        ax.plot([f_right, f_right], [-0.5, 0.5], 'ro-', linewidth=3, markersize=8)
        ax.text(f_left, -1, f'F({f_left:.1f})', ha='center', fontsize=11, color='red')
        ax.text(f_right, -1, f'F\'({f_right:.1f})', ha='center', fontsize=11, color='red')
        
        # 物体（蓝色箭头）
        object_height = 2.5
        object_pos = lens_pos - self.object_distance
        ax.arrow(object_pos, 0, 0, object_height, head_width=0.4, head_length=0.4, 
                fc='blue', ec='blue', linewidth=4)
        ax.text(object_pos, object_height + 0.8, '物体', ha='center', fontsize=12, color='blue', fontweight='bold')
        
        # 像
        if image_distance > 0:
            # 实像（红色向下箭头）
            image_pos = lens_pos + image_distance
            image_height = -object_height * magnification
            ax.arrow(image_pos, 0, 0, image_height, head_width=0.4, head_length=0.4, 
                    fc='red', ec='red', linewidth=4)
            ax.text(image_pos, image_height - 0.8, '实像', ha='center', fontsize=12, color='red', fontweight='bold')
            image_type = "实像"
        else:
            # 虚像（绿色向上箭头）
            image_pos = lens_pos + image_distance
            image_height = object_height * magnification
            ax.arrow(image_pos, 0, 0, image_height, head_width=0.4, head_length=0.4, 
                    fc='green', ec='green', linewidth=4)
            ax.text(image_pos, image_height + 0.8, '虚像', ha='center', fontsize=12, color='green', fontweight='bold')
            image_type = "虚像"
        
        # 绘制三条主光线
        # 光线1：平行于主轴 → 通过焦点
        ax.plot([object_pos, lens_pos], [object_height, object_height], 'b--', alpha=0.8, linewidth=2)
        if image_distance > 0:
            ax.plot([lens_pos, image_pos], [object_height, image_height], 'r--', alpha=0.8, linewidth=2)
        else:
            ax.plot([lens_pos, image_pos], [object_height, image_height], 'g--', alpha=0.8, linewidth=2)
        
        # 光线2：通过光心直线传播
        ax.plot([object_pos, image_pos], [object_height, image_height], 'k:', alpha=0.8, linewidth=2)
        
        # 光线3：通过焦点 → 平行于主轴
        if self.object_distance > self.focal_length:
            ax.plot([object_pos, f_left], [object_height, 0], 'b--', alpha=0.8, linewidth=2)
            ax.plot([f_right, lens_pos], [0, object_height], 'r--', alpha=0.8, linewidth=2)
        
        # 标注距离
        # 物距标注
        ax.annotate('', xy=(object_pos/2, -1.5), xytext=(object_pos/2, -2.5),
                   arrowprops=dict(arrowstyle='<->', color='blue', lw=2))
        ax.text(object_pos/2, -3, f'd₀={self.object_distance:.1f}cm', 
               ha='center', fontsize=10, color='blue', fontweight='bold')
        
        # 像距标注
        if image_distance > 0:
            ax.annotate('', xy=((lens_pos + image_pos)/2, -1.5), xytext=((lens_pos + image_pos)/2, -2.5),
                       arrowprops=dict(arrowstyle='<->', color='red', lw=2))
            ax.text((lens_pos + image_pos)/2, -3, f'dᵢ={image_distance:.1f}cm', 
                   ha='center', fontsize=10, color='red', fontweight='bold')
        
        # 显示成像信息
        info_text = f"""成像信息：
放大率: m = {magnification:.2f}
像的类型: {image_type}
像的大小: {'放大' if magnification > 1 else '缩小'}
像的倒正: {'倒立' if image_distance > 0 else '正立'}"""
        
        ax.text(-18, 6, info_text, bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow"), 
               fontsize=10, verticalalignment='top')
    
    def plot_imaging_chart(self):
        """绘制成像规律图表"""
        ax = self.ax_chart
        
        # 设置坐标系
        ax.set_xlim(0, 25)
        ax.set_ylim(0, 25)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title('成像区域图', fontsize=12)
        ax.set_xlabel('物距 d₀ (cm)')
        ax.set_ylabel('像距 dᵢ (cm)')
        
        # 特殊点
        f = self.focal_length
        f2 = 2 * f
        
        # 绘制分界线
        ax.axvline(x=f, color='red', linestyle=':', alpha=0.8, linewidth=2, label=f'焦点 f={f:.1f}')
        ax.axvline(x=f2, color='orange', linestyle=':', alpha=0.8, linewidth=2, label=f'2f点={f2:.1f}')
        ax.axhline(y=f, color='red', linestyle=':', alpha=0.8, linewidth=2)
        ax.axhline(y=f2, color='orange', linestyle=':', alpha=0.8, linewidth=2)
        
        # 绘制成像曲线
        do_range = np.linspace(0.5, 20, 300)
        di_values = []
        
        for do in do_range:
            di = self.lens_formula(do, f)
            if abs(di) < 30:
                di_values.append(di)
            else:
                di_values.append(np.nan)
        
        di_array = np.array(di_values)
        valid_mask = ~np.isnan(di_array)
        
        # 实像区域（蓝色实线）
        real_mask = (di_array > 0) & valid_mask
        if np.any(real_mask):
            ax.plot(do_range[real_mask], di_array[real_mask], 'b-', linewidth=3, label='实像')
        
        # 虚像区域（绿色虚线）
        virtual_mask = (di_array < 0) & valid_mask
        if np.any(virtual_mask):
            ax.plot(do_range[virtual_mask], -di_array[virtual_mask], 'g--', linewidth=3, label='虚像')
        
        # 当前点（红色圆点）
        current_di = self.lens_formula(self.object_distance, f)
        if abs(current_di) < 25:
            ax.plot(self.object_distance, abs(current_di), 'ro', markersize=12, 
                   markeredgecolor='darkred', markeredgewidth=2, label='当前位置')
            
            # 标注放大率
            mag = abs(current_di / self.object_distance)
            ax.annotate(f'放大率 m={mag:.2f}', xy=(self.object_distance, abs(current_di)), 
                       xytext=(self.object_distance+2, abs(current_di)+2),
                       arrowprops=dict(arrowstyle='->', color='black', lw=1.5), 
                       fontsize=11, fontweight='bold', 
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow"))
        
        # 区域标注
        ax.text(f2 + 1, f2 - 2, '放大实像区域', fontsize=10, color='blue', fontweight='bold')
        ax.text(f + 1, f + 1, '缩小实像区域', fontsize=10, color='blue', fontweight='bold')
        ax.text(1, f + 1, '放大虚像区域', fontsize=10, color='green', fontweight='bold')
        
        ax.legend(loc='upper right', fontsize=10)
        
        # 成像规律说明
        rules_text = """成像规律：
• u > 2f：倒立缩小实像
• u = 2f：倒立等大实像
• f < u < 2f：倒立放大实像
• u = f：不成像
• u < f：正立放大虚像"""
        
        ax.text(13, 3, rules_text, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcyan"), 
               fontsize=9)
    
    def reset_parameters(self, event):
        """重置参数"""
        self.f_slider.reset()
        self.d_slider.reset()
    
    def animate_focal_change(self, event):
        """动画演示焦距变化"""
        import time
        
        # 禁用按钮
        self.animate_button.label.set_text('演示中...')
        self.animate_button.color = 'lightgray'
        self.fig.canvas.draw_idle()
        
        # 保存原始值
        original_f = self.focal_length
        original_d = self.object_distance
        
        # 动画序列
        focal_values = np.linspace(1, 15, 60)
        
        for i, f in enumerate(focal_values):
            # 更新焦距滑块
            self.f_slider.set_val(f)
            
            # 稍微延迟以便观察
            time.sleep(0.05)
            
            # 处理GUI事件
            self.fig.canvas.flush_events()
        
        # 恢复原始参数
        self.f_slider.set_val(original_f)
        self.d_slider.set_val(original_d)
        
        # 恢复按钮
        self.animate_button.label.set_text('动画演示')
        self.animate_button.color = 'lightblue'
        self.fig.canvas.draw_idle()

def main():
    """主函数"""
    print("凸透镜成像拖动可视化程序")
    print("=" * 40)
    print("操作说明：")
    print("🖱️  拖动下方滑块调节焦距和物距")
    print("🔄 点击'重置'恢复默认参数") 
    print("🎬 点击'动画演示'观看焦距变化效果")
    print("📊 左侧显示光学示意图，右侧显示成像规律")
    print("=" * 40)
    
    try:
        # 启动可视化程序
        visualizer = DragLensVisualizer()
        
    except Exception as e:
        print(f"程序运行出错: {e}")
        print("\n请确保已安装必要的库：")
        print("pip install matplotlib numpy")

if __name__ == "__main__":
    main()