import sys
import json
from pathlib import Path
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv(Path(__file__).parent / ".env")

import os
from playwright.sync_api import sync_playwright

BLOG_NAME = os.environ.get("TISTORY_BLOG_NAME", "doctorhwang")
EMAIL = os.environ.get("TISTORY_EMAIL", "")
PASSWORD = os.environ.get("TISTORY_PASSWORD", "")
SESSION_FILE = Path(__file__).parent / "tistory_session.json"


def main():
    print("티스토리 카카오 자동 로그인 세션 저장")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        )
        page = context.new_page()
        page.goto(f"https://{BLOG_NAME}.tistory.com/manage/newpost/")
        page.wait_for_load_state("networkidle", timeout=30000)

        if "login" in page.url or "kakao" in page.url or "auth" in page.url:
            if "tistory.com/auth/login" in page.url:
                page.get_by_role("link", name="카카오계정으로 로그인").click()
                page.wait_for_load_state("networkidle", timeout=15000)
            page.get_by_role("textbox", name="계정 정보 입력").fill(EMAIL)
            page.get_by_role("textbox", name="비밀번호 입력").fill(PASSWORD)
            page.get_by_role("button", name="로그인", exact=True).click()
            page.wait_for_url(f"**{BLOG_NAME}.tistory.com/manage/**", timeout=60000)

        cookies = context.cookies()
        SESSION_FILE.write_text(json.dumps(cookies, ensure_ascii=False), encoding="utf-8")
        print(f"세션 저장 완료: {SESSION_FILE}")
        browser.close()


if __name__ == "__main__":
    main()
