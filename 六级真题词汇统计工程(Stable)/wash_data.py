import os
import re

# 优化 1：将固定配置提取到全局作用域，避免每次读取文件时重复分配内存
EXACT_NOISE_LINES = {
    '升级付费版', 
    '自动缩放', 
    'player settings', 
    '安装app', 
    '生词本'
}

def clean_text_content(raw_text):
    """核心清洗函数：精细化过滤行与特定噪点"""
    
    # 优化 2：使用 splitlines() 替代 split('\n')
    # 它能自动识别并兼容 Windows(\r\n), Mac(\r), Linux(\n) 的不同换行符，防止文件因换行符差异变成“一整行”
    lines = raw_text.splitlines()
    cleaned_lines = []
    
    for line in lines:
        strip_line = line.strip()
        
        # 策略 A：跳过绝对空行
        if not strip_line:
            cleaned_lines.append("")
            continue
            
        # 策略 B：整行精确匹配噪点词（不区分大小写），符合则直接丢弃
        if strip_line.lower() in EXACT_NOISE_LINES:
            continue
            
        # 策略 C：通过正则表达式匹配动态噪点
        if re.match(r'^第\s*\d+\s*页$', strip_line):
            continue
            
        if strip_line == 'i':
            continue
            
        # 策略 D：行内细节清洗
        processed_line = re.sub(r'\d{2}:\d{2}', '', line)
        cleaned_lines.append(processed_line)

    # 重新用换行符连接
    result_text = "\n".join(cleaned_lines)
    
    # 最后的格式微调
    result_text = re.sub(r'\n{3,}', '\n\n', result_text)
    
    return result_text.strip()

def main():
    # 数据存放文件夹
    input_dir = "/Users/andrewyu/Documents/Projects/value_for_vscode_codes/value_for_vscode_codes/六级真题词汇统计工程/cet6_zhenti_data"
    output_dir = "/Users/andrewyu/Documents/Projects/value_for_vscode_codes/value_for_vscode_codes/六级真题词汇统计工程/cet6_zhenti_cleaned"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    if not os.path.exists(input_dir):
        print(f"❌ 找不到输入文件夹: [{input_dir}]，请确认路径！")
        return

    all_files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    # 优化 3：动态获取文件总数
    total_files = len(all_files) 
    print(f"📂 找到 {total_files} 个真题文本文件，开始批量清洗...")

    success_count = 0
    for file_name in all_files:
        src_path = os.path.join(input_dir, file_name)
        dst_path = os.path.join(output_dir, file_name)
        
        try:
            with open(src_path, 'r', encoding='utf-8') as f:
                raw_content = f.read()
            
            # 优化 4：源文件内容为空预警
            if not raw_content.strip():
                print(f"⚠️ 警告: 源文件 [{file_name}] 本身是空的！")
            
            # 洗涤数据
            clean_content = clean_text_content(raw_content)
            
            # 优化 5：如果源文件不为空，但清洗后变为空白，抛出警告，方便排查误杀
            if raw_content.strip() and not clean_content.strip():
                print(f"⚠️ 异常: [{file_name}] 清洗后变成了纯空白！请检查是否内容全为噪点。")
            
            # 写入新文件夹
            with open(dst_path, 'w', encoding='utf-8') as f:
                f.write(clean_content)
                
            success_count += 1
            print(f"✨ 成功清洗并导出: {file_name}")
            
        except UnicodeDecodeError:
            print(f"❌ 编码错误: [{file_name}] 不是标准的 UTF-8 编码，请检查文件格式。")
        except Exception as e:
            print(f"❌ 处理文件 [{file_name}] 时发生未知错误: {e}")

    # 替换这里写死的 60 为 total_files
    print(f"\n🎉 批量清洗战役圆满结束！共成功处理 {success_count}/{total_files} 个文件。")
    print(f"👉 请前往新生成的 [{output_dir}] 文件夹查看最纯净的高清真题！")

if __name__ == "__main__":
    main()