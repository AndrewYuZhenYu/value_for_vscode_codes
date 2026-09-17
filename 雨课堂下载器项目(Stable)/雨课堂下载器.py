import os
import time
import shutil
import img2pdf
from playwright.sync_api import sync_playwright

# ================= 固定配置区域 =================
# 本地缓存目录，用于持久化保存登录状态（不需要每次都输入）
USER_DATA_DIR = "./yuketang_login_cache"
# ==========================================

def main():
    print("=====================================================")
    print(" 🚀 雨课堂课件自动化下载器 (交互最终版)")
    print("=====================================================")
    
    # 让用户交互式输入核心配置
    COURSE_URL = input("👉 请输入课件的网址 (回车确认): ").strip()
    if not COURSE_URL:
        print("❌ 网址不能为空，程序退出！")
        return
        
    SAVE_DIR = input("👉 请输入截图保存文件夹名称 (直接回车默认用 './yuketang_temp'): ").strip()
    if not SAVE_DIR:
        SAVE_DIR = "./yuketang_temp"
        
    OUTPUT_PDF = input("👉 请输入生成的 PDF 文件名 (直接回车默认用 '下载课件.pdf'): ").strip()
    if not OUTPUT_PDF:
        OUTPUT_PDF = "下载课件.pdf"
    
    # 确保 PDF 文件名带有后缀
    if not OUTPUT_PDF.endswith(".pdf"):
        OUTPUT_PDF += ".pdf"

    print("\n⏳ 正在启动配置，请稍候...")
    os.makedirs(SAVE_DIR, exist_ok=True)

    with sync_playwright() as p:
        # 使用持久化上下文，扫一次码，终身受益
        context = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            viewport={'width': 1920, 'height': 1080},
            args=['--force-device-scale-factor=1']
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        # timeout=0 表示禁用超时限制，直到网页真正加载出来为止
        page.goto(COURSE_URL, timeout=0)

        print("=====================================================")
        print("💡 提示：如果未登录，请扫码。如果已登录，脚本将自动开始。")
        print("=====================================================")
        
        try:
            page.wait_for_selector(".thumbImg-container", timeout=60000)
        except Exception:
            print("❌ 未能检测到课件页面，请确认登录状态或网址是否正确。")
            context.close()
            return

        thumbnails = page.locator(".thumbImg-container")
        total_pages = thumbnails.count()
        print(f"✅ 检测到 {total_pages} 页课件！开始下载...")

        # 【核心逻辑】：使用您找到的绝对路径，定点切除牛皮癣
        # 我们把父级包装器 .layout_right_switch 一并删掉，最干净
        remove_btn_js = """
            const blackBtn = document.querySelector('#app > div.viewContainer > div > section > main > div > div.basePPTMain.basePPTInline > div > div.layout_body > div.layout_right_switch');
            if (blackBtn) {
                blackBtn.remove();
            }
        """

        image_paths = []

        for i in range(total_pages):
            try:
                # 翻页
                thumb = thumbnails.nth(i)
                thumb.scroll_into_view_if_needed()
                thumb.click()
                
                # 等待课件文字与公式渲染
                time.sleep(2.0) 

                # 在截图前的一瞬间，执行切除逻辑（防止翻页导致按钮重绘）
                page.evaluate(remove_btn_js)

                img_path = os.path.join(SAVE_DIR, f"page_{i+1:03d}.png")
                
                # 精准截取课件图层
                page.locator(".slide_layer").first.screenshot(path=img_path)
                image_paths.append(img_path)
                
                print(f"✅ 第 {i+1}/{total_pages} 页截取成功 (已移除遮挡)")
            except Exception as e:
                print(f"⚠️ 第 {i+1} 页截取异常: {e}")
                continue

        context.close()

        # 生成最终 PDF 并自动清理
        if image_paths:
            print("\n📦 正在合成 PDF 文件...")
            with open(OUTPUT_PDF, "wb") as f:
                f.write(img2pdf.convert(image_paths))
            print(f"🎊 大功告成！无遮挡课件已保存为: {OUTPUT_PDF}")
            
            # 【新增：自动清理文件夹及内部图片】
            try:
                shutil.rmtree(SAVE_DIR)
                print(f"🧹 临时图片及文件夹 '{SAVE_DIR}' 已自动清理完毕！")
            except Exception as e:
                print(f"⚠️ 清理临时文件夹失败: {e}")

if __name__ == "__main__":
    main()