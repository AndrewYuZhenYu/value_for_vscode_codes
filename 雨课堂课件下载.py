import os
import time
import img2pdf
from playwright.sync_api import sync_playwright

# ================= 配置区域 =================
COURSE_URL = "https://yuketang.cn/v2/web/studentCards/30205229/6989381/55471246/ppt?cid=5052732&university_id=2964&platform_id=3&classroom_id=30205229"
SAVE_DIR = "./yuketang_final_pure"
OUTPUT_PDF = "大学物理I_完美最终版.pdf"

# 本地缓存目录，用于持久化保存登录状态
USER_DATA_DIR = "./yuketang_login_cache"
# ==========================================

def main():
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
        print("如果未登录，请扫码。如果已登录，脚本将自动开始。")
        print("=====================================================")
        
        try:
            page.wait_for_selector(".thumbImg-container", timeout=60000)
        except Exception:
            print("❌ 未能检测到课件页面，请确认登录状态。")
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

                # 在截图前的一瞬间，执行您找到的切除逻辑（防止翻页导致按钮重绘）
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

        # 生成最终 PDF
        if image_paths:
            print("\n正在合成 PDF 文件...")
            with open(OUTPUT_PDF, "wb") as f:
                f.write(img2pdf.convert(image_paths))
            print(f"🎊 大功告成！无遮挡课件已保存为: {OUTPUT_PDF}")

if __name__ == "__main__":
    main()