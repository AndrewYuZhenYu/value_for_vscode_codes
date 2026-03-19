import numpy as np
import matplotlib.pyplot as plt

def boat_crossing_simulation():
    print("=== 小船过河物理仿真参数输入 ===")
    
    # 1. 参数输入
    try:
        width = float(input("请输入河宽 (m): ") or 100)
        v_river = float(input("请输入水流速度 (m/s): ") or 3)
        v_boat = float(input("请输入小船在静水中的速度 (m/s): ") or 5)
        angle_deg = float(input("请输入船头与河岸垂直方向的夹角 (度, 上游偏转为正): ") or 0)
    except ValueError:
        print("输入错误，请使用数字。")
        return

    # 2. 物理计算 (弧度制)
    angle_rad = np.radians(angle_deg)
    
    # 速度分解
    # v_x 是平行于河岸的速度 (正向为下游)
    # v_y 是垂直于河岸的速度 (指向对岸)
    v_boat_x = -v_boat * np.sin(angle_rad)  # 向上游偏则减小水平速度
    v_boat_y = v_boat * np.cos(angle_rad)
    
    v_final_x = v_river + v_boat_x
    v_final_y = v_boat_y
    
    if v_final_y <= 0:
        print("错误：船速分量无法到达对岸（角度太大或速度太小）")
        return

    # 计算结果
    time_taken = width / v_final_y
    drift_distance = v_final_x * time_taken
    total_distance = np.sqrt(width**2 + drift_distance**2)
    v_total = np.sqrt(v_final_x**2 + v_final_y**2)

    # 3. 打印分析报告
    print("\n" + "="*30)
    print(f"物理分析报告：")
    print(f"  - 过河时间: {time_taken:.2f} 秒")
    print(f"  - 沿岸偏移位移: {drift_distance:.2f} 米 ({'下游' if drift_distance > 0 else '上游'})")
    print(f"  - 实际行驶总路程: {total_distance:.2f} 米")
    print(f"  - 实际合速度大小: {v_total:.2f} m/s")
    print("="*30)

    # 4. 绘图仿真
    plt.figure(figsize=(10, 5))
    
    # 画河岸
    plt.axhline(0, color='black', linewidth=2)
    plt.axhline(width, color='black', linewidth=2)
    plt.fill_between([min(0, drift_distance)-20, max(0, drift_distance)+20], 0, width, color='skyblue', alpha=0.3)

    # 画速度矢量图 (起始点)
    plt.quiver(0, 0, v_river, 0, angles='xy', scale_units='xy', scale=1, color='blue', label='水流速度')
    plt.quiver(0, 0, v_boat_x, v_boat_y, angles='xy', scale_units='xy', scale=1, color='red', label='船头方向(静水速)')
    plt.quiver(0, 0, v_final_x, v_final_y, angles='xy', scale_units='xy', scale=1, color='green', label='合速度方向')

    # 画实际路径
    plt.plot([0, drift_distance], [0, width], 'g--', label='预期行驶轨迹')
    plt.scatter([drift_distance], [width], color='green', marker='X') # 到达点

    # 设置图表
    plt.title(f"小船过河仿真 (角度: {angle_deg}°, 时间: {time_taken:.1f}s)")
    plt.xlabel("沿岸位移 (m)")
    plt.ylabel("河宽位移 (m)")
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    
    print("\n正在生成轨迹图...")
    plt.show()

if __name__ == "__main__":
    boat_crossing_simulation()