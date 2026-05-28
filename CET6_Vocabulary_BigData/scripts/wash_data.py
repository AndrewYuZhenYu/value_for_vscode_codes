import os
import re

def clean_text_content(raw_text):
    lines = raw_text.split('\n')
    cleaned_lines = []
    
    exact_noise_lines = {'升级付费版', '自动缩放', 'player settings', '安装app', '生词本'}
    
    for line in lines:
        strip_line = line.strip()
        if not strip_line:
            cleaned_lines.append("")
            continue
        if strip_line.lower() in exact_noise_lines:
            continue
        if re.match(r'^第\s*\d+\s*页$', strip_line):
            continue
        if strip_line == 'i':
            continue
            
        processed_line = re.sub(r'\d{2}:\d{2}', '', line)
        cleaned_lines.append(processed_line)

    result_text = "\n".join(cleaned_lines)
    result_text = re.sub(r'\n{3,}', '\n\n', result_text)
    return result_text.strip()

def main():
    # ─── 🚀 动态定位：自动计算输入输出文件夹 ───
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.abspath(os.path.join(current_script_dir, "..", "data", "origin"))
    output_dir = os.path.abspath(os.path.join(current_script_dir, "..", "data", "cleaned"))
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    if not os.path.exists(input_dir):
        print(f"❌ 找不到输入源文件夹: [{input_dir}]")
        return

    all_files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    print(f"📂 找到 {len(all_files)} 个真题文件，开始批量动态清洗...")

    success_count = 0
    for file_name in all_files:
        src_path = os.path.join(input_dir, file_name)
        dst_path = os.path.join(output_dir, file_name)
        try:
            with open(src_path, 'r', encoding='utf-8') as f:
                raw_content = f.read()
            
            clean_content = clean_text_content(raw_content)
            
            with open(dst_path, 'w', encoding='utf-8') as f:
                f.write(clean_content)
            success_count += 1
        except Exception as e:
            print(f"❌ 过滤 {file_name} 失败: {e}")

    print(f"\n🎉 批量动态清洗结束！成功处理 {success_count} 个文件。存放在: [{output_dir}]")

if __name__ == "__main__":
    main()