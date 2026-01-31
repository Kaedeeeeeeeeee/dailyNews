"""
note.com 自动发布器
使用 Playwright 自动填写文章内容并保存为草稿
"""

import asyncio
import json
import os
import re
from pathlib import Path
from playwright.async_api import async_playwright

COOKIES_FILE = Path(__file__).parent.parent / "note_cookies.json"


def is_x_url(line: str) -> bool:
    """检测是否为X/Twitter URL"""
    return bool(re.match(r'https://(x\.com|twitter\.com)/\w+/status/\d+', line.strip()))


def has_markdown_link(line: str) -> bool:
    """检测是否包含markdown链接语法 [text](url)"""
    return bool(re.search(r'\[.+\]\(https?://.+\)', line))


async def embed_x_url(page, url: str) -> bool:
    """
    使用note.com嵌入功能插入X URL
    返回True表示成功，False表示失败
    """
    try:
        # 确保光标在内容区域
        content_area = page.locator('.ProseMirror[contenteditable="true"]')
        await content_area.click()
        await page.wait_for_timeout(300)

        # 方法1: 尝试点击左侧的+按钮
        # note.com的+按钮通常在段落左侧
        plus_btn = None

        # 尝试多种选择器找到+按钮
        selectors = [
            'button[aria-label="ブロックを追加"]',
            'button[aria-label="Add block"]',
            '[data-testid="add-block-button"]',
        ]

        for selector in selectors:
            btn = page.locator(selector).first
            if await btn.count() > 0:
                plus_btn = btn
                break

        # 如果没找到，尝试通过位置查找（左侧的按钮）
        if not plus_btn or await plus_btn.count() == 0:
            buttons = page.locator('button')
            count = await buttons.count()
            for i in range(count):
                btn = buttons.nth(i)
                try:
                    bbox = await btn.bounding_box()
                    if bbox and bbox['x'] < 100:  # 左侧按钮
                        inner_text = await btn.inner_text()
                        if '+' in inner_text or inner_text == '':
                            plus_btn = btn
                            break
                except:
                    continue

        if not plus_btn or await plus_btn.count() == 0:
            print(f"⚠️ 未找到+按钮，跳过嵌入: {url[:50]}...")
            return False

        await plus_btn.click()
        await page.wait_for_timeout(500)

        # 选择「埋め込み」或「＜＞」选项
        embed_option = None
        embed_selectors = [
            'text=埋め込み',
            'text=＜＞',
            'text=貼り付け',
            '[data-testid="embed-option"]',
        ]

        for selector in embed_selectors:
            opt = page.locator(selector).first
            if await opt.count() > 0:
                embed_option = opt
                break

        if not embed_option or await embed_option.count() == 0:
            # 关闭菜单
            await page.keyboard.press('Escape')
            print(f"⚠️ 未找到埋め込み选项，跳过嵌入: {url[:50]}...")
            return False

        await embed_option.click()
        await page.wait_for_timeout(500)

        # 在输入框中填入URL
        url_input = page.locator('input[type="text"], input[placeholder*="URL"], input[placeholder*="url"]').first
        if await url_input.count() > 0:
            await url_input.fill(url)
            await page.keyboard.press('Enter')
            await page.wait_for_timeout(2000)  # 等待嵌入加载
            print(f"✅ 已嵌入X链接: {url[:50]}...")
            return True
        else:
            # 尝试直接在页面输入
            await page.keyboard.type(url)
            await page.keyboard.press('Enter')
            await page.wait_for_timeout(2000)
            print(f"✅ 已嵌入X链接(备用): {url[:50]}...")
            return True

    except Exception as e:
        print(f"⚠️ 嵌入失败: {e}")
        return False


async def create_draft(
    title: str,
    content: str,
    cover_image_path: str = None,
    headless: bool = True
) -> str:
    """创建 note.com 草稿"""
    if not COOKIES_FILE.exists():
        raise FileNotFoundError(f"Cookie 文件不存在: {COOKIES_FILE}")
    
    async with async_playwright() as p:
        # 使用反检测参数启动浏览器
        browser = await p.chromium.launch(
            headless=headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process'
            ]
        )
        
        # 使用真实浏览器指纹
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1280, 'height': 800},
            locale='ja-JP'
        )
        
        # 加载 cookies
        with open(COOKIES_FILE, "r") as f:
            cookies = json.load(f)
        await context.add_cookies(cookies)
        
        page = await context.new_page()
        
        # 打开新建文章页面
        print("正在打开 note.com 编辑器...")
        await page.goto("https://note.com/notes/new")
        
        # 等待完全加载（SPA 应用需要较长时间）
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(8000)  # 等待 SPA 渲染
        
        # 检查登录状态
        if "login" in page.url:
            await browser.close()
            raise PermissionError("Cookies 已过期")
        
        print(f"✅ 成功登录 note.com")
        print(f"   URL: {page.url}")
        
        # 等待编辑器就绪 - 使用多种选择器，增加超时
        editor_ready = False
        for wait_time in [15000, 20000, 30000]:  # 多次尝试
            for selector in [
                'textarea[placeholder="記事タイトル"]',
                'textarea',
                '.ProseMirror',
                '[contenteditable="true"]'
            ]:
                try:
                    await page.wait_for_selector(selector, timeout=wait_time)
                    editor_ready = True
                    print(f"✅ 编辑器已加载 (选择器: {selector})")
                    break
                except:
                    continue
            if editor_ready:
                break
            print(f"⏳ 等待编辑器加载... ({wait_time/1000}s)")
        
        if not editor_ready:
            print("⚠️ 编辑器加载超时，将截图后继续尝试...")
            await page.screenshot(path=str(Path(__file__).parent.parent / "output" / "note_error.png"))
        
        await page.wait_for_timeout(2000)
        
        # 上传封面图片
        if cover_image_path and os.path.exists(cover_image_path):
            print(f"🖼️ 正在上传封面...")
            try:
                # 点击封面上传按钮（会出现下拉菜单）
                cover_btn = page.locator('button[aria-label="画像を追加"]').first
                
                if await cover_btn.count() > 0:
                    await cover_btn.click()
                    await page.wait_for_timeout(1000)
                    
                    # 点击"画像をアップロード"选项
                    upload_option = page.get_by_text("画像をアップロード").first
                    if await upload_option.count() > 0:
                        async with page.expect_file_chooser(timeout=5000) as fc_info:
                            await upload_option.click()
                        file_chooser = await fc_info.value
                        await file_chooser.set_files(cover_image_path)
                        # 等待裁剪对话框出现
                        await page.wait_for_timeout(2000)
                        
                        # 在模态框内找保存按钮（日语：保存）
                        # 模态框通常在 ReactModalPortal 或有特定类名
                        modal_save = page.locator('.ReactModalPortal button:has-text("保存")').first
                        if await modal_save.count() == 0:
                            # 备用选择器
                            modal_save = page.locator('button:has-text("保存")').last
                        
                        if await modal_save.count() > 0:
                            await modal_save.click(force=True)  # 强制点击
                            await page.wait_for_timeout(3000)
                            print(f"✅ 封面已上传并保存")
                        else:
                            print(f"⚠️ 未找到保存按钮，封面可能需要手动保存")
                    else:
                        # 关闭菜单
                        await page.keyboard.press('Escape')
                        print(f"⚠️ 未找到上传选项")
                else:
                    print(f"⚠️ 未找到封面上传按钮，跳过")
            except Exception as e:
                print(f"⚠️ 封面上传失败: {e}")
                # 尝试关闭可能打开的菜单
                await page.keyboard.press('Escape')
        
        # 填写标题
        try:
            title_area = page.locator('textarea[placeholder="記事タイトル"]')
            if await title_area.count() > 0:
                await title_area.fill(title)
                print(f"✅ 标题已填写: {title[:40]}...")
            else:
                # 备用：尝试点击并输入
                await page.click('text=記事タイトル')
                await page.keyboard.type(title)
                print(f"✅ 标题已填写（备用方法）")
        except Exception as e:
            print(f"⚠️ 标题填写失败: {e}")
        
        await page.wait_for_timeout(500)
        
        # 填写内容
        try:
            content_area = page.locator('.ProseMirror[contenteditable="true"]')
            if await content_area.count() > 0:
                await content_area.click()
                await page.wait_for_timeout(500)
                
                # 转换为 note.com 友好格式
                note_content = convert_for_note(content)
                
                # 分离引用部分和正文部分
                lines = note_content.split('\n')
                intro_lines = []  # 引用/开头部分
                body_lines = []   # 正文部分
                found_first_heading = False
                
                for line in lines:
                    if line.startswith('## ') and not found_first_heading:
                        found_first_heading = True
                    
                    if found_first_heading:
                        body_lines.append(line)
                    else:
                        intro_lines.append(line)
                
                # 1. 先输入引用部分
                for line in intro_lines:
                    if line.strip():
                        await page.keyboard.type(line, delay=0)
                    await page.keyboard.press('Enter')
                await page.wait_for_timeout(500)
                
                # 2. 插入目录组件
                try:
                    # 需要先点击一个段落，+按钮才会出现在左边
                    # 点击引用区域（blockquote 或第一个段落）
                    quote_area = page.locator('.ProseMirror blockquote, .ProseMirror p').first
                    if await quote_area.count() > 0:
                        await quote_area.click()
                        await page.wait_for_timeout(500)
                    
                    # 现在+按钮应该出现了，查找它
                    # +按钮通常在段落左边，可能没有文字只有+符号
                    plus_btn = page.locator('button:has(svg)').filter(
                        has=page.locator('path')
                    ).first
                    
                    # 尝试多种选择器
                    if await plus_btn.count() == 0:
                        plus_btn = page.locator('[class*="add"], [class*="plus"], [class*="insert"]').first
                    
                    # 或者查找左侧区域的按钮
                    if await plus_btn.count() == 0:
                        # 从之前的截图看，+按钮在段落左边
                        # 尝试点击内容区域的前一个兄弟元素
                        buttons = page.locator('button')
                        count = await buttons.count()
                        for i in range(count):
                            btn = buttons.nth(i)
                            try:
                                bbox = await btn.bounding_box()
                                if bbox and bbox['x'] < 100 and 200 < bbox['y'] < 400:
                                    plus_btn = btn
                                    break
                            except:
                                continue
                    
                    if await plus_btn.count() > 0:
                        await plus_btn.click()
                        await page.wait_for_timeout(500)
                        
                        # 选择目次选项
                        toc_option = page.get_by_text('目次', exact=True).first
                        if await toc_option.count() > 0:
                            await toc_option.click()
                            await page.wait_for_timeout(1000)
                            print(f"✅ 目录已插入")
                        else:
                            await page.keyboard.press('Escape')
                            print(f"⚠️ 未找到目次选项")
                    else:
                        print(f"⚠️ 未找到+按钮，跳过目录插入")
                except Exception as e:
                    print(f"⚠️ 插入目录失败: {e}")
                
                # 3. 输入正文部分
                # 重新点击内容区域
                await content_area.click()
                await page.keyboard.press('End')  # 移动到末尾
                await page.keyboard.press('Enter')

                for i, line in enumerate(body_lines):
                    stripped = line.strip()
                    if stripped:
                        # 含markdown链接的行使用粘贴（触发markdown解析）
                        if has_markdown_link(stripped):
                            await page.evaluate(f'navigator.clipboard.writeText({repr(stripped)})')
                            await page.keyboard.press('Control+v')  # Linux (GitHub Actions)
                            await page.wait_for_timeout(200)
                        else:
                            await page.keyboard.type(line, delay=0)
                    await page.keyboard.press('Enter')

                    if i % 50 == 0 and i > 0:
                        await page.wait_for_timeout(500)
                
                # 限制长度检查
                total_len = len('\n'.join(intro_lines + body_lines))
                await page.wait_for_timeout(2000)
                print(f"✅ 内容已填写 ({total_len} 字符)")
            else:
                print("⚠️ 未找到内容编辑区")
        except Exception as e:
            print(f"⚠️ 内容填写失败: {e}")
        
        # 等待内容输入完成
        await page.wait_for_timeout(2000)
        
        # 点击"下書き保存"按钮保存草稿
        try:
            save_draft_btn = page.locator('button:has-text("下書き保存")').first
            if await save_draft_btn.count() > 0:
                await save_draft_btn.click()
                await page.wait_for_timeout(3000)
                print(f"✅ 草稿已保存")
        except Exception as e:
            print(f"⚠️ 保存草稿失败: {e}")
        
        # 获取草稿链接
        draft_url = page.url
        print(f"✅ 草稿 URL: {draft_url}")
        
        # 保存截图
        screenshot_path = Path(__file__).parent.parent / "output" / "note_draft.png"
        await page.screenshot(path=str(screenshot_path))
        print(f"✅ 截图已保存: {screenshot_path}")
        
        # 更新 cookies
        new_cookies = await context.cookies()
        with open(COOKIES_FILE, "w") as f:
            json.dump(new_cookies, f, indent=2, ensure_ascii=False)
        
        await browser.close()
        return draft_url


def convert_for_note(text: str) -> str:
    """
    转换 Markdown 为 note.com 友好格式
    - 移除会导致序号重复的格式
    - 保留可读性的结构
    """
    lines = text.split('\n')
    result = []
    in_toc = False  # 是否在目录区域
    skip_until_content = False
    
    for line in lines:
        # 检测目录开始 - 跳过整个目录部分（让 note.com 自动生成）
        if '## 目次' in line:
            in_toc = True
            # 不输出目录标题，note.com 会自动生成
            continue
        
        # 检测目录结束（遇到分隔线表示正文开始）
        if in_toc:
            if line.startswith('---'):
                in_toc = False
                result.append('')  # 空行
            continue  # 跳过所有目录内容
        
        # 处理正文标题：`## 1.【OpenAI】xxx` → `## 1. OpenAI: xxx`
        # 使用 ## + 空格，note.com 会识别为「大見出し」
        match = re.match(r'^##\s*(\d+)\.\s*【([^】]+)】\s*(.*)$', line)
        if match:
            num = match.group(1)
            source = match.group(2)
            title = match.group(3)
            result.append('')  # 空行分隔
            # 使用 ## 格式，让 note.com 识别为见出し
            if title:
                result.append(f'## {num}. {source}: {title}')
            else:
                result.append(f'## {num}. {source}')
            continue
        
        # 跳过其他 Markdown 标题标记（如 # 标题）
        if line.startswith('# ') and not line.startswith('## '):
            # 跳过主标题，已经单独处理了
            continue
        
        # 移除分隔线
        if re.match(r'^-{3,}$', line):
            result.append('')
            continue
        
        # 保留引用格式
        if line.startswith('>'):
            result.append(line)
            continue
        
        # 其他行保持原样
        result.append(line)
    
    # 合并过多空行
    text = '\n'.join(result)
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    
    return text.strip()


async def main():
    """命令行入口"""
    import sys
    from datetime import datetime
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python note_publisher.py test                    - 测试草稿")
        print("  python note_publisher.py publish <article> [cover] - 发布文章")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "test":
        today = datetime.now().strftime("%Y年%m月%d日")
        draft_url = await create_draft(
            title=f"🍁 Kaede's AI Daily News - {today}",
            content=f"今日はテストです。\n\n日付: {today}\n\n段落1の内容。\n\n段落2の内容。",
            headless=False
        )
        print(f"\n🔗 草稿链接: {draft_url}")
    
    elif cmd == "publish":
        if len(sys.argv) < 3:
            print("错误: 请指定文章路径")
            return
        
        article_path = sys.argv[2]
        cover_path = sys.argv[3] if len(sys.argv) > 3 else None
        
        if not os.path.exists(article_path):
            print(f"错误: 文件不存在 {article_path}")
            return
        
        with open(article_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.strip().split('\n')
        title = lines[0].lstrip('#').strip()
        body = '\n'.join(lines[1:]).strip()
        
        # 自动查找封面
        if not cover_path:
            dir_path = os.path.dirname(article_path)
            default_cover = os.path.join(dir_path, "cover.png")
            if os.path.exists(default_cover):
                cover_path = default_cover
        
        print(f"📄 文章: {article_path}")
        print(f"🖼️ 封面: {cover_path or '无'}")
        print(f"📝 标题: {title}")
        
        draft_url = await create_draft(
            title=title,
            content=body,
            cover_image_path=cover_path,
            headless=True
        )
        
        print(f"\n🔗 草稿链接: {draft_url}")
        
        # 输出到 GitHub Actions
        github_output = os.environ.get("GITHUB_OUTPUT")
        if github_output:
            with open(github_output, "a") as f:
                f.write(f"draft_url={draft_url}\n")


if __name__ == "__main__":
    asyncio.run(main())
