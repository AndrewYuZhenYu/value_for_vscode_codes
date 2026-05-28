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
    pyperclip.copy("") 
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.6)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.8)
    return pyperclip.paste()

def merge_chunks(chunks):
    seen_lines = {}
    for chunk in chunks:
        lines = chunk.split('\n')
        for line in lines:
            clean_line = line.strip()
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
    
    # 自动断点续爬
    if os.path.exists(filename) and os.path.getsize(filename) > 3000:
        print(f"⏭️ 真题 [{safe_name}] 已经存在，跳过。")
        return

    print(f"\n📖 正在进行三段物理拼图抓取: {safe_name}")
    driver.get(url)
    time.sleep(4) 

    try:
        driver.switch_to.window(driver.current_window_handle)
        time.sleep(0.5)
        text_chunks = []

        print("⌨️  正在抓取【前半部分】...")
        text_chunks.append(rpa_copy_action())

        print("⌨️  正在翻页，抓取【中间部分】...")
        for _ in range(4):
            pyautogui.press('pagedown')
            time.sleep(0.4)
        text_chunks.append(rpa_copy_action())

        print("⌨️  正在直达底部，抓取【后半部分】...")
        pyautogui.hotkey('ctrl', 'end') if os.name == 'nt' else pyautogui.press('end')
        time.sleep(1)
        text_chunks.append(rpa_copy_action())

        pyautogui.hotkey('ctrl', 'home')
        pyautogui.press('down')

        final_text = merge_chunks(text_chunks)

        if len(final_text) > 3000:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(final_text)
            print(f"💾 🎉【拼图落盘成功！】-> {filename}")
        else:
            print(f"⚠️ 拼接后字数依然偏少（{len(final_text)}字）。")

    except Exception as e:
        print(f"❌ 运行出错: {e}")

def main():
    # ─── 🚀 动态定位：自动寻找 scripts 旁边的 data/origin ───
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.abspath(os.path.join(current_script_dir, "..", "data", "origin"))
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        list_url = "https://zhenti.burningvocabulary.cn/cet6"
        all_urls = get_all_zhenti_urls(driver, list_url)
        
        print("\n🤖 启动物理 RPA 拼图流抓取...")
        for index, url in enumerate(all_urls, 1):
            print(f"\n进度: [{index}/{len(all_urls)}]")
            scrape_single_page_puzzle(driver, url, output_dir)
            time.sleep(2)
            
        print(f"\n🎉 原始真题数据搬运完毕！")
    finally:
        pass

if __name__ == "__main__":
    main()