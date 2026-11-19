"""雨课堂下载器 Beta。

上传课件优先按原始图片图层复原 PDF；不兼容时回退到稳定版截图。
额外依赖：pip install pymupdf pillow certifi
"""

from __future__ import annotations

from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from http.client import IncompleteRead
from io import BytesIO
import math
import re
import shutil
import ssl
import tempfile
import time
from urllib.parse import urlparse
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import img2pdf
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

try:
    import certifi
except ImportError:
    certifi = None

ASSET_SSL_CONTEXT = ssl.create_default_context(
    cafile=certifi.where() if certifi is not None else None
)

try:
    import fitz
    from PIL import Image
except ImportError:
    fitz = None
    Image = None


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
    """按页码重新从 P1 开始的位置拆分课堂课件。"""
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
            const label = item.querySelector('.slide-desc > span')?.textContent || '';
            const match = label.trim().match(/^P\\s*(\\d+)$/);
            const image = item.querySelector('img');
            return {
                number: match ? Number(match[1]) : null,
                url: image?.getAttribute('data-src') || image?.getAttribute('src') || null
            };
        })"""
    )
    return split_classroom_slides(slides)


def classroom_presentations(page) -> list[dict]:
    """将“打印课件”的文件名与页面中按 P1 分开的课件逐一对应。"""
    groups = classroom_slide_groups(page)
    frame = page.frame_locator(CLASSROOM_FRAME)
    titles = frame.locator(".ppt-list .ppt-list-item .ppt-title")
    if not titles.count():
        try:
            frame.get_by_text("打印课件").first.click(timeout=10000)
            titles.first.wait_for(timeout=10000)
        except PlaywrightTimeoutError as exc:
            raise RuntimeError("无法读取“打印课件”中的文件名，已停止以避免混合不同课件。") from exc
    names = [name.strip() for name in titles.all_text_contents()]
    if len(names) != len(groups) or not all(names):
        raise RuntimeError(
            f"打印课件列出 {len(names)} 份，页面识别到 {len(groups)} 组；"
            "数量不一致，已停止以避免把课件混在一起。"
        )
    return [{"name": name, "slides": group} for name, group in zip(names, groups)]


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


def choose_classroom_groups(presentations: list[dict]) -> list[int]:
    print(f"✅ 发现 {len(presentations)} 份课堂课件：")
    for i, item in enumerate(presentations, 1):
        print(f"   {i}. {item['name']}（{len(item['slides'])} 页）")
    print("   A. 全部下载")
    while True:
        value = input("👉 请选择课件序号（多选用逗号分隔，全部输入 A）：").strip()
        if value.lower() in {"a", "all"}:
            return list(range(len(presentations)))
        parts = [part.strip() for part in value.replace("，", ",").split(",")]
        if parts and all(part.isdigit() and 1 <= int(part) <= len(presentations)
                         for part in parts):
            return sorted({int(part) - 1 for part in parts})
        print("❌ 请输入有效序号，例如 1,3；全部下载请输入 A。")


def classroom_pdf_path(base: Path, index: int, name: str, multiple: bool) -> Path:
    if not multiple:
        return base
    safe_name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name).strip(" .")[:70]
    return base.with_name(f"{base.stem}_{index + 1:02d}_{safe_name or '课件'}.pdf")


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


def uploaded_layer_manifest(page) -> list[dict]:
    """一次读取所有页面已渲染的背景、母版和正文图片层。"""
    page.wait_for_selector(".thumbImg-container", timeout=120000)
    manifest = page.evaluate("""() => {
        const decks = [...document.querySelectorAll('.courseware')];
        return decks.map(deck => {
            const width = parseFloat(deck.style.width);
            const height = parseFloat(deck.style.height);
            const layers = ['.bg_layer', '.master_bg_layer', '.slide_layer'];
            const images = [];
            let unsupported = false;
            for (const selector of layers) {
                const layer = deck.querySelector(selector);
                if (!layer) { unsupported = true; continue; }
                for (const child of layer.children) {
                    if (child.tagName !== 'IMG') { unsupported = true; continue; }
                    images.push({
                        url: child.getAttribute('src'),
                        width: child.style.width,
                        height: child.style.height,
                        minHeight: child.style.minHeight,
                        left: child.style.left,
                        top: child.style.top,
                        rotate: child.style.transform,
                        z: Number(child.style.zIndex) || 0,
                        layer: layers.indexOf(selector)
                    });
                }
            }
            return {width, height, images, unsupported,
                    bg: deck.querySelector('.bg_layer')?.style.backgroundColor || 'white'};
        });
    }""")
    expected = page.locator(".thumbImg-container").count()
    if not manifest or len(manifest) != expected:
        raise RuntimeError(f"图层页数 {len(manifest)} 与缩略图页数 {expected} 不一致")
    if any(item["unsupported"] or not item["images"] or
           not item["width"] or not item["height"] or
           any(not image["url"] for image in item["images"])
           for item in manifest):
        raise RuntimeError("含有未识别的课件图层")
    return manifest


def checked_asset_url(url: str) -> str:
    parsed = urlparse(url)
    host = parsed.hostname or ""
    if parsed.scheme not in {"http", "https"} or not (
        host == "ykt.io" or host.endswith(".ykt.io") or
        host == "yuketang.cn" or host.endswith(".yuketang.cn")
    ):
        raise RuntimeError("课件素材地址不属于雨课堂")
    return parsed._replace(scheme="https").geturl()


def verified_layer_image(data: bytes) -> bytes:
    image = Image.open(BytesIO(data))
    image.verify()
    if image.format not in {"PNG", "JPEG"}:
        with Image.open(BytesIO(data)) as image:
            converted = BytesIO()
            image.convert("RGBA" if "A" in image.getbands() else "RGB").save(
                converted, format="PNG"
            )
            return converted.getvalue()
    return data


def download_layer_asset(url: str, referer: str) -> tuple[str, bytes]:
    asset_url = checked_asset_url(url)
    # python.org 的 macOS Python 可能没有安装默认 CA 文件；使用 certifi 的
    # 公共根证书继续严格校验 HTTPS，不关闭证书验证。
    for attempt in range(5):
        try:
            request = Request(asset_url, headers={
                "Referer": referer, "User-Agent": "Mozilla/5.0"
            })
            with urlopen(request, timeout=45, context=ASSET_SSL_CONTEXT) as response:
                data = response.read()
            return url, verified_layer_image(data)
        except HTTPError as exc:
            if exc.code not in {408, 429, 500, 502, 503, 504}:
                raise
            if attempt == 4:
                raise
        except (OSError, IncompleteRead):
            # 包含 RemoteDisconnected、连接重置、TLS EOF 和不完整图片。
            if attempt == 4:
                raise
        time.sleep(min(0.75 * 2 ** attempt, 6))


def browser_layer_asset(page, url: str) -> bytes:
    """Python 连接反复中断时，用已登录浏览器的请求通道补取单张图片。"""
    for attempt in range(3):
        try:
            response = page.context.request.get(
                checked_asset_url(url),
                headers={"Referer": page.url, "User-Agent": "Mozilla/5.0"},
                timeout=45000,
            )
            try:
                if not response.ok:
                    raise RuntimeError(f"HTTP {response.status}")
                return verified_layer_image(response.body())
            finally:
                response.dispose()
        except Exception:
            if attempt == 2:
                raise
            time.sleep(1.5 * (attempt + 1))


def css_length(value: str, total: float, default: float = 0) -> float:
    if not value:
        return default
    if value.endswith("%"):
        return total * float(value[:-1]) / 100
    if value.endswith("px"):
        return float(value[:-2])
    raise RuntimeError(f"不支持的课件尺寸：{value}")


def pdf_background(page, color: str) -> None:
    if color == "white":
        return
    match = re.fullmatch(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", color)
    if not match:
        raise RuntimeError(f"不支持的课件背景色：{color}")
    rgb = tuple(int(value) / 255 for value in match.groups())
    page.draw_rect(page.rect, color=rgb, fill=rgb, overlay=False)


def export_uploaded_layers(page, output_pdf: Path) -> int:
    """直接复原图片层，保留源图分辨率并在 PDF 内复用重复素材。"""
    if fitz is None or Image is None:
        raise RuntimeError("优化模式需要 pymupdf 和 pillow")
    manifest = uploaded_layer_manifest(page)
    urls = {image["url"] for slide in manifest for image in slide["images"]}
    print(f"✅ 识别到 {len(manifest)} 页、{len(urls)} 个独立图片素材，开始下载...")
    assets = {}
    failed = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(download_layer_asset, url, page.url): url for url in urls}
        for future in as_completed(futures):
            try:
                url, data = future.result()
                assets[url] = data
            except Exception as exc:
                failed.append((futures[future], exc))
            if (len(assets) + len(failed)) % 100 == 0:
                print(f"⏳ 素材下载进度：{len(assets) + len(failed)}/{len(urls)}")
    if failed:
        print(f"⚠️ {len(failed)} 个素材首轮下载失败，正在逐个重试...")
        for index, (url, _) in enumerate(failed, 1):
            try:
                _, data = download_layer_asset(url, page.url)
                assets[url] = data
                print(f"✅ 重试成功：{index}/{len(failed)}")
            except Exception as exc:
                print(f"⚠️ 素材 {index}/{len(failed)} 仍连接失败，改用浏览器请求...")
                try:
                    assets[url] = browser_layer_asset(page, url)
                    print(f"✅ 浏览器补取成功：{index}/{len(failed)}")
                except Exception as browser_exc:
                    raise RuntimeError(
                        f"素材 {index}/{len(failed)} 最终下载失败（{url}）："
                        f"Python: {exc}；浏览器: {browser_exc}"
                    ) from browser_exc

    document = fitz.open()
    image_refs = {}
    rotated_refs = {}
    try:
        for slide_number, slide in enumerate(manifest, 1):
            pdf_page = document.new_page(width=slide["width"], height=slide["height"])
            pdf_background(pdf_page, slide["bg"])
            for item in sorted(slide["images"], key=lambda x: (x["layer"], x["z"])):
                data = assets[item["url"]]
                with Image.open(BytesIO(data)) as source:
                    natural_width, natural_height = source.size
                width = css_length(item["width"], slide["width"])
                height = css_length(item["height"], slide["height"],
                                    width * natural_height / natural_width)
                height = max(height, css_length(item["minHeight"], slide["height"]))
                left = css_length(item["left"], slide["width"])
                top = css_length(item["top"], slide["height"])
                angle_text = item["rotate"] or "rotate(0deg)"
                match = re.fullmatch(r"rotate\((-?[\d.]+)deg\)", angle_text)
                if not match:
                    raise RuntimeError(f"不支持的图片旋转：{angle_text}")
                angle = float(match.group(1)) % 360
                if angle:
                    key = (item["url"], angle, round(width, 2), round(height, 2))
                    if key not in rotated_refs:
                        with Image.open(BytesIO(data)) as source:
                            scale = max(source.width / width, source.height / height, 1)
                            pixels = source.convert("RGBA").resize(
                                (max(1, round(width * scale)), max(1, round(height * scale))),
                                Image.Resampling.LANCZOS
                            )
                            rotated = pixels.rotate(-angle, expand=True,
                                                    resample=Image.Resampling.BICUBIC)
                            buffer = BytesIO()
                            rotated.save(buffer, format="PNG")
                        rotated_refs[key] = buffer.getvalue()
                    data = rotated_refs[key]
                    radians = math.radians(angle)
                    box_width = abs(width * math.cos(radians)) + abs(height * math.sin(radians))
                    box_height = abs(width * math.sin(radians)) + abs(height * math.cos(radians))
                    left += (width - box_width) / 2
                    top += (height - box_height) / 2
                    width, height = box_width, box_height
                    cache_key = key
                else:
                    cache_key = item["url"]
                rectangle = fitz.Rect(left, top, left + width, top + height)
                image_refs[cache_key] = pdf_page.insert_image(
                    rectangle, stream=data if cache_key not in image_refs else None,
                    xref=image_refs.get(cache_key, 0), keep_proportion=False,
                    overlay=True
                )
            print(f"✅ 第 {slide_number}/{len(manifest)} 页已复原")
        partial = output_pdf.with_name(output_pdf.name + ".partial")
        try:
            document.save(str(partial), garbage=4, deflate=True)
            partial.replace(output_pdf)
        finally:
            partial.unlink(missing_ok=True)
    finally:
        document.close()
    return len(manifest)


def main() -> None:
    print("=" * 53)
    print(" 🚀 雨课堂课件下载器 Beta")
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

        # 先取得实际文件名，再询问保存位置；此时不下载图片。
        try:
            with sync_playwright() as p:
                context = p.chromium.launch_persistent_context(
                    user_data_dir=str(USER_DATA_DIR), headless=False,
                    viewport={"width": 1920, "height": 1080},
                )
                try:
                    page = context.pages[0] if context.pages else context.new_page()
                    page.goto(course_url, wait_until="domcontentloaded", timeout=60000)
                    print("💡 未登录请在浏览器中扫码；已登录则自动识别课堂课件。")
                    presentations = classroom_presentations(page)
                    selected_indices = choose_classroom_groups(presentations)
                    expected = [(item["name"], len(item["slides"]))
                                for item in presentations]
                finally:
                    context.close()
        except Exception as exc:
            print(f"❌ 无法识别课堂课件：{exc}")
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

    # 所有输入已完成；从这里计时到下载、合成与清理结束。
    started_at = time.perf_counter()

    # 保证用户给出的输出路径有可用的父目录。
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    save_dir.mkdir(parents=True, exist_ok=True)

    # 每次运行创建独立的临时子目录；只删除本次生成的文件。
    with tempfile.TemporaryDirectory(prefix="capture_", dir=save_dir) as temp_dir:
        image_paths = []
        classroom_results = []
        optimized_uploaded = False
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
                        try:
                            total_pages = export_uploaded_layers(page, output_pdf)
                            optimized_uploaded = True
                        except Exception as exc:
                            print(f"⚠️ 图片层复原不可用：{exc}")
                            print("⏳ 正在回退到原有逐页截图方式...")
                            image_paths, total_pages = capture_uploaded_slides(
                                page, Path(temp_dir)
                            )
                    else:
                        current = classroom_presentations(page)
                        if [(item["name"], len(item["slides"])) for item in current] != expected:
                            raise RuntimeError("重新打开页面后课件列表发生变化，已停止以避免错选。")
                        groups = [item["slides"] for item in current]
                        for group_index in selected_indices:
                            group_dir = Path(temp_dir) / f"group_{group_index + 1:02d}"
                            group_dir.mkdir()
                            paths = download_classroom_slides(
                                context, page, groups, group_index, group_dir
                            )
                            classroom_results.append((group_index, current[group_index]["name"], paths))

                finally:
                    # 先关闭浏览器，才能安全删除磁盘缓存。
                    context.close()
                    context = None

            if source == "1" and not optimized_uploaded and not image_paths:
                raise RuntimeError("没有成功获取任何页面，未生成 PDF。")

            if source == "1" and optimized_uploaded:
                print(f"🎊 优化版 PDF 已保存：{output_pdf.resolve()}")
                targets = []
            elif source == "1":
                targets = [(output_pdf, image_paths)]
            else:
                targets = [
                    (classroom_pdf_path(output_pdf, index, name,
                                        len(classroom_results) > 1), paths)
                    for index, name, paths in classroom_results
                ]
            for pdf_path, paths in targets:
                if not paths:
                    raise RuntimeError(f"{pdf_path.name} 没有可合成的课件页面。")
                print(f"\n📦 正在合成 {pdf_path.name}...")
                partial_pdf = pdf_path.with_name(pdf_path.name + ".partial")
                try:
                    with partial_pdf.open("wb") as pdf_file:
                        pdf_file.write(img2pdf.convert([str(path) for path in paths]))
                    partial_pdf.replace(pdf_path)
                finally:
                    partial_pdf.unlink(missing_ok=True)
                print(f"🎊 PDF 已保存：{pdf_path.resolve()}")
            if source == "1" and len(image_paths) != total_pages:
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

    minutes, seconds = divmod(int(time.perf_counter() - started_at), 60)
    print(f"⏱️ 下载总耗时：{minutes} 分 {seconds} 秒")


if __name__ == "__main__":
    main()
