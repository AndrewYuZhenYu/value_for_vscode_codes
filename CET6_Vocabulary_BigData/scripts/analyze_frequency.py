import os
import re
from collections import Counter
import pandas as pd

def load_custom_stopwords():
    paper_structure_words = {
        'section', 'directions', 'questions', 'question', 'part', 'sheet', 'passage', 
        'translation', 'writing', 'listening', 'comprehension', 'minutes', 'allowed',
        'essay', 'commenting', 'words', 'write', 'choose', 'best', 'answer', 'marked',
        'corresponding', 'letter', 'single', 'line', 'through', 'centre', 'based',
        'statements', 'attached', 'contains', 'information', 'given', 'paragraphs',
        'identify', 'paragraph', 'derived', 'once', 'view', 'illustrate', 'examples',
        'cite', 'least', 'more', 'than', 'university', 'true', 'false', 'null', 'undefined',
        'player', 'settings', 'app', 'online', 'copyright', 'home', 'about', 'menu', 'options'
    }
    
    basic_english_stopwords = {
        'the', 'a', 'an', 'and', 'to', 'of', 'in', 'is', 'that', 'it', 'for', 'you', 'are', 
        'on', 'with', 'as', 'this', 'was', 'they', 'by', 'at', 'be', 'from', 'or', 'have', 
        'your', 'not', 'he', 'she', 'but', 'their', 'will', 'about', 'his', 'her', 
        'we', 'can', 'one', 'all', 'there', 'who', 'so', 'up', 'out', 'if', 'what', 'been',
        'their', 'them', 'my', 'me', 'our', 'us', 'its', 'has', 'had', 'do', 'does', 'did',
        'were', 'would', 'could', 'should', 'theyre', 'dont', 'other', 'am', 'are', 'is'
    }
    return paper_structure_words.union(basic_english_stopwords)

def analyze_cet6_full_data():
    # ─── 🚀 动态定位：精准计算输入和最终 Excel 的输出位置 ───
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.abspath(os.path.join(current_script_dir, "..", "data", "cleaned"))
    output_excel = os.path.abspath(os.path.join(current_script_dir, "..", "cet6_full_vocabulary_frequency.xlsx"))
    
    if not os.path.exists(input_dir):
        print(f"❌ 找不到清洗后的文件夹: [{input_dir}]")
        return

    word_counter = Counter()
    stopwords = load_custom_stopwords()
    
    all_files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    print(f"📊 正在从本地 {len(all_files)} 个文本中抽取【全量】大数据词频...")

    for file_name in all_files:
        file_path = os.path.join(input_dir, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
            
            words = re.findall(r'\b[a-z-]+\b', content)
            for word in words:
                if len(word) <= 1:
                    continue
                if word in stopwords:
                    continue
                word_counter[word] += 1
        except Exception as e:
            print(f"读取文件 {file_name} 失败: {e}")

    all_words = word_counter.most_common()
    if not all_words:
        print("⚠️ 统计结束，数据为空。")
        return

    df = pd.DataFrame(all_words, columns=['核心词汇 (Word)', '全站出现总频次 (Frequency)'])
    df.insert(0, '大数据排名 (Rank)', range(1, len(df) + 1))
    
    df.to_excel(output_excel, index=False)
    print(f"\n🎉 大数据全量分析彻底完工！")
    print(f"💾 包含完整的 {len(df)} 个词汇大盘已动态保存至根目录: [{output_excel}]")

if __name__ == "__main__":
    analyze_cet6_full_data()