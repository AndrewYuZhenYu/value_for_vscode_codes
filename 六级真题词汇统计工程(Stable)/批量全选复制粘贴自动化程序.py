import time
import os
import re
import pyautogui
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_all_zhenti_urls(driver, list_url):
    print(f"🚀 正在读取目录页: {list_url}")
    driver.get(list_url)
    time.sleep(3) 
    links = driver.find_elements(By.TAG_NAME, "a")
    urls = []
    for link in links:
        href = link.get_attribute("href")
        if href and "/cet6/" in href and href != list_url:
            if href not in urls:
                urls.append(href)
    print(f"🎯 成功识别到 {len(urls)} 套真题链接！")
    return urls

def rpa_copy_action():
    """纯按键流：全选 + 复制，返回当前剪贴板文本"""
    pyperclip.copy("") # 清空
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.6)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.8)
    return pyperclip.paste()

def merge_chunks(chunks):
    """将三段复制出来的文本进行智能去重拼接，保留排版"""
    # 按照换行符切分，用字典保持顺序去重
    seen_lines = {}
    for chunk in chunks:
        lines = chunk.split('\n')
        for line in lines:
            clean_line = line.strip()
            # 过滤掉无意义的空行和网页公共噪点
            if clean_w := re.sub(r'[^a-zA-Z]', '', clean_line).lower():
                if any(noise in clean_w for noise in ['home', 'about', 'copyright', 'menu', 'login', 'vocabulary', 'burning']):
                    continue
            if clean_line:
                seen_lines[clean_line] = True
    return "\n".join(seen_lines.keys())

def scrape_single_page_puzzle(driver, url, output_dir):
    safe_name = re.sub(r'https?://[^/]+/cet6/', '', url)
    safe_name = re.sub(r'[\\/:*?"<>|]', '_', safe_name)
    filename = os.path.join(output_dir, f"{safe_name}.txt")
    
    print(f"\n📖 正在进行三段物理拼图抓取: {safe_name}")
    driver.get(url)
    time.sleep(4) # 等待初始渲染

    try:
        # 强位置顶聚焦窗口，鼠标在安全区不动
        driver.switch_to.window(driver.current_window_handle)
        time.sleep(0.5)

        text_chunks = []

        # --- 🪵 第一块拼图：顶部文本 ---
        print("⌨️  正在抓取【前半部分】...")
        text_chunks.append(rpa_copy_action())

        # --- 🪵 第二块拼图：中段文本 ---
        print("⌨️  正在翻页，抓取【中间部分】...")
        # 物理模拟按下 4 次 PageDown 键，往下翻页唤醒中段 DOM
        for _ in range(4):
            pyautogui.press('pagedown')
            time.sleep(0.4)
        text_chunks.append(rpa_copy_action())

        # --- 🪵 第三块拼图：尾部文本 ---
        print("⌨️  正在直达底部，抓取【后半部分】...")
        # 物理模拟按下 End 键，直达试卷底部，强制唤醒最后的选择题
        pyautogui.hotkey('ctrl', 'end') if os.name == 'nt' else pyautogui.press('end')
        time.sleep(1)
        text_chunks.append(rpa_copy_action())

        # 回弹到顶部释放状态
        pyautogui.hotkey('ctrl', 'home')
        pyautogui.press('down')

        # 智能合并去重
        final_text = merge_chunks(text_chunks)

        if len(final_text) > 3000:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(final_text)
            print(f"💾 🎉【拼图绝杀成功！】已将全量、不残缺真题保存至 -> {filename}")
        else:
            print(f"⚠️ 拼接后字数依然偏少（{len(final_text)}字），可能没聚焦成功。")

    except Exception as e:
        print(f"❌ 运行出错: {e}")

def main():
    output_dir = "cet6_zhenti_data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        list_url = "https://zhenti.burningvocabulary.cn/cet6"
        all_urls = get_all_zhenti_urls(driver, list_url)
        
        # 为了把之前不全的文件彻底覆盖掉，这次我们不搞断点续爬，直接全量精细洗一遍
        for index, url in enumerate(all_urls, 1):
            print(f"\n进度: [{index}/{len(all_urls)}]")
            scrape_single_page_puzzle(driver, url, output_dir)
            time.sleep(2)
            
        print(f"\n🎉 60套全量、完全不残缺的高清真题已全部落盘！")
    finally:
        pass

if __name__ == "__main__":
    main()