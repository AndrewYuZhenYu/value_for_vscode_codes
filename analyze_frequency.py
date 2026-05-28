 import os
import re
from collections import Counter
import pandas as pd

def load_custom_stopwords():
    """定义需要过滤的六级结构词以及基础英语停用词"""
    # 1. 题干中你指定的结构词和垃圾残留
    paper_structure_words = {
        'section', 'directions', 'questions', 'question', 'part', 'sheet', 'passage', 
        'translation', 'writing', 'listening', 'comprehension', 'minutes', 'allowed',
        'essay', 'commenting', 'words', 'write', 'choose', 'best', 'answer', 'marked',
        'corresponding', 'letter', 'single', 'line', 'through', 'centre', 'based',
        'statements', 'attached', 'contains', 'information', 'given', 'paragraphs',
        'identify', 'paragraph', 'derived', 'once', 'view', 'illustrate', 'examples',
        'cite', 'least', 'more', 'than', 'university', 'true', 'false', 'null', 'undefined'
    }
    
    # 2. 英语基础停用词（代词、介词、冠词、连词等）
    basic_english_stopwords = {
        'the', 'a', 'an', 'and', 'to', 'of', 'in', 'is', 'that', 'it', 'for', 'you', 'are', 
        'on', 'with', 'as', 'this', 'was', 'they', 'by', 'at', 'be', 'from', 'or', 'have', 
        'your', 'not', 'he', 'she', 'but', 'their', 'will', 'an', 'about', 'his', 'her', 
        'we', 'can', 'one', 'all', 'there', 'who', 'so', 'up', 'out', 'if', 'what', 'been',
        'their', 'them', 'my', 'me', 'our', 'us', 'its', 'has', 'had', 'do', 'does', 'did',
        'were', 'would', 'could', 'should', 'their', 'theyre', 'dont', 'than', 'other', 'been'
    }
    
    # 合并所有的干扰词
    all_stopwords = paper_structure_words.union(basic_english_stopwords)
    return all_stopwords

def analyze_cet6_big_data():
    input_dir = "cet6_zhenti_cleaned"
    output_excel = "cet6_high_frequency_words.xlsx"
    
    if not os.path.exists(input_dir):
        print(f"❌ 找不到清洗后的文件夹 [{input_dir}]，请确认路径！")
        return

    # 初始化计数器
    word_counter = Counter()
    stopwords = load_custom_stopwords()
    
    # 获取文件夹内所有的清洗文本
    all_files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    print(f"📊 正在从 {len(all_files)} 个满血文本文件中抽取大数据词频...")

    for file_name in all_files:
        file_path = os.path.join(input_dir, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
            
            # 使用正则抓取连续的字母段（同时支持带着连字符的词如 rule-governed）
            words = re.findall(r'\b[a-z-]+\b', content)
            
            for word in words:
                # 过滤规则 1：单独的 abcd、i、t 等所有单字母，强制避开
                if len(word) <= 1:
                    continue
                # 过滤规则 2：如果在我们的停用词/结构词大字典里，直接枪毙
                if word in stopwords:
                    continue
                
                # 剩下的就是真正的核心高质量词汇，计入大盘
                word_counter[word] += 1
                
        except Exception as e:
            print(f"读取文件 {file_name} 失败: {e}")

    # 提取出现频次最高的前 200 个核心词汇
    top_words = word_counter.most_common(200)
    
    if not top_words:
        print("⚠️ 统计结束，但核心词盘为空，请检查输入文件是否包含英文。")
        return

    # 使用 Pandas 优雅地整理成数据表格
    df = pd.DataFrame(top_words, columns=['核心词汇 (Word)', '全站出现总频次 (Frequency)'])
    
    # 增加一列排名，看着更直观
    df.insert(0, '大数据排名 (Rank)', range(1, len(df) + 1))
    
    # 导出到 Excel
    df.to_excel(output_excel, index=False)
    print(f"\n🎉 大数据分析战役圆满结束！")
    print(f"💾 高频词频大盘已保存为: [{output_excel}]")
    
    # 在终端打印前 20 名，让你先睹为快
    print("\n🔥 抢先看：六级全站真题出现频次最高的 Top 20 核心词：")
    print(df.head(20).to_string(index=False))

if __name__ == "__main__":
    analyze_cet6_big_data()