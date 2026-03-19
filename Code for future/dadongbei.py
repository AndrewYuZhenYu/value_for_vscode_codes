import folium
from folium import plugins
import webbrowser
import os

# ==========================================
# 1. 欧亚大陆关键枢纽坐标 (模拟真实行进路线)
# 路线逻辑：莫斯科 -> 喀山 -> 叶卡捷琳堡 (进入亚洲) -> 新西伯利亚 -> 
# 伊尔库茨克 (贝加尔湖) -> 赤塔 -> 哈巴罗夫斯克 (伯力) -> 乌苏里斯克 (双城子) -> 豆满江 (入朝) -> 平壤
# ==========================================

eurasia_route = [
    [55.7558, 37.6173],   # 莫斯科 (Moscow)
    [55.7887, 49.1221],   # 喀山 (Kazan)
    [56.8389, 60.6057],   # 叶卡捷琳堡 (Yekaterinburg) - 欧亚分界
    [55.0084, 82.9357],   # 新西伯利亚 (Novosibirsk)
    [56.5010, 84.9924],   # 托木斯克附近
    [52.2870, 104.2810],  # 伊尔库茨克 (Irkutsk) - 贝加尔湖畔
    [52.0317, 113.5009],  # 赤塔 (Chita)
    [48.4725, 135.0577],  # 哈巴罗夫斯克 / 伯力 (Khabarovsk)
    [43.7995, 131.9540],  # 乌苏里斯克 / 双城子 (Ussuriysk)
    [42.4285, 130.6415],  # 哈桑 (Khasan) - 俄朝边界
    [40.1130, 127.4900],  # 咸兴 (Hamhung)
    [39.0392, 125.7625]   # 平壤 (Pyongyang)
]

def create_eurasia_map():
    print("正在构建跨越欧亚大陆的真实路线图...")

    # 1. 创建地图，初始视角定在欧亚中心
    m = folium.Map(
        location=[50.0, 100.0], 
        zoom_start=3, 
        control_scale=True,
        tiles=None
    )

    # 2. 添加卫星图层和标签层
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='高清卫星影像',
        overlay=False,
        control=True
    ).add_to(m)

    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='边界与城市标签',
        overlay=True,
        control=True
    ).add_to(m)

    # 3. 标记起点 (莫斯科) 与 终点 (平壤)
    folium.Marker(
        location=eurasia_route[0],
        popup='<b>起点：莫斯科 (Moscow)</b>',
        icon=folium.Icon(color='red', icon='university', prefix='fa')
    ).add_to(m)

    folium.Marker(
        location=eurasia_route[-1],
        popup='<b>终点：平壤 (Pyongyang)</b>',
        icon=folium.Icon(color='red', icon='star', prefix='fa')
    ).add_to(m)

    # 4. 标记关键节点 (如贝加尔湖、欧亚分界点)
    key_points = {
        2: "叶卡捷琳堡 (欧亚分界线)",
        5: "伊尔库茨克 (贝加尔湖)",
        9: "俄朝图们江大桥"
    }
    for idx, label in key_points.items():
        folium.CircleMarker(
            location=eurasia_route[idx],
            radius=5,
            color='cyan',
            fill=True,
            popup=label
        ).add_to(m)

    # 5. 绘制动态动画路线
    # 使用红色半透明蚂蚁线，模拟长途跋涉的视觉感
    plugins.AntPath(
        locations=eurasia_route,
        weight=4,
        color='red',
        pulse_color='yellow',
        delay=1500,
        dash_array=[10, 20],
        opacity=0.8,
        tooltip='莫斯科 - 平壤 跨国铁路线'
    ).add_to(m)

    # 6. 增强功能：添加小地图、全屏和鼠标坐标显示
    plugins.MiniMap(toggle_display=True, position='bottomright').add_to(m)
    plugins.Fullscreen().add_to(m)
    plugins.MousePosition().add_to(m) # 方便查看经纬度

    # 7. 保存并自动打开
    output_file = 'moscow_pyongyang_route.html'
    m.save(output_file)
    print(f"地图已生成: {output_file}")
    
    file_path = os.path.realpath(output_file)
    webbrowser.open(f'file://{file_path}')

if __name__ == "__main__":
    create_eurasia_map()