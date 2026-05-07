import os
import sys
from pathlib import Path
from markdown_it import MarkdownIt

sys.path.insert(0, str(Path(__file__).parent.parent))
from config.coupang_links import get_coupang_items

md = MarkdownIt()

COUPANG_ENABLED = os.environ.get("COUPANG_ENABLED", "False").lower() == "true"

WRAPPER_STYLE = (
    "max-width:720px;margin:0 auto;font-family:'Noto Sans KR',sans-serif;"
    "font-size:16px;line-height:1.9;color:#222;"
)
SUMMARY_BOX_STYLE = (
    "background:#eef6ff;border-left:4px solid #2196F3;"
    "padding:18px 20px;margin:24px 0;border-radius:0 6px 6px 0;"
    "font-size:15px;line-height:1.8;"
)
DISCLAIMER_STYLE = (
    "font-size:12px;color:#999;border-top:1px solid #eee;"
    "margin-top:48px;padding-top:12px;"
)
COUPANG_TOP_NOTICE_STYLE = (
    "font-size:13px;color:#555;background:#fff8e1;border-left:3px solid #FFC107;"
    "padding:10px 14px;margin-bottom:24px;"
)
COUPANG_NOTICE_STYLE = "font-size:11px;color:#bbb;margin-bottom:10px;"
COUPANG_CARD_STYLE = (
    "display:inline-block;border:1px solid #e0e0e0;border-radius:8px;"
    "padding:14px 18px;margin:6px 6px 6px 0;text-decoration:none;"
    "color:#333;background:#fff;vertical-align:top;min-width:200px;"
)


def convert_to_html(markdown_text: str, coupang_items_meta: list | None) -> str:
    body_html = md.render(markdown_text)

    # 첫 번째 <p> 뒤의 ## 핵심 요약 블록을 파란 박스로 변환
    body_html = _style_summary_box(body_html)

    coupang_top = ""
    coupang_html = ""
    if COUPANG_ENABLED:
        categories = [item["category"] for item in coupang_items_meta] if coupang_items_meta else []
        products = get_coupang_items(categories, limit=2)
        if products:
            coupang_html = _build_coupang_block(products[:1])
            if len(products) >= 2:
                body_html = _inject_mid_coupang(body_html, _build_coupang_block(products[1:2]))

    disclaimer = (
        f'<p style="{DISCLAIMER_STYLE}">'
        "본 내용은 의학적 참고 정보이며, 개인 진료를 대체하지 않습니다. "
        "증상이 지속되면 전문의 상담을 받으시기 바랍니다."
        "</p>"
    )

    html = (
        f'<div style="{WRAPPER_STYLE}">'
        f"{coupang_top}"
        f"{body_html}"
        f"{coupang_html}"
        f"{disclaimer}"
        "</div>"
    )

    return html


def _style_summary_box(html: str) -> str:
    """## 핵심 요약 섹션 바로 다음 <ul> 또는 <p>를 파란 박스로 감싼다."""
    marker_start = "<h2>핵심 요약</h2>"
    marker_end_tags = ["<h2>", "<h3>"]

    if marker_start not in html:
        return html

    start_idx = html.index(marker_start)
    content_start = start_idx + len(marker_start)

    end_idx = len(html)
    for tag in marker_end_tags:
        pos = html.find(tag, content_start + 10)
        if pos != -1 and pos < end_idx:
            end_idx = pos

    summary_content = html[content_start:end_idx]
    boxed = f'<div style="{SUMMARY_BOX_STYLE}">{summary_content}</div>'

    return html[:start_idx] + boxed + html[end_idx:]


def _inject_mid_coupang(html: str, card_html: str) -> str:
    """본문 h2 중 가운데(N//2번째) 직전에 카드를 삽입. h2가 1개 이하면 원본 반환."""
    positions = []
    start = 0
    while True:
        pos = html.find("<h2", start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 1
    if len(positions) < 2:
        return html
    target = positions[len(positions) // 2]
    return html[:target] + card_html + html[target:]


def _build_coupang_block(products: list[dict]) -> str:
    p = products[0]
    image_html = ""
    if p.get("image_url"):
        image_html = (
            f'<img src="{p["image_url"]}" alt="{p["name"]}" '
            'style="width:80px;height:160px;object-fit:cover;'
            'border-radius:4px;flex-shrink:0;">'
        )
    text_block = (
        f'<strong style="font-size:15px;display:block;margin-bottom:4px;">{p["name"]}</strong>'
        f'<span style="font-size:13px;color:#666;display:block;margin-bottom:8px;">{p["desc"]}</span>'
        '<span style="font-size:11px;color:#e74c3c;">COUPANG</span>'
    )
    padding = "12px" if image_html else "0"
    inner = (
        f'{image_html}'
        f'<div style="padding-left:{padding}">{text_block}</div>'
    )
    return (
        '<div style="border-top:1px solid #eee;margin-top:40px;padding-top:20px;">'
        '<p style="font-size:13px;color:#e74c3c;font-weight:bold;margin-bottom:10px;">'
        '* 이 게시물은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.'
        '</p>'
        f'<a href="{p["url"]}" target="_blank" rel="noopener sponsored" referrerpolicy="unsafe-url" '
        'style="display:flex;align-items:center;background:#fff;border:1px solid #e0e0e0;'
        'border-radius:8px;padding:16px 20px;text-decoration:none;color:#333;max-width:420px;">'
        f'{inner}'
        '</a>'
        '</div>'
    )
