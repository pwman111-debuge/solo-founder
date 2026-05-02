"""
카테고리별 쿠팡파트너스 제품 링크.
쿠팡파트너스 가입 후 링크를 발급받아 url 필드를 채워주세요.
.env에서 COUPANG_ENABLED=True 로 변경하면 활성화됩니다.
"""

COUPANG_LINKS: dict[str, list[dict]] = {
    "비타민D": [
        {"name": "메가도스 D 비타민D3 4000IU", "desc": "햇빛 부족 시 권장 보충량, 흡수율 좋은 연질캡슐", "url": "https://link.coupang.com/a/eA9n85", "image_url": "https://img1a.coupangcdn.com/image/affiliate/banner/661a66549afeb273dbb00090d5579a85@2x.jpg"},
        {"name": "비타민D3+K2 복합", "desc": "비타민K2와 함께 섭취 시 칼슘 흡수 최적화", "url": "https://link.coupang.com/TODO"},
    ],
    "오메가3": [
        {"name": "뉴트리디데이 슈퍼 피쉬오일 오메가3", "desc": "EPA+DHA 고함량, 혈행 개선 필수 지방산", "url": "https://link.coupang.com/a/eA9tFO", "image_url": "https://img4a.coupangcdn.com/image/affiliate/banner/c04a77ca0e95e328e7146f3620a6205b@2x.jpg"},
        {"name": "크릴오일", "desc": "인지질 형태 오메가3, 위 부담 적음", "url": "https://link.coupang.com/TODO"},
    ],
    "마그네슘": [
        {"name": "뉴트리디데이 프리미엄 마그네슘 400", "desc": "수면 질 개선·근육 이완, 피로 회복 지원", "url": "https://link.coupang.com/a/eA9w6m", "image_url": "https://img3a.coupangcdn.com/image/affiliate/banner/eff36d36b295b1db5d488c48ac519a39@2x.jpg"},
        {"name": "마그네슘+B6 복합", "desc": "신경계 지원, 두통·근육 경련 완화", "url": "https://link.coupang.com/TODO"},
    ],
    "비타민C": [
        {"name": "고함량 비타민C 1000mg", "desc": "산화 스트레스 방어, 면역력 지원", "url": "https://link.coupang.com/TODO"},
        {"name": "리포소말 비타민C", "desc": "리포좀 캡슐로 흡수율 극대화", "url": "https://link.coupang.com/TODO"},
    ],
    "아연": [
        {"name": "아연 25mg", "desc": "면역·피부·남성 건강 지원", "url": "https://link.coupang.com/TODO"},
    ],
    "칼슘": [
        {"name": "칼슘+마그네슘+비타민D", "desc": "뼈 건강 3종 세트, 균형 잡힌 비율", "url": "https://link.coupang.com/TODO"},
    ],
    "철분": [
        {"name": "철분 헴철 18mg", "desc": "헴철 형태로 흡수율 높음, 위장 자극 최소화", "url": "https://link.coupang.com/TODO"},
    ],
    "엽산": [
        {"name": "활성형 엽산 (메틸폴레이트)", "desc": "MTHFR 유전자 변이에도 활용 가능한 활성형", "url": "https://link.coupang.com/TODO"},
    ],
    "비타민B12": [
        {"name": "메틸코발라민 B12", "desc": "활성형 B12, 신경 보호·피로 회복", "url": "https://link.coupang.com/TODO"},
    ],
    "코엔자임Q10": [
        {"name": "유비퀴놀 코큐텐 100mg", "desc": "환원형 CoQ10, 40대 이상 흡수율 우수", "url": "https://link.coupang.com/TODO"},
    ],
    "루테인": [
        {"name": "루테인+지아잔틴 20mg", "desc": "황반변성 예방, 눈 피로 회복", "url": "https://link.coupang.com/TODO"},
    ],
    "유산균": [
        {"name": "프로바이오틱스 100억 CFU", "desc": "다균주 복합 유산균, 장 환경 개선", "url": "https://link.coupang.com/TODO"},
        {"name": "신바이오틱스 (유산균+프리바이오틱스)", "desc": "먹이 포함으로 정착률 향상", "url": "https://link.coupang.com/TODO"},
    ],
    "글루타치온": [
        {"name": "리포소말 글루타치온", "desc": "강력 항산화, 해독 지원", "url": "https://link.coupang.com/TODO"},
    ],
    "밀크씨슬": [
        {"name": "밀크씨슬 실리마린 80%", "desc": "간세포 보호, 알코올 해독 지원", "url": "https://link.coupang.com/TODO"},
    ],
    "종합비타민": [
        {"name": "고려은단 멀티비타민 올인원", "desc": "26종 영양소 한 알에, 식사 대용 기초 보충", "url": "https://link.coupang.com/a/eA9z39", "image_url": "https://image7.coupangcdn.com/image/affiliate/banner/7f200c3c37119030cef29ad65b35beea@2x.jpg"},
    ],
    "혈압계": [
        {"name": "가정용 자동 혈압계", "desc": "의사 권고: 가정 혈압 측정이 진료실보다 정확", "url": "https://link.coupang.com/TODO"},
    ],
    "혈당계": [
        {"name": "가정용 혈당측정기 세트", "desc": "공복·식후 혈당 자가 모니터링 필수 도구", "url": "https://link.coupang.com/TODO"},
    ],
    "홍국": [
        {"name": "홍국 코큐텐 복합", "desc": "콜레스테롤 관리, 스타틴 대체 자연 성분", "url": "https://link.coupang.com/TODO"},
    ],
    "베르베린": [
        {"name": "베르베린 500mg", "desc": "혈당·콜레스테롤 조절, 자연 유래 성분", "url": "https://link.coupang.com/TODO"},
    ],
    "강황": [
        {"name": "커큐민 BCM-95 500mg", "desc": "흡수율 높인 강황 추출물, 항염 효과", "url": "https://link.coupang.com/TODO"},
    ],
    "비오틴": [
        {"name": "비오틴 10000mcg", "desc": "탈모·손발톱 강화, 피부 케라틴 합성 지원", "url": "https://link.coupang.com/TODO"},
    ],
    "크레아틴": [
        {"name": "크레아틴 모노하이드레이트", "desc": "근육 합성·운동 능력 향상", "url": "https://link.coupang.com/TODO"},
    ],
}

CATEGORY_KEYWORD_MAP: dict[str, list[str]] = {
    "비타민D": ["비타민d", "비타민 d", "비타민디"],
    "오메가3": ["오메가3", "오메가-3", "epa", "dha"],
    "마그네슘": ["마그네슘"],
    "비타민C": ["비타민c", "비타민 c"],
    "아연": ["아연"],
    "칼슘": ["칼슘", "뼈 건강", "골다공증"],
    "철분": ["철분", "빈혈"],
    "엽산": ["엽산"],
    "비타민B12": ["비타민b12", "b12"],
    "코엔자임Q10": ["코엔자임", "코큐텐", "q10"],
    "루테인": ["루테인", "눈 건강", "황반"],
    "유산균": ["유산균", "프로바이오틱스", "장 건강"],
    "글루타치온": ["글루타치온"],
    "밀크씨슬": ["밀크씨슬", "간 건강", "지방간"],
    "종합비타민": ["종합비타민"],
    "혈압계": ["고혈압", "혈압"],
    "혈당계": ["당뇨", "혈당", "공복혈당"],
    "홍국": ["홍국", "콜레스테롤", "고지혈증"],
    "베르베린": ["베르베린"],
    "강황": ["강황", "커큐민", "염증"],
    "비오틴": ["비오틴", "탈모"],
    "크레아틴": ["크레아틴"],
}


FALLBACK_CATEGORIES = ["종합비타민", "오메가3", "마그네슘", "비타민D"]


def _valid_products(category: str) -> list[dict]:
    return [p for p in COUPANG_LINKS.get(category, []) if "TODO" not in p["url"]]


def get_coupang_items(category_names: list[str]) -> list[dict]:
    """요청 카테고리 우선, 유효 상품 없으면 범용 카테고리로 폴백."""
    for cat in category_names:
        products = _valid_products(cat)
        if products:
            return products[:1]

    for cat in FALLBACK_CATEGORIES:
        if cat not in category_names:
            products = _valid_products(cat)
            if products:
                return products[:1]

    return []
