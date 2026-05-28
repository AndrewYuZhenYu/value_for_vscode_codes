import time
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def get_all_zhenti_urls(driver, list_url):
    """第一阶段：抓取链接"""
    print(f"🚀 正在通过您现有的浏览器读取目录页: {list_url}")
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

def scrape_single_page(driver, url, output_dir):
    """第二阶段：接管并抓取单个页面"""
    safe_name = re.sub(r'https?://[^/]+/cet6/', '', url)
    safe_name = re.sub(r'[\\/:*?"<>|]', '_', safe_name)
    
    filename = os.path.join(output_dir, f"{safe_name}.txt")
    
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        print(f"⏭️ 真题 [{safe_name}] 已经下载过，跳过。")
        return

    print(f"\n📖 正在爬取真题: {safe_name} -> {url}")
    driver.get(url)
    
    try:
        # 增加一点等待时间，防止网络波动
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "textLayer"))
        )
        
        # 自动滚动
        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(8): 
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
        # 抓取 <aword> 标签
        word_elements = driver.find_elements(By.TAG_NAME, "aword")
        words = [el.text.strip().lower() for el in word_elements if el.text.strip()]
        
        if words:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(" ".join(words))
            print(f"💾 成功保存 {len(words)} 个单词到 {filename}")
        else:
            print(f"⚠️ 页面加载成功，但该试卷可能需要更高权限或无文本（尝试手动在网页上点选个单词看看？）。")
            
    except Exception as e:
        print(f"❌ 爬取失败，当前页面可能被拦截或加载超时。")

def main():
    output_dir = "cet6_zhenti_data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 【核心修改】告诉 Selenium 不要新建浏览器，而是去连接端口为 9222 的已有浏览器
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        list_url = "https://zhenti.burningvocabulary.cn/cet6"
        all_urls = get_all_zhenti_urls(driver, list_url)
        
        if not all_urls:
            print("❌ 未获取到任何真题链接。")
            return
            
        print("\n🤖 开始全自动化批量下载...")
        for index, url in enumerate(all_urls, 1):
            print(f"\n进度: [{index}/{len(all_urls)}]")
            scrape_single_page(driver, url, output_dir)
            time.sleep(3) # 保持温柔的抓取频率
            
        print(f"\n🎉 所有真题下载完毕！")
        
    except Exception as e:
        print(f"全局运行出错: {e}")
    # 注意：这里去掉了 driver.quit()，这样爬虫结束或崩溃后，你的 Chrome 浏览器不会被强行关闭。

if __name__ == "__main__":
    main()