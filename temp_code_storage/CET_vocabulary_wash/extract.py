import os
from pypdf import PdfReader

def stream_extract_pdf_to_txt(pdf_path, txt_path):
    print("🚀 开始流式提取文本，请稍候...")
    
    if not os.path.exists(pdf_path):
        print(f"❌ 错误：找不到文件 {pdf_path}，请检查路径是否正确。")
        return

    # 1. 初始化 PDF 读取器
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    print(f"📚 成功加载 PDF，总计 {total_pages} 页。")
    
    # 2. 采用流式写入模式 ('w')，逐页读取即时写入磁盘，彻底杜绝卡死
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        for page_num in range(total_pages):
            try:
                page = reader.pages[page_num]
                # 提取当前页的底层 OCR 文本
                text = page.extract_text()
                
                # 写入页码锚点和文本内容
                txt_file.write(f"\n\n--- PAGE {page_num + 1} ---\n")
                if text:
                    txt_file.write(text)
                else:
                    txt_file.write("[本页未提取到文本]")
                
                # 每 100 页打印一次进度
                if (page_num + 1) % 100 == 0 or (page_num + 1) == total_pages:
                    print(f"⏳ 已完成: {page_num + 1}/{total_pages} 页...")
                    
            except Exception as e:
                print(f"⚠️ 第 {page_num + 1} 页提取时发生轻微错误（可能就是你提到的那一两页问题）: {e}")
                txt_file.write(f"\n\n--- PAGE {page_num + 1} 提取失败 ---\n")
                continue
                
    print(f"\n🎉 大功告成！纯文本已完美保存至: {txt_path}")

if __name__ == "__main__":
    # 📝 请在这里填写你 OCR 成功的 PDF 文件名（如果在同一目录下）
    # 或者填写绝对路径，例如 "D:/CET6/my_ocr_file.pdf"
    INPUT_PDF ="（2015.6-2025.12）六级考试所有真题集合.pdf" 
    # INPUT_PDF = "CET_vocabulary_wash/(2015.6-2025.12) 六级考试所有真题集合.pdf"
    OUTPUT_TXT = "六级真题_raw.txt"
    
    stream_extract_pdf_to_txt(INPUT_PDF, OUTPUT_TXT)