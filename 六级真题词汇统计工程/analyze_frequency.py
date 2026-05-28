import os
import re
from collections import Counter
import pandas as pd

def load_custom_stopwords():
    """定义需要过滤的六级结构词、网页噪点以及基础英语停用词"""
    # 1. 题干中你指定的结构词、垃圾残留以及网页固定噪点
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
    
    # 2. 英语基础极高频停用词（代词、介词、冠词、连词、基础助动词等）
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
    input_dir = "cet6_zhenti_cleaned"
    output_excel = "cet6_full_vocabulary_frequency.xlsx"
    
    if not os.path.exists(input_dir):
        print(f"❌ 找不到清洗后的文件夹 [{input_dir}]，请确认路径！")
        return

    # 初始化全局计数器
    word_counter = Counter()
    stopwords = load_custom_stopwords()
    
    all_files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    print(f"📊 正在从本地 {len(all_files)} 个文本文件中抽取【全量】大数据词频...")

    for file_name in all_files:
        file_path = os.path.join(input_dir, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
            
            # 抓取干净的英文单词流
            words = re.findall(r'\b[a-z-]+\b', content)
            
            for word in words:
                # 过滤规则 1：单独的 abcd、i、s 等所有单字母残留，强制避开
                if len(word) <= 1:
                    continue
                # 过滤规则 2：如果在我们的停用词/结构词字典里，跳过
                if word in stopwords:
                    continue
                
                word_counter[word] += 1
                
        except Exception as e:
            print(f"读取文件 {file_name} 失败: {e}")

    # 【核心调整】：彻底拿掉限制！直接提取计数器中的全部汇总词汇，并按频次从高到低排序
    all_words = word_counter.most_common()
    
    if not all_words:
        print("⚠️ 统计结束，但词盘为空，请检查输入文本内容。")
        return

    # 整理数据并落盘
    df = pd.DataFrame(all_words, columns=['核心词汇 (Word)', '全站出现总频次 (Frequency)'])
    df.insert(0, '大数据排名 (Rank)', range(1, len(df) + 1))
    
    # 导出到 Excel
    df.to_excel(output_excel, index=False)
    print(f"\n🎉 大数据全量分析彻底完工！")
    print(f"💾 包含完整的 {len(df)} 个词汇大盘已保存为: [{output_excel}]")
    print(f"💡 现在你可以打开这个 Excel，从第 1 行一口气拉到最后一页了！")

if __name__ == "__main__":
    analyze_cet6_full_data()