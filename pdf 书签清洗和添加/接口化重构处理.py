import fitz  # PyMuPDF
import os

# ==============================================================
# ⬇️ 接口配置区：以后每次只需要在这里修改文件路径和偏移量即可 ⬇️
# ==============================================================

CONFIG = {
    # 1. 目录内容文件 (txt 或 md 格式的绝对或相对路径)
    "TOC_FILE": '/Users/andrewyu/Documents/Projects/value_for_vscode_codes/value_for_vscode_codes/pdf 书签清洗和添加/离散数学目录文件.md',
    
    # 2. 要处理的原始 PDF 路径
    "INPUT_PDF": '/Users/andrewyu/Documents/离散数学（第2版）（MACOCR）.pdf',
    
    # 3. 生成的新 PDF 路径
    "OUTPUT_PDF": '/Users/andrewyu/Documents/Projects/value_for_vscode_codes/value_for_vscode_codes/pdf 书签清洗和添加/离散数学最终版本.pdf',
    
    # 4. 页码偏移量：书面页码 + OFFSET = PDF 物理页码
    "OFFSET": 10
}

# ==============================================================
# ⬆️ 配置结束，下方核心代码无需修改 ⬆️
# ==============================================================


def update_pdf_toc_from_file(input_pdf, output_pdf, toc_file, offset):
    """
    从外部文本/Markdown文件读取目录信息并写入 PDF
    """
    # 1. 检查文件是否存在
    if not os.path.exists(toc_file):
        print(f"❌ 错误: 找不到目录文件 '{toc_file}'")
        return
    if not os.path.exists(input_pdf):
        print(f"❌ 错误: 找不到 PDF 文件 '{input_pdf}'")
        return

    # 2. 解析目录数据
    print(f"正在从 '{toc_file}' 解析目录数据...")
    new_toc = []
    with open(toc_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            # 忽略空行，支持以 '#' 开头的注释行
            if not line or line.startswith('#'):
                continue
            
            parts = line.split('|')
            if len(parts) == 3:
                try:
                    level = int(parts[0].strip())
                    title = parts[1].strip()
                    book_page = int(parts[2].strip())
                    
                    # 书本页码小于 1 不处理
                    if book_page < 1:
                        continue
                    
                    actual_page = book_page + offset
                    new_toc.append([level, title, actual_page])
                except ValueError:
                    print(f"⚠️ 警告: 第 {line_num} 行格式错误(含有非数字)，已跳过 -> {line}")
            else:
                print(f"⚠️ 警告: 第 {line_num} 行格式不匹配(缺少或多出'|')，已跳过 -> {line}")

    if not new_toc:
        print("❌ 错误: 没有解析到任何有效的目录数据，请检查文件格式！")
        return

    # 3. 写入 PDF
    print("正在打开 PDF 文件...")
    try:
        doc = fitz.open(input_pdf)
    except Exception as e:
        print(f"❌ 打开 PDF 失败: {e}")
        return
    
    print("正在清除原有的目录...")
    doc.set_toc([])
    
    print(f"准备写入 {len(new_toc)} 条新目录...")
    doc.set_toc(new_toc)

    # 4. 植入双重逻辑页码 (Page Labels)
    print("正在设置双重逻辑页码 (前言罗马数字，正文阿拉伯数字)...")
    try:
        page_labels = [
            {"startpage": 0, "style": "r", "prefix": "", "firstpagenum": 1},      # 前言部分
            {"startpage": offset, "style": "D", "prefix": "", "firstpagenum": 1}  # 正文部分
        ]
        doc.set_page_labels(page_labels)
        print("✅ 逻辑页码规则已注入")
    except Exception as e:
        print(f"⚠️ 设置 Page Labels 提示 (可忽略): {e}")

    # 5. 保存 PDF
    print(f"正在保存新的 PDF 到: '{output_pdf}'")
    try:
        doc.save(output_pdf)
        print("✅ 处理完成！")
    except Exception as e:
        print(f"❌ 保存 PDF 失败: {e}")
    finally:
        doc.close()

if __name__ == "__main__":
    # 执行主程序 (直接读取上方配置好的全局变量)
    update_pdf_toc_from_file(
        input_pdf=CONFIG["INPUT_PDF"],
        output_pdf=CONFIG["OUTPUT_PDF"],
        toc_file=CONFIG["TOC_FILE"],
        offset=CONFIG["OFFSET"]
    )