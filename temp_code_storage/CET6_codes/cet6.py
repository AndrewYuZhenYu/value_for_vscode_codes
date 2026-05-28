import pdfplumber
import json
import re
import os

def solve_file_not_found():
    # 1. 自动获取当前脚本所在的目录
    current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
    print(f"当前搜索目录: {current_dir}")

    # 2. 自动寻找 PDF 文件 (模糊匹配“六级”和“pdf”)
    target_pdf = None
    for file in os.listdir(current_dir):
        if "六级" in file and file.endswith(".pdf"):
            target_pdf = os.path.join(current_dir, file)
            break
    
    if not target_pdf:
        print("❌ 错误：在当前目录下没找到包含‘六级’字样的 PDF 文件！")
        print(f"当前目录下的文件有: {os.listdir(current_dir)}")
        return

    print(f"✅ 找到目标文件: {os.path.basename(target_pdf)}")
    
    # 3. 开始执行提取逻辑
    extract_and_clean_words(target_pdf, "cet6_vocabulary.json")

def extract_and_clean_words(pdf_path, json_output_path):
    word_list = []
    current_entry = None
    index_pattern = re.compile(r'^\d+\.\s*')

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                table = page.extract_table(table_settings={
                    "vertical_strategy": "lines", 
                    "horizontal_strategy": "lines",
                    "snap_y_tolerance": 4,
                })
                
                if not table: continue
                    
                for row in table:
                    if not any(row) or len(row) < 3: continue
                    
                    raw_word = str(row[0] or "").strip()
                    col_phonetic = str(row[1] or "").strip()
                    col_def = str(row[2] or "").strip()

                    if "单词" in raw_word: continue

                    if raw_word:
                        clean_word = index_pattern.sub('', raw_word)
                        current_entry = {
                            "word": clean_word.replace('\n', ''),
                            "phonetic": col_phonetic.replace('\n', ''),
                            "definition": col_def.replace('\n', ' ')
                        }
                        word_list.append(current_entry)
                    elif current_entry:
                        if col_phonetic: current_entry["phonetic"] += col_phonetic.replace('\n', '')
                        if col_def: current_entry["definition"] += " " + col_def.replace('\n', ' ')
                
                if (i + 1) % 5 == 0:
                    print(f"已处理 {i+1} 页...")

        # 清洗并保存
        for entry in word_list:
            entry["definition"] = " ".join(entry["definition"].split())

        with open(json_output_path, 'w', encoding='utf-8') as f:
            json.dump(word_list, f, ensure_ascii=False, indent=4)
        
        print(f"\n✨ 成功提取 {len(word_list)} 个单词！")
        print(f"📂 JSON 已保存至: {json_output_path}")

    except Exception as e:
        print(f"解析过程中出错: {e}")

if __name__ == "__main__":
    solve_file_not_found()