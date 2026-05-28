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

def scrape_single_page_keyboard_only(driver, url, output_dir):
    safe_name = re.sub(r'https?://[^/]+/cet6/', '', url)
    safe_name = re.sub(r'[\\/:*?"<>|]', '_', safe_name)
    filename = os.path.join(output_dir, f"{safe_name}.txt")
    
    # 断点续爬：如果文件已经存在且有内容，跳过
    if os.path.exists(filename) and os.path.getsize(filename) > 500:
        print(f"⏭️ 真题 [{safe_name}] 已存在，跳过。")
        return

    print(f"\n📖 正在纯键盘流处理: {safe_name}")
    driver.get(url)
    time.sleep(4) # 给页面 4 秒的充足加载时间

    pyperclip.copy("") # 每次开始前清空系统剪贴板

    try:
        # 【核心修改】：绝对不动鼠标！通过 Selenium 强行置顶并聚焦当前窗口
        driver.switch_to.window(driver.current_window_handle)
        time.sleep(0.5)

        # 1. 第一步：全选 (Ctrl + A)
        print("⌨️  第一步：键盘全选 (Ctrl+A)...")
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.8) 

        # 2. 第二步：键盘复制 (Ctrl + C)
        print("⌨️  第二步：键盘复制 (Ctrl+C)...")
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(1.2) # 留足时间写入系统内存

        # 3. 第三步：读取剪贴板并粘贴进文件
        raw_text = pyperclip.paste()
        
        # 释放变蓝的全选状态
        pyautogui.press('down')

        if len(raw_text.strip()) > 1000:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(raw_text)
            print(f"💾 第三步：成功创建并保存文本文件 -> {filename}")
        else:
            print(f"⚠️ 警告：当前页面复制字数过少（{len(raw_text.strip())}字），请确认浏览器窗口是否在最前端。")

    except Exception as e:
        print(f"❌ 运行发生错误: {e}")

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
        
        print("\n🤖 开始全自动模拟纯键盘搬运...")
        for index, url in enumerate(all_urls, 1):
            print(f"\n进度: [{index}/{len(all_urls)}]")
            scrape_single_page_keyboard_only(driver, url, output_dir)
            time.sleep(1.5) # 套题之间歇一下
            
        print(f"\n🎉 批量搬运全部完成！请查看 [{output_dir}] 文件夹！")
    finally:
        pass

if __name__ == "__main__":
    main()