from ultralytics import YOLO

# 在 Windows 系统下调用多核多线程训练，必须加上这句 if __name__ == '__main__':
if __name__ == '__main__':
    print("🚀 正在加载轻量级 YOLOv8 底座...")
    # 第一次运行会自动下载 yolov8n.pt，大概只有 6MB
    model = YOLO("yolov8n.pt")

    print("🧠 开始训练！请观察下方进度条，等待 50 轮 (Epochs) 跑完...")
    # 开始训练！参数说明：
    # data: 配置文件路径
    # epochs: 学习 50 遍
    # imgsz: 图片压缩到 640 像素进行学习（防止显存爆炸）
    # batch: 每次送入 8 张图（拯救者的显卡毫无压力）
    results = model.train(data="config.yaml", epochs=50, imgsz=640, batch=8)

    print("✅ 训练完美结束！你的专属模型已生成在 runs/detect/train/weights/best.pt")