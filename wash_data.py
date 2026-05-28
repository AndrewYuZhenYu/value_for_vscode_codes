import os
import re

def clean_text_content(raw_text):
    """核心清洗函数：精细化过滤行与特定噪点"""
    lines = raw_text.split('\n')
    cleaned_lines = []
    
    # 1. 定义需要【整行直接删掉】的固定垃圾字符串字典
    # 使用 set 提高查找效率
    exact_noise_lines = {
        '升级付费版', 
        '自动缩放', 
        'player settings', 
        '安装app', 
        '生词本'
    }
    
    for line in lines:
        strip_line = line.strip()
        
        # 策略 A：跳过绝对空行
        if not strip_line:
            cleaned_lines.append("")
            continue
            
        # 策略 B：整行精确匹配噪点词（不区分大小写），符合则直接丢弃
        if strip_line.lower() in exact_noise_lines:
            continue
            
        # 策略 C：通过正则表达式匹配动态噪点
        # 匹配 "第 1 页"、"第 2 页"、"第   12  页" 等页码标识
        if re.match(r'^第\s*\d+\s*页$', strip_line):
            continue
            
        # 匹配类似于单独出现的孤立小写字母 i（通常是渲染残留的噪点行）
        if strip_line == 'i':
            continue
            
        # 策略 D：行内细节清洗（不删整行，只剃掉行内的局部时间戳）
        # 匹配形如 00:00 或 27:31 的时间戳并替换为空
        processed_line = re.sub(r'\d{2}:\d{2}', '', line)
        
        # 保持原有的缩进和内容
        cleaned_lines.append(processed_line)

    # 2. 将处理后的行重新用换行符连接
    result_text = "\n".join(cleaned_lines)
    
    # 3. 最后的格式微调：把由于删行导致的连续 3 个以上的空白行，压缩成最多 2 个空行，保持排版美观
    result_text = re.sub(r'\n{3,}', '\n\n', result_text)
    
    return result_text.strip()

def main():
    # 你的数据存放文件夹
    input_dir = "cet6_zhenti_data"
    # 洗干净后的数据存放文件夹（分开存放，防止把好不容易抓来的原文件改坏）
    output_dir = "cet6_zhenti_cleaned"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    if not os.path.exists(input_dir):
        print(f"❌ 找不到输入文件夹: [{input_dir}]，请确认路径！")
        return

    # 遍历获取 60 个文件
    all_files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    print(f"📂 找到 {len(all_files)} 个真题文本文件，开始批量清洗...")

    success_count = 0
    for file_name in all_files:
        src_path = os.path.join(input_dir, file_name)
        dst_path = os.path.join(output_dir, file_name)
        
        try:
            # 读取原始文本
            with open(src_path, 'r', encoding='utf-8') as f:
                raw_content = f.read()
            
            # 洗涤数据
            clean_content = clean_text_content(raw_content)
            
            # 写入新文件夹
            with open(dst_path, 'w', encoding='utf-8') as f:
                f.write(clean_content)
                
            success_count += 1
            print(f"✨ 成功清洗并导出: {file_name}")
            
        except Exception as e:
            print(f"❌ 处理文件 {file_name} 时发生错误: {e}")

    print(f"\n🎉 批量清洗战役圆满结束！共成功处理 {success_count}/60 个文件。")
    print(f"👉 请前往新生成的 [{output_dir}] 文件夹查看最纯净的高清真题！")

if __name__ == "__main__":
    main()