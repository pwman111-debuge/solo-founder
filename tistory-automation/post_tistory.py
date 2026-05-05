import sys
import os
import time
import argparse
from pathlib import Path
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")

load_dotenv(Path(__file__).parent / ".env")

LOCK_FILE = Path(__file__).parent / ".running.lock"


def acquire_lock():
    if LOCK_FILE.exists():
        pid = LOCK_FILE.read_text().strip()
        print(f"이미 실행 중입니다 (PID {pid}). 중복 실행 방지로 종료합니다.")
        sys.exit(1)
    LOCK_FILE.write_text(str(os.getpid()))


def release_lock():
    LOCK_FILE.unlink(missing_ok=True)

from modules.keyword_picker import pick_keyword
from modules.content_generator import generate_content
from modules.html_converter import convert_to_html
from modules.tistory_poster import post_to_tistory
from modules.threads_poster import post_to_threads
from modules.linkedin_poster import post_to_linkedin
from modules.logger import log_post

POSTS_PER_RUN = 3
DELAY_BETWEEN_POSTS = 120


def run_once(index: int, total: int, keyword_override: str | None = None) -> dict | None:
    print(f"\n[편 {index}/{total}]")
    try:
        if keyword_override:
            kw = {"keyword": keyword_override, "category": "건강"}
        else:
            kw = pick_keyword()
        print(f"  [1/6] 키워드: \"{kw['keyword']}\"")

        content = generate_content(kw)
        coupang_meta = content.get("coupang_items")
        if coupang_meta and isinstance(coupang_meta[0], str):
            coupang_meta = [{"category": item, "reason": ""} for item in coupang_meta]
        coupang_label = f"예 — {coupang_meta[0]['category']}" if coupang_meta else "아니오"
        print(f"  [2/6] 콘텐츠 생성 완료 (쿠팡 삽입: {coupang_label})")

        html = convert_to_html(content["markdown"], coupang_meta)
        print(f"  [3/5] HTML 변환 완료")

        post_url = post_to_tistory(
            title=content["title"],
            html=html,
        )
        print(f"  [4/5] 티스토리 발행 완료")

        threads_ok = post_to_threads(content["sns_summary"], post_url)
        linkedin_ok = post_to_linkedin(content["sns_summary"], post_url)
        t_mark = "✓" if threads_ok else "✗"
        l_mark = "✓" if linkedin_ok else "✗"
        print(f"  [5/5] Threads {t_mark}  LinkedIn {l_mark}")
        print(f"  → {post_url}")

        log_post(kw["keyword"], content["title"], post_url, threads_ok, linkedin_ok)

        return {"url": post_url, "title": content["title"]}

    except Exception as e:
        import traceback
        print(f"  ❌ 오류 발생: {e}")
        traceback.print_exc()
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword", type=str, default=None, help="강제 지정 키워드")
    parser.add_argument("--count", type=int, default=POSTS_PER_RUN, help="발행 편수")
    args = parser.parse_args()

    count = args.count
    print(f"=== 오늘의 포스팅 시작 ({count}편) ===")
    start = time.time()
    results = []

    for i in range(1, count + 1):
        result = run_once(i, count, keyword_override=args.keyword)
        if result:
            results.append(result)
        if i < count:
            print(f"\n  ({DELAY_BETWEEN_POSTS}초 대기 중...)")
            time.sleep(DELAY_BETWEEN_POSTS)

    elapsed = int(time.time() - start)
    print(f"\n=== 완료 (총 소요: {elapsed//60}분 {elapsed%60}초) ===")
    print(f"오늘 발행: {len(results)}/{count}편")
    for r in results:
        print(f"  {r['url']}")


if __name__ == "__main__":
    acquire_lock()
    try:
        main()
    finally:
        release_lock()
