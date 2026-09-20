import fitz  # PyMuPDF
from ultralytics import YOLO
import easyocr
import numpy as np
import cv2
import json
from pypdf import PdfReader, PdfWriter

# ================= ⚙️ 配置区 =================
# 1. 你的原始 1GB PDF 路径
pdf_path = r"F:\Pycharm Codes\PDF_Auto_Bookmark\data_raw\27张宇基础30讲高数_带大纲.pdf"

# 2. 最终生成的带有完美多级目录的 PDF 路径
output_pdf_path = r"F:\Pycharm Codes\PDF_Auto_Bookmark\27张宇_最终完美版.pdf"

# 3. 你的模型路径
model_path = r"runs\detect\train-2\weights\best.pt"
# =============================================

if __name__ == '__main__':
    print("🚀 正在加载 AI 引擎...")
    model = YOLO(model_path)
    reader = easyocr.Reader(['ch_sim', 'en'], gpu=True)

    print(f"📖 正在打开大文件: {pdf_path}")
    doc = fitz.open(pdf_path)
    final_toc = []

    print(f"🔍 开始流式扫描全书，共 {len(doc)} 页...")
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # 将当前页转为图片
        pix = page.get_pixmap(dpi=200)
        img_array = np.frombuffer(pix.tobytes("png"), dtype=np.uint8)
        img_bgr = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # 视觉狙击标题
        results = model(img_bgr, verbose=False)
        boxes = results[0].boxes

        page_titles = []
        for box in boxes:
            cls_id = int(box.cls[0].item())
            level = cls_id + 1
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

            # OCR 提取文字
            crop_img = img_bgr[y1:y2, x1:x2]
            ocr_res = reader.readtext(crop_img, detail=0)
            text = " ".join(ocr_res) if ocr_res else f"未识别标题_{level}"

            page_titles.append({'y': y1, 'level': level, 'text': text})

        page_titles.sort(key=lambda x: x['y'])

        for pt in page_titles:
            final_toc.append([pt['level'], pt['text'], page_num + 1])
            print(f"  --> [第{page_num + 1}页] 发现 {pt['level']}级标题: {pt['text']}")

    # 扫描结束，释放大文件内存防止冲突
    doc.close()

    # ========================================================
    # 🌟 护城河 1：将目录数据备份到本地硬盘，防止二次白跑！
    # ========================================================
    print("\n💾 扫描完成！正在将数据备份到本地 toc_backup.json...")
    with open("toc_backup.json", "w", encoding="utf-8") as f:
        json.dump(final_toc, f, ensure_ascii=False, indent=2)

    # ========================================================
    # 🌟 护城河 2：修复越级 bug
    # ========================================================
    print("🛠️ 正在修复越级的非法目录层级...")
    fixed_toc = []
    last_level = 0
    for item in final_toc:
        lvl, title, page = item
        if not fixed_toc:
            lvl = 1
        elif lvl > last_level + 1:
            lvl = last_level + 1
        fixed_toc.append([lvl, title, page])
        last_level = lvl

    # ========================================================
    # 🌟 护城河 3：使用工业级 pypdf 进行底层重构与注入！
    # ========================================================
    print("💉 正在使用 pypdf 重构 PDF 底层目录树...")
    reader_pdf = PdfReader(pdf_path)
    writer = PdfWriter()

    # 拷贝原版所有的页面进去
    writer.append_pages_from_reader(reader_pdf)

    # 虚拟出一个根节点字典
    parent_nodes = {0: None}

    for item in fixed_toc:
        lvl, title, page = item
        # 寻找当前级别的父亲是谁
        parent_item = parent_nodes.get(lvl - 1, None)

        # 写入书签（注意：pypdf 要求页码从 0 开始，所以 page - 1）
        bm = writer.add_outline_item(title, page - 1, parent=parent_item)

        # 记录当前刚生成的节点，作为下一层小标题的父亲
        parent_nodes[lvl] = bm

    print(f"📦 正在打包生成最终文件：{output_pdf_path}")
    with open(output_pdf_path, "wb") as f:
        writer.write(f)

    print("🎉 彻底完工！这次 WPS 想不认都不行了，快去验收！")