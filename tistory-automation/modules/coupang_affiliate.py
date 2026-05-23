"""쿠팡파트너스 OpenAPI 광고 발급 모듈 (건강 카테고리 전용).

엔드포인트:
  GET  /v2/providers/affiliate_open_api/apis/openapi/v1/products/search
  POST /v2/providers/affiliate_open_api/apis/openapi/v1/deeplink

필요 env:
  COUPANG_ACCESS_KEY
  COUPANG_SECRET_KEY
"""
import hashlib
import hmac
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone

ACCESS_KEY = os.getenv("COUPANG_ACCESS_KEY", "")
SECRET_KEY = os.getenv("COUPANG_SECRET_KEY", "")
DOMAIN = "https://api-gateway.coupang.com"


CATEGORY_SEARCH_MAP: dict[str, str] = {
    "비타민D": "비타민D 영양제",
    "오메가3": "오메가3",
    "마그네슘": "마그네슘 영양제",
    "비타민C": "비타민C 영양제",
    "아연": "아연 영양제",
    "칼슘": "칼슘 영양제",
    "철분": "철분제",
    "엽산": "엽산 영양제",
    "비타민B12": "비타민B12",
    "코엔자임Q10": "코엔자임 Q10",
    "루테인": "루테인",
    "유산균": "프로바이오틱스 유산균",
    "글루타치온": "글루타치온",
    "밀크씨슬": "밀크씨슬",
    "종합비타민": "종합비타민",
    "혈압계": "가정용 혈압계",
    "혈당계": "혈당측정기",
    "홍국": "홍국 영양제",
    "베르베린": "베르베린",
    "강황": "강황 커큐민",
    "비오틴": "비오틴",
    "크레아틴": "크레아틴",
}

FALLBACK_QUERY = "종합비타민"


def get_search_query(category: str) -> str:
    return CATEGORY_SEARCH_MAP.get(category, f"{category} 영양제")


def _generate_authorization(method: str, path_with_query: str) -> str:
    parts = path_with_query.split("?", 1)
    path = parts[0]
    query = parts[1] if len(parts) > 1 else ""
    datetime_str = datetime.now(timezone.utc).strftime("%y%m%dT%H%M%SZ")
    message = datetime_str + method + path + query
    signature = hmac.new(
        SECRET_KEY.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return (
        f"CEA algorithm=HmacSHA256, access-key={ACCESS_KEY}, "
        f"signed-date={datetime_str}, signature={signature}"
    )


def _api_call(method: str, path_with_query: str, body: dict | None = None) -> dict:
    authorization = _generate_authorization(method, path_with_query)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(DOMAIN + path_with_query, data=data, method=method)
    req.add_header("Authorization", authorization)
    req.add_header("Content-Type", "application/json;charset=UTF-8")
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))


def search_products(keyword: str, limit: int = 5) -> list[dict]:
    """검색어로 상품 최대 limit개 반환.

    각 dict: {"product_name", "affiliate_url", "image_url", "product_price"}
    """
    if not ACCESS_KEY or not SECRET_KEY:
        print("  [쿠팡] COUPANG_ACCESS_KEY/SECRET_KEY 미설정")
        return []

    encoded = urllib.parse.quote(keyword)
    path = (
        "/v2/providers/affiliate_open_api/apis/openapi/v1/products/search"
        f"?keyword={encoded}&limit={limit}"
    )
    try:
        result = _api_call("GET", path)
    except Exception as e:
        print(f"  [쿠팡] '{keyword}' 검색 실패: {e}")
        return []

    if str(result.get("rCode", "")) != "0":
        print(f"  [쿠팡] API 오류: {result.get('rMessage')}")
        return []

    products = result.get("data", {}).get("productData", []) or []
    items: list[dict] = []
    needs_deeplink: list[tuple[int, str]] = []
    for idx, p in enumerate(products):
        product_url = p.get("productUrl", "")
        if product_url and "link.coupang.com" not in product_url:
            needs_deeplink.append((idx, product_url))
        items.append({
            "product_name": p.get("productName", ""),
            "affiliate_url": product_url,
            "image_url": p.get("productImage", ""),
            "product_price": p.get("productPrice", 0),
        })
    if needs_deeplink:
        converted = _convert_to_deeplink([u for _, u in needs_deeplink])
        for (idx, _), short in zip(needs_deeplink, converted):
            if short:
                items[idx]["affiliate_url"] = short
    return items


def _convert_to_deeplink(coupang_urls: list[str]) -> list[str]:
    if not coupang_urls:
        return []
    path = "/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink"
    try:
        result = _api_call("POST", path, {"coupangUrls": coupang_urls})
    except Exception as e:
        print(f"  [쿠팡] deeplink 변환 실패: {e}")
        return []
    if str(result.get("rCode", "")) != "0":
        print(f"  [쿠팡] deeplink API 오류: {result.get('rMessage')}")
        return []
    items = result.get("data", []) or []
    return [item.get("shortenUrl", "") for item in items]


def fetch_products_for_category(category: str, limit: int = 2) -> list[dict]:
    """카테고리명으로 쿠팡 상품 limit개 반환. 검색 결과 없으면 폴백 검색어로 재시도."""
    query = get_search_query(category)
    items = search_products(query, limit=max(limit, 5))
    if not items and FALLBACK_QUERY != query:
        print(f"  [쿠팡] '{query}' 결과 없음 → fallback '{FALLBACK_QUERY}' 시도")
        items = search_products(FALLBACK_QUERY, limit=max(limit, 5))

    picked: list[dict] = []
    seen_urls: set[str] = set()
    for it in items:
        url = it.get("affiliate_url", "")
        if not url or url in seen_urls:
            continue
        picked.append(it)
        seen_urls.add(url)
        if len(picked) >= limit:
            break
    return picked


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    from dotenv import load_dotenv
    from pathlib import Path
    load_dotenv(Path(__file__).parent.parent / ".env")
    ACCESS_KEY = os.getenv("COUPANG_ACCESS_KEY", "")
    SECRET_KEY = os.getenv("COUPANG_SECRET_KEY", "")

    print("=== 카테고리별 검색어 ===")
    for cat in ["비타민D", "오메가3", "혈압계", "크레아틴"]:
        print(f"  {cat} → '{get_search_query(cat)}'")

    print("\n=== 실제 API 호출 (마그네슘 영양제) ===")
    products = fetch_products_for_category("마그네슘", limit=2)
    for i, p in enumerate(products, 1):
        print(f"  [{i}] {p['product_name']}")
        print(f"      가격: {p['product_price']:,}원")
        print(f"      URL: {p['affiliate_url']}")
        print(f"      이미지: {p['image_url']}")
