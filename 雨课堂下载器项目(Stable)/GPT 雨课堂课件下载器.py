from __future__ import annotations

from pathlib import Path
import re
import shutil
import tempfile
import time
from urllib.parse import urlparse

import img2pdf
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


# ================= 固定配置区域 =================
# 复用浏览器用户数据，保存 Cookie 等登录信息，实现下次免扫码。
USER_DATA_DIR = Path("./yuketang_login_cache")
DEFAULT_SAVE_DIR = Path("./yuketang_temp")
DEFAULT_OUTPUT_PDF = "下载课件.pdf"
CLASSROOM_FRAME = 'iframe[src*="/m/v2/lesson/student/"]'
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


def choose_source() -> str:
    print("👉 课件来源：")
    print("1. 老师上传的课件")
    print("2. 课堂回顾中的课件")
    print("(输入 1 或 2)")
    while True:
        choice = input("👉 请输入：").strip()
        if choice in {"1", "2"}:
            return choice
        print("❌ 请输入 1 或 2。")


def classroom_slide_groups(page) -> list[list[dict]]:
    """按 P1 重新开始的位置，把同一课堂的多组课件分开。"""
    frame = page.frame_locator(CLASSROOM_FRAME)
    try:
        frame.get_by_text("课件", exact=True).first.click(timeout=120000)
        frame.locator(".slide-list .slide-item").first.wait_for(timeout=30000)
    except PlaywrightTimeoutError as exc:
        raise RuntimeError("未找到课堂回顾中的课件，请检查登录状态、网址或课件权限。") from exc

    # 课件列表可能分批渲染；连续三次页数相同后再读取，避免漏掉后续组。
    items = frame.locator(".slide-list .slide-item")
    previous_count = -1
    stable_samples = 0
    for _ in range(12):
        current_count = items.count()
        stable_samples = stable_samples + 1 if current_count == previous_count else 0
        if stable_samples >= 2:
            break
        previous_count = current_count
        page.wait_for_timeout(500)

    slides = items.evaluate_all(
        """items => items.map(item => {
            const match = item.textContent.trim().match(/^P\\s*(\\d+)/);
            const image = item.querySelector('img');
            return {
                number: match ? Number(match[1]) : null,
                url: image?.getAttribute('data-src') || image?.getAttribute('src') || null
            };
        })"""
    )
    return split_classroom_slides(slides)


def split_classroom_slides(slides: list[dict]) -> list[list[dict]]:
    if not slides:
        raise RuntimeError("课堂课件列表为空。")
    groups: list[list[dict]] = []
    for slide in slides:
        if not slide["number"] or not slide["url"]:
            raise RuntimeError("课件列表有缺失的页码或图片，已停止以避免生成漏页 PDF。")
        if slide["number"] == 1:
            groups.append([])
        if not groups or slide["number"] != len(groups[-1]) + 1:
            raise RuntimeError("课件页码不连续，已停止以避免把不同课件混在一起。")
        groups[-1].append(slide)
    return groups


def choose_classroom_group(groups: list[list[dict]]) -> int:
    print(f"✅ 发现 {len(groups)} 组课堂课件：")
    for i, group in enumerate(groups, 1):
        print(f"   {i}. 第 {i} 组，P1–P{len(group)}，共 {len(group)} 页")
    if len(groups) == 1:
        return 0
    while True:
        value = input(f"👉 请选择要下载的组号 (直接回车选择第 {len(groups)} 组): ").strip()
        if not value:
            return len(groups) - 1
        if value.isdigit() and 1 <= int(value) <= len(groups):
            return int(value) - 1
        print("❌ 请输入上面列出的组号。")


def image_extension(data: bytes) -> str:
    if data.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    raise ValueError("返回内容不是受支持的 JPEG/PNG 课件图片")


def download_classroom_slides(context, page, groups: list[list[dict]],
                              group_index: int, temp_dir: Path) -> list[Path]:
    """下载完整课堂原图；签名失效时刷新页面并重试。"""
    selected = groups[group_index]
    total_pages = len(selected)
    image_paths = []
    print(f"✅ 已选择第 {group_index + 1} 组，共 {total_pages} 页，开始下载完整原图...")

    for i in range(total_pages):
        for attempt in range(3):
            url = selected[i]["url"]
            parsed = urlparse(url)
            if parsed.scheme != "https" or not (
                parsed.hostname == "yuketang.cn"
                or (parsed.hostname or "").endswith(".yuketang.cn")
            ):
                raise RuntimeError(f"第 {i + 1} 页的图片地址不属于雨课堂，已停止下载。")

            response = None
            try:
                response = context.request.get(
                    url, headers={"Referer": page.url}, timeout=45000
                )
                if not response.ok:
                    raise RuntimeError(f"HTTP {response.status}")
                data = response.body()
                suffix = image_extension(data)
                image_path = temp_dir / f"page_{i + 1:04d}{suffix}"
                image_path.write_bytes(data)
                image_paths.append(image_path)
                print(f"✅ 第 {i + 1}/{total_pages} 页下载成功")
                break
            except Exception as exc:
                if attempt == 2:
                    raise RuntimeError(
                        f"第 {i + 1}/{total_pages} 页连续三次下载失败：{exc}"
                    ) from exc
                print(f"⚠️ 第 {i + 1} 页下载失败，正在重试：{exc}")
                if response is not None and response.status in {401, 403}:
                    page.reload(wait_until="domcontentloaded", timeout=60000)
                    refreshed = classroom_slide_groups(page)
                    if (group_index >= len(refreshed)
                            or len(refreshed[group_index]) != total_pages):
                        raise RuntimeError("刷新后课件页数发生变化，已停止以避免漏页。")
                    selected = refreshed[group_index]
                else:
                    time.sleep(1)
            finally:
                if response is not None:
                    response.dispose()
    return image_paths


def capture_uploaded_slides(page, temp_dir: Path) -> tuple[list[Path], int]:
    """上传课件的文字和插图由 JavaScript 渲染，因此保留整页截图。"""
    try:
        page.wait_for_selector(".thumbImg-container", timeout=120000)
    except PlaywrightTimeoutError as exc:
        raise RuntimeError("两分钟内未检测到上传课件缩略图，请检查登录状态或网址。") from exc

    thumbnails = page.locator(".thumbImg-container")
    total_pages = thumbnails.count()
    if not total_pages:
        raise RuntimeError("未检测到上传课件页数。")
    print(f"✅ 检测到 {total_pages} 页上传课件，开始截图...")

    remove_btn_js = """
        const btn = document.querySelector(
            '#app > div.viewContainer > div > section > main > div > div.basePPTMain.basePPTInline > div > div.layout_body > div.layout_right_switch'
        );
        if (btn) btn.remove();
    """
    image_paths = []
    for i in range(total_pages):
        try:
            thumb = thumbnails.nth(i)
            thumb.scroll_into_view_if_needed()
            thumb.click()
            time.sleep(2.0)  # 等待文字、公式和图片渲染
            page.evaluate(remove_btn_js)
            image_path = temp_dir / f"page_{i + 1:04d}.png"
            page.locator(".slide_layer").first.screenshot(
                path=str(image_path), timeout=30000
            )
            image_paths.append(image_path)
            print(f"✅ 第 {i + 1}/{total_pages} 页截取成功")
        except Exception as exc:
            print(f"⚠️ 第 {i + 1}/{total_pages} 页截取失败：{exc}")
    return image_paths, total_pages


def main() -> None:
    print("=" * 53)
    print(" 🚀 雨课堂课件自动化下载器")
    print("=" * 53)

    source = choose_source()
    prompt = "课堂回顾的网址" if source == "2" else "上传课件的网址"
    course_url = input(f"👉 请输入{prompt} (回车确认): ").strip()
    if not course_url:
        print("❌ 网址不能为空，程序退出！")
        return
    if source == "2":
        parsed = urlparse(course_url)
        if (parsed.scheme != "https"
                or parsed.hostname not in {"yuketang.cn", "www.yuketang.cn"}
                or not re.fullmatch(
                    r"/v2/web/student-lesson-report/\d+/\d+/\d+/?", parsed.path
                )):
            print("❌ 课堂课件请输入雨课堂 student-lesson-report 页面网址。")
            return

    save_dir_input = input(
        "👉 请输入截图/图片临时文件夹 (直接回车默认 './yuketang_temp'): "
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

    # 每次运行创建独立的临时子目录；只删除本次生成的文件。
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

                    if source == "1":
                        image_paths, total_pages = capture_uploaded_slides(
                            page, Path(temp_dir)
                        )
                    else:
                        groups = classroom_slide_groups(page)
                        group_index = choose_classroom_group(groups)
                        image_paths = download_classroom_slides(
                            context, page, groups, group_index, Path(temp_dir)
                        )
                        total_pages = len(groups[group_index])

                finally:
                    # 先关闭浏览器，才能安全删除磁盘缓存。
                    context.close()
                    context = None

            if not image_paths:
                print("❌ 没有成功获取任何页面，未生成 PDF。")
                return

            print("\n📦 正在合成 PDF...")
            partial_pdf = output_pdf.with_name(output_pdf.name + ".partial")
            try:
                with partial_pdf.open("wb") as pdf_file:
                    pdf_file.write(img2pdf.convert([str(path) for path in image_paths]))
                partial_pdf.replace(output_pdf)
            finally:
                partial_pdf.unlink(missing_ok=True)
            print(f"🎊 PDF 已保存：{output_pdf.resolve()}")
            if len(image_paths) != total_pages:
                print(f"⚠️ 注意：成功 {len(image_paths)} 页，失败 {total_pages - len(image_paths)} 页。")

        except Exception as exc:
            print(f"❌ 运行失败：{exc}")
        finally:
            # TemporaryDirectory 会自动删除本次生成的 PNG/JPEG。
            # 浏览器必须已关闭；若启动/关闭失败，则不冒险删除可能在用的缓存。
            if context is None:
                clean_browser_cache()
            print("🧹 本次临时文件已清理；浏览器登录信息已保留。")

    # 只在目录为空时删除，不影响用户原有文件。
    try:
        save_dir.rmdir()
    except OSError:
        pass


if __name__ == "__main__":
    main()
