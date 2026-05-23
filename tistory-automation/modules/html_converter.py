import os
import sys
import html
from pathlib import Path
from markdown_it import MarkdownIt

sys.path.insert(0, str(Path(__file__).parent.parent))
from modules.coupang_affiliate import fetch_products_for_category

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
    "font-size:14px;font-weight:bold;color:#c0392b;"
    "background:#fff3cd;border:1px solid #f0ad4e;border-radius:4px;"
    "padding:12px 16px;margin-bottom:24px;display:block;"
)


def convert_to_html(markdown_text: str, coupang_items_meta: list | None) -> str:
    body_html = md.render(markdown_text)
    body_html = _style_summary_box(body_html)

    coupang_top = ""
    coupang_bottom = ""
    if COUPANG_ENABLED and coupang_items_meta:
        category = coupang_items_meta[0].get("category", "") if isinstance(coupang_items_meta[0], dict) else str(coupang_items_meta[0])
        if category:
            products = fetch_products_for_category(category, limit=2)
            if products:
                coupang_top = (
                    f'<p style="{COUPANG_TOP_NOTICE_STYLE}">'
                    "[광고] 이 포스팅은 쿠팡 파트너스 활동의 일환으로, "
                    "이에 따른 일정액의 수수료를 제공받습니다."
                    "</p>"
                )
                coupang_bottom = _build_coupang_block(products[0], position="bottom")
                if len(products) >= 2:
                    body_html = _inject_mid_coupang(body_html, _build_coupang_block(products[1], position="middle"))

    disclaimer = (
        f'<p style="{DISCLAIMER_STYLE}">'
        "본 내용은 의학적 참고 정보이며, 개인 진료를 대체하지 않습니다. "
        "증상이 지속되면 전문의 상담을 받으시기 바랍니다."
        "</p>"
    )

    return (
        f'<div style="{WRAPPER_STYLE}">'
        f"{coupang_top}"
        f"{body_html}"
        f"{coupang_bottom}"
        f"{disclaimer}"
        "</div>"
    )


def _style_summary_box(html: str) -> str:
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


def _inject_mid_coupang(body_html: str, card_html: str) -> str:
    positions = []
    start = 0
    while True:
        pos = body_html.find("<h2", start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 1
    if len(positions) < 2:
        return body_html
    target = positions[len(positions) // 2]
    return body_html[:target] + card_html + body_html[target:]


def _build_coupang_block(product: dict, position: str = "bottom") -> str:
    name = html.escape(product.get("product_name", ""), quote=False)
    name_attr = html.escape(product.get("product_name", ""), quote=True)
    url = html.escape(product.get("affiliate_url", ""), quote=True)
    img = html.escape(product.get("image_url", ""), quote=True)
    price = product.get("product_price", 0)
    price_text = f"{price:,}원" if isinstance(price, int) and price > 0 else "쿠팡 추천"

    image_html = (
        f'<img src="{img}" alt="{name_attr}" '
        'style="width:80px;height:160px;object-fit:cover;'
        'border-radius:4px;flex-shrink:0;">'
    ) if img else ""

    text_block = (
        f'<strong style="font-size:15px;display:block;margin-bottom:4px;">{name}</strong>'
        f'<span style="font-size:13px;color:#666;display:block;margin-bottom:8px;">{price_text}</span>'
        '<span style="font-size:11px;color:#e74c3c;">COUPANG</span>'
    )
    padding = "12px" if image_html else "0"
    inner = (
        f'{image_html}'
        f'<div style="padding-left:{padding}">{text_block}</div>'
    )

    if position == "bottom":
        wrapper_open = '<div style="border-top:1px solid #eee;margin-top:40px;padding-top:20px;">'
        notice = (
            '<p style="font-size:13px;color:#e74c3c;font-weight:bold;margin-bottom:10px;">'
            '* 이 게시물은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.'
            '</p>'
        )
    else:
        wrapper_open = '<div style="margin:32px 0;padding-top:8px;">'
        notice = (
            '<p style="font-size:11px;color:#aaa;margin-bottom:8px;">'
            '* 쿠팡 파트너스 활동 일환으로 수수료를 제공받을 수 있습니다.'
            '</p>'
        )

    return (
        f'{wrapper_open}'
        f'{notice}'
        f'<a href="{url}" target="_blank" rel="noopener sponsored" referrerpolicy="unsafe-url" '
        'style="display:flex;align-items:center;background:#fff;border:1px solid #e0e0e0;'
        'border-radius:8px;padding:16px 20px;text-decoration:none;color:#333;max-width:420px;">'
        f'{inner}'
        '</a>'
        '</div>'
    )
