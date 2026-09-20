import json
import os
from pypdf import PdfReader, PdfWriter

# ================= ⚙️ 极简配置区 =================
pdf_path = r"F:\Pycharm Codes\PDF_Auto_Bookmark\data_raw\27张宇基础30讲高数_带大纲.pdf"
output_pdf_path = r"F:\Pycharm Codes\PDF_Auto_Bookmark\27张宇基础30讲最终完美版.pdf"

# 超一级的总目录名字
ROOT_TITLE = "《考研数学基础30讲 (高数分册)》"

# AI 扫出的是物理页码，默认先不加偏移。如果生成后发现依然错位，改成 5 再运行一次即可。
PAGE_OFFSET = 0
# =============================================

print("📖 正在读取 AI 识别出的全套精确目录数据...")
if not os.path.exists("toc_backup.json"):
    print("❌ 找不到 toc_backup.json，请确认它在项目根目录！")
    exit()

with open("toc_backup.json", "r", encoding="utf-8") as f:
    final_toc = json.load(f)

print("🛠️ 正在梳理层级，防止越级报错...")
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

print("💉 正在构建【超一级总纲】并注入识别目录...")
reader = PdfReader(pdf_path)
writer = PdfWriter()

# 拷贝原版页面
writer.append_pages_from_reader(reader)

# 1. 建立超一级目录 (指向物理第 0 页，封面)
root_bm = writer.add_outline_item(ROOT_TITLE, 0)

# 2. 将 0 级父亲设为 root_bm，这样 AI 扫出的 1 级标题全会完美折叠在它下面
parent_nodes = {0: root_bm}

max_index = len(reader.pages) - 1

for item in fixed_toc:
    lvl, title, page = item

    # 寻找对应的父节点
    parent_item = parent_nodes.get(lvl - 1, root_bm)

    # 加上偏移量（AI 读取的是物理页码，通常 page-1 就是正确索引）
    target_index = page - 1 + PAGE_OFFSET

    # 防越界保护
    if target_index > max_index: target_index = max_index
    if target_index < 0: target_index = 0

    # 写入书签
    bm = writer.add_outline_item(title, target_index, parent=parent_item)
    parent_nodes[lvl] = bm

print(f"📦 正在输出最终文件：{output_pdf_path}")
with open(output_pdf_path, "wb") as f:
    writer.write(f)

print("🎉 注入成功！这下所有的识别目录都被整整齐齐收编在总纲下面了！")