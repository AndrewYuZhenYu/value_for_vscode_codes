import fitz  # PyMuPDF 的包名
import os

# ================= ⚙️ 配置区 =================
# 1. 替换为你的 1GB PDF 文件的真实路径
pdf_path = r"F:\Pycharm Codes\PDF_Auto_Bookmark\data_raw\27张宇基础30讲高数_带大纲.pdf"

# 2. 图片输出的目标文件夹
output_dir = "dataset/images"

# 3. 🎯 将你人工找到的页码填在下面的中括号里（用逗号隔开）
# ⚠️ 极其重要：请填写你在 PDF 阅读器顶部看到的“绝对页码”（哪怕正文上印的是第 1 页，只要阅读器显示是第 15 页，就填 15）
target_pages = [8,10,12,14,19,32,33,35,82,105,125,146,145,150,151,154,170,191,193,194,201,237,383,385,416,420,471,495,512]
# =============================================

# 如果输出文件夹不存在，自动创建
os.makedirs(output_dir, exist_ok=True)

print("🚀 正在加载巨无霸 PDF 文件，请稍候...")
try:
    doc = fitz.open(pdf_path)
except Exception as e:
    print(f"❌ 打开 PDF 失败，请检查文件路径是否正确。错误信息：{e}")
    exit()

print(f"✅ 文件加载成功！共包含 {len(doc)} 页。开始提取高清图片...")

# 遍历你提供的所有目标页码
for page_num in target_pages:
    # 程序的页码索引是从 0 开始计数的，所以我们要把你的输入减 1
    actual_index = page_num - 1

    # 防止你填错页码导致程序崩溃的安全检查
    if actual_index < 0 or actual_index >= len(doc):
        print(f"⚠️ 警告：页码 {page_num} 超出了文件的总页数，已跳过。")
        continue

    try:
        # 加载指定页面
        page = doc.load_page(actual_index)

        # 提取高清像素图，dpi=300 保证文字边缘如刀刻般锐利
        pix = page.get_pixmap(dpi=300)

        # 生成保存路径，例如 dataset/images/page_15.png
        output_filename = f"page_{page_num}.png"
        output_path = os.path.join(output_dir, output_filename)

        # 保存图片到本地
        pix.save(output_path)
        print(f"📸 提取成功：第 {page_num} 页 -> {output_filename}")

    except Exception as e:
        print(f"❌ 提取第 {page_num} 页时发生错误：{e}")

print("\n🎉 全部定向提取任务完成！现在可以把这些完美的高清图片拖进 MakeSense.ai 去画框了。")