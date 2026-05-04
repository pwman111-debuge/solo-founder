import json
import os
import re
import urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

BASE_DIR = Path(__file__).parent.parent
SESSION_FILE = BASE_DIR / "tistory_session.json"
BLOG_NAME = os.environ.get("TISTORY_BLOG_NAME", "doctorhwang")
CATEGORY = os.environ.get("POST_CATEGORY", "건강 이야기")
HEADLESS = os.environ.get("HEADLESS", "False").lower() == "true"
EMAIL = os.environ.get("TISTORY_EMAIL", "")
PASSWORD = os.environ.get("TISTORY_PASSWORD", "")


def post_to_tistory(title: str, html: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        )

        if SESSION_FILE.exists():
            context.add_cookies(json.loads(SESSION_FILE.read_text(encoding="utf-8")))

        page = context.new_page()
        page.goto(f"https://{BLOG_NAME}.tistory.com/manage/newpost/")
        page.wait_for_load_state("networkidle", timeout=30000)

        if "login" in page.url or "kakao" in page.url or "auth" in page.url:
            _kakao_login(page, BLOG_NAME)
            _save_session(context)
            print("  세션 저장 완료")

        page.on("dialog", lambda d: d.dismiss())
        page.wait_for_timeout(2000)
        _dismiss_restore_popup(page)

        _fill_title(page, title)
        _inject_html(page, html)
        _set_category(page, CATEGORY)
        post_url = _publish(page)

        _save_session(context)
        browser.close()
        return post_url


def _kakao_login(page, blog_name: str) -> None:
    print("  카카오 자동 로그인 시도 중...")
    page.wait_for_load_state("networkidle", timeout=15000)

    if "tistory.com/auth/login" in page.url:
        page.get_by_role("link", name="카카오계정으로 로그인").click()
        page.wait_for_load_state("networkidle", timeout=15000)

    page.get_by_role("textbox", name="계정 정보 입력").fill(EMAIL)
    page.get_by_role("textbox", name="비밀번호 입력").fill(PASSWORD)
    page.get_by_role("button", name="로그인", exact=True).click()

    page.wait_for_url(f"**{blog_name}.tistory.com/manage/**", timeout=60000)
    print("  카카오 로그인 완료")


def _fill_title(page, title: str) -> None:
    page.wait_for_selector("#post-title-inp", timeout=10000)
    page.fill("#post-title-inp", title)


def _dismiss_restore_popup(page) -> None:
    for btn_text in ["취소", "아니오", "닫기", "새 글 작성"]:
        try:
            btn = page.locator(f"button:has-text('{btn_text}')").first
            if btn.is_visible(timeout=2000):
                btn.click()
                page.wait_for_timeout(800)
                return
        except Exception:
            continue


def _inject_html(page, html: str) -> None:
    page.wait_for_function(
        "() => !!(window.tinymce && tinymce.activeEditor && tinymce.activeEditor.initialized)",
        timeout=15000,
    )
    page.wait_for_timeout(1500)

    expected_len = len(html)

    for attempt in range(4):
        _dismiss_restore_popup(page)
        page.evaluate("(content) => tinymce.activeEditor.setContent(content)", html)
        page.wait_for_timeout(2000)
        _dismiss_restore_popup(page)

        current = page.evaluate("() => tinymce.activeEditor.getContent()")
        if current and len(current) > 200 and abs(len(current) - expected_len) / expected_len < 0.4:
            page.evaluate("() => tinymce.activeEditor.save()")
            page.wait_for_timeout(500)
            print(f"  [본문 주입] 성공 ({len(current)}자)")
            return
        print(f"  [본문 주입] 시도 {attempt + 1}: 길이 불일치({len(current) if current else 0}/{expected_len}), 재시도")
        page.wait_for_timeout(1500)

    raise RuntimeError("본문 주입 실패 — TinyMCE에 내용이 들어가지 않음")



def _set_category(page, category: str) -> None:
    try:
        page.get_by_role("combobox", name="카테고리 선택").click(timeout=3000)
        page.wait_for_timeout(300)
        page.get_by_role("option", name=category).click(timeout=3000)
    except Exception:
        pass


def _publish(page) -> str:
    page.evaluate("() => tinymce.activeEditor.save()")
    page.wait_for_timeout(500)
    final = page.evaluate("() => tinymce.activeEditor.getContent()")
    print(f"  [발행 직전 본문] {len(final or '')}자")

    old_url = _latest_post_url()

    page.locator("#publish-layer-btn, button:has-text('완료')").first.click(timeout=5000)
    page.wait_for_selector("[role='dialog']", timeout=8000)
    page.wait_for_timeout(500)

    page.get_by_role("dialog").get_by_role("button", name="공개 발행").click(timeout=5000)

    for _ in range(15):
        page.wait_for_timeout(3000)
        new_url = _latest_post_url()
        if new_url != old_url:
            return new_url

    return old_url


def _latest_post_url() -> str:
    try:
        rss_url = f"https://{BLOG_NAME}.tistory.com/rss"
        req = urllib.request.Request(rss_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            rss = r.read().decode("utf-8")
        match = re.search(r"<guid[^>]*>(https://[^<]+tistory\.com/\d+)</guid>", rss)
        if match:
            return match.group(1)
        match = re.search(r"<link>(https://[^<]+tistory\.com/entry/[^<]+)</link>", rss)
        if match:
            return match.group(1)
    except Exception:
        pass
    return f"https://{BLOG_NAME}.tistory.com"


def _save_session(context) -> None:
    cookies = context.cookies()
    SESSION_FILE.write_text(json.dumps(cookies, ensure_ascii=False), encoding="utf-8")
