import fitz

def clean_pdf(input_file, output_file, target_rgb):
    doc = fitz.open(input_file)
    
    for page in doc:
        # 寻找页面上的所有绘制对象
        paths = page.get_drawings()
        for path in paths:
            color = path.get("fill")
            if color:
                # 比较颜色，考虑到浮点数精度，用 abs 差值比较
                if all(abs(c1 - c2) < 0.01 for c1, c2 in zip(color, target_rgb)):
                    # 获取该形状的矩形
                    rect = path["rect"]
                    # 在该位置画一个白色矩形挡住它
                    page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1), overlay=True)

    doc.save(output_file)
    doc.close()

# 将你测得的颜色值填入这里
my_target = (0.92549, 0.61176, 0.81569) # 举例，需替换为你测到的值
clean_pdf("input.pdf", "output.pdf", my_target)