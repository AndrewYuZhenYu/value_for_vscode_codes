from pathlib import Path
import shutil
import tempfile
import time

import img2pdf
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


# ================= 固定配置区域 =================
# 复用浏览器用户数据，保存 Cookie 等登录信息，实现下次免扫码。
USER_DATA_DIR = Path("./yuketang_login_cache")
DEFAULT_SAVE_DIR = Path("./yuketang_temp")
DEFAULT_OUTPUT_PDF = "下载课件.pdf"
# ================================================


def clean_browser_cache() -> None:
    """浏览器完全关闭后清理可重建的缓存，保留登录状态等用户数据。"""
    cache_dirs = [
        USER_DATA_DIR / "Default" / "Cache",
        USER_DATA_DIR / "Default" / "Code Cache",
        USER_DATA_DIR / "Default" / "GPUCache",
        USER_DATA_DIR / "Cache",
        USER_DATA_DIR / "Code Cache",
        USER_DATA_DIR / "GPUCache",
    ]

    for cache_dir in cache_dirs:
        if cache_dir.is_dir():
            try:
                shutil.rmtree(cache_dir)
            except OSError as exc:
                print(f"⚠️ 无法清理缓存 {cache_dir}：{exc}")


def main() -> None:
    print("=" * 53)
    print(" 🚀 雨课堂课件自动化下载器")
    print("=" * 53)

    course_url = input("👉 请输入课件的网址 (回车确认): ").strip()
    if not course_url:
        print("❌ 网址不能为空，程序退出！")
        return

    save_dir_input = input(
        "👉 请输入截图临时文件夹 (直接回车默认 './yuketang_temp'): "
    ).strip()
    save_dir = Path(save_dir_input) if save_dir_input else DEFAULT_SAVE_DIR

    output_pdf_input = input(
        "👉 请输入生成的 PDF 文件名 (直接回车默认 '下载课件.pdf'): "
    ).strip()
    output_pdf = Path(output_pdf_input or DEFAULT_OUTPUT_PDF)
    if output_pdf.suffix.lower() != ".pdf":
        output_pdf = Path(str(output_pdf) + ".pdf")

    # 保证用户给出的输出路径有可用的父目录。
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    save_dir.mkdir(parents=True, exist_ok=True)

    # 每次运行创建独立的临时子目录；只删除本次截图，不误删用户已有文件。
    with tempfile.TemporaryDirectory(prefix="capture_", dir=save_dir) as temp_dir:
        image_paths = []
        context = None

        try:
            print("\n⏳ 正在启动浏览器...")
            with sync_playwright() as p:
                context = p.chromium.launch_persistent_context(
                    user_data_dir=str(USER_DATA_DIR),
                    headless=False,
                    viewport={"width": 1920, "height": 1080},
                    args=[
                        "--force-device-scale-factor=1",
                        "--disk-cache-size=1",
                        "--media-cache-size=1",
                    ],
                )

                try:
                    page = context.pages[0] if context.pages else context.new_page()
                    page.goto(course_url, wait_until="domcontentloaded", timeout=60000)

                    print("=" * 53)
                    print("💡 未登录请在浏览器中扫码；已登录则自动开始。")
                    print("=" * 53)

                    try:
                        page.wait_for_selector(".thumbImg-container", timeout=120000)
                    except PlaywrightTimeoutError:
                        print("❌ 两分钟内未检测到课件缩略图，请检查登录状态或网址。")
                        return

                    thumbnails = page.locator(".thumbImg-container")
                    total_pages = thumbnails.count()
                    if total_pages == 0:
                        print("❌ 未检测到课件页数。")
                        return

                    print(f"✅ 检测到 {total_pages} 页课件，开始截图...")

                    # 每次翻页后移除遮挡控件，避免它重新出现。
                    remove_btn_js = """
                        const btn = document.querySelector(
                            '#app > div.viewContainer > div > section > main > div > div.basePPTMain.basePPTInline > div > div.layout_body > div.layout_right_switch'
                        );
                        if (btn) btn.remove();
                    """

                    for i in range(total_pages):
                        try:
                            thumb = thumbnails.nth(i)
                            thumb.scroll_into_view_if_needed()
                            thumb.click()
                            time.sleep(2.0)  # 等待文字、公式和图片渲染

                            page.evaluate(remove_btn_js)
                            image_path = Path(temp_dir) / f"page_{i + 1:03d}.png"
                            page.locator(".slide_layer").first.screenshot(
                                path=str(image_path), timeout=30000
                            )
                            image_paths.append(str(image_path))
                            print(f"✅ 第 {i + 1}/{total_pages} 页截取成功")
                        except Exception as exc:
                            print(f"⚠️ 第 {i + 1}/{total_pages} 页截取失败：{exc}")

                finally:
                    # 先关闭浏览器，才能安全删除磁盘缓存。
                    context.close()
                    context = None

            if not image_paths:
                print("❌ 没有成功截取任何页面，未生成 PDF。")
                return

            print("\n📦 正在合成 PDF...")
            with output_pdf.open("wb") as pdf_file:
                pdf_file.write(img2pdf.convert(image_paths))
            print(f"🎊 PDF 已保存：{output_pdf.resolve()}")
            if len(image_paths) != total_pages:
                print(f"⚠️ 注意：成功 {len(image_paths)} 页，失败 {total_pages - len(image_paths)} 页。")

        except Exception as exc:
            print(f"❌ 运行失败：{exc}")
        finally:
            # TemporaryDirectory 会自动删除本次生成的全部 PNG。
            # 浏览器必须已关闭；若启动/关闭失败，则不冒险删除可能在用的缓存。
            if context is None:
                clean_browser_cache()
            print("🧹 本次临时截图已清理；浏览器登录信息已保留。")

    # 只在目录为空时删除，不影响用户原有文件。
    try:
        save_dir.rmdir()
    except OSError:
        pass


if __name__ == "__main__":
    main()
