import pandas

doc = fitz.open("概率论月考二试题（2018-2023）.pdf")
page = doc[54] # 选一张有水印的页面（索引从0开始，第55页就是54）
paths = page.get_drawings()

for i, path in enumerate(paths):
    # 打印填充颜色 (fill) 或 描边颜色 (color)
    print(f"序号: {i}, 颜色: {path.get('fill')}, 区域: {path['rect']}")