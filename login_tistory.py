import sys
import json
from pathlib import Path
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv(Path(__file__).parent / ".env")

import os
from playwright.sync_api import sync_playwright

BLOG_NAME = os.environ.get("TISTORY_BLOG_NAME", "doctorhwang")
SESSION_FILE = Path(__file__).parent / "tistory_session.json"


def main():
    print("티스토리 로그인 세션 저장 도구")
    print("브라우저가 열리면 카카오 계정으로 로그인 후 관리 페이지가 열릴 때까지 기다려주세요.")
    print()

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

        print("로그인 대기 중... (최대 5분)")
        page.wait_for_url(f"**{BLOG_NAME}.tistory.com/manage/**", timeout=300000)

        cookies = context.cookies()
        SESSION_FILE.write_text(json.dumps(cookies, ensure_ascii=False), encoding="utf-8")
        print(f"세션 저장 완료: {SESSION_FILE}")
        browser.close()


if __name__ == "__main__":
    main()
