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
        {"name": "고려은단 멀티비타민 올인원 맨 60+", "desc": "산화 스트레스 방어, 면역력 지원", "url": "https://link.coupang.com/a/eBnBCN", "image_url": "https://image12.coupangcdn.com/image/affiliate/banner/64d2fbe96e9a977f7a6924516fb4d572@2x.jpg"},
    ],
    "아연": [
        {"name": "아연 25mg", "desc": "면역·피부·남성 건강 지원", "url": "https://link.coupang.com/TODO"},
    ],
    "칼슘": [
        {"name": "내츄럴플러스 상어연골 칼슘 180정", "desc": "뼈 건강 필수 칼슘, 흡수율 높은 상어연골 원료", "url": "https://link.coupang.com/a/eBnELW", "image_url": "https://image7.coupangcdn.com/image/affiliate/banner/41b67a9c296edbc79c6cf5f58a4729a1@2x.jpg"},
    ],
    "철분": [
        {"name": "비타할로 철분 90정", "desc": "헴철 형태로 흡수율 높음, 위장 자극 최소화", "url": "https://link.coupang.com/a/eBnHi3", "image_url": "https://img3a.coupangcdn.com/image/affiliate/banner/dc2bc9b4da864b25d45ed5dda09ebcff@2x.jpg"},
    ],
    "엽산": [
        {"name": "활성형 엽산 (메틸폴레이트)", "desc": "MTHFR 유전자 변이에도 활용 가능한 활성형", "url": "https://link.coupang.com/TODO"},
    ],
    "비타민B12": [
        {"name": "메틸코발라민 B12 1000mcg 120정", "desc": "활성형 B12, 신경 보호·피로 회복", "url": "https://link.coupang.com/a/eBnK9N", "image_url": "https://image2.coupangcdn.com/image/affiliate/banner/23da7d96884fd60c30833524728e7624@2x.jpg"},
    ],
    "코엔자임Q10": [
        {"name": "유비퀴놀 코큐텐 100mg", "desc": "환원형 CoQ10, 40대 이상 흡수율 우수", "url": "https://link.coupang.com/TODO"},
    ],
    "루테인": [
        {"name": "뉴트리정 프리미엄 눈건강 루테인 300정", "desc": "황반변성 예방, 눈 피로 회복", "url": "https://link.coupang.com/a/eBnzuv", "image_url": "https://image11.coupangcdn.com/image/affiliate/banner/80f0262e8a2243c136268bb7fd7e3e8a@2x.jpg"},
    ],
    "유산균": [
        {"name": "GNC 비피도 핏 다이어트 유산균", "desc": "다균주 복합 유산균, 장 환경 개선", "url": "https://link.coupang.com/a/eBntGq", "image_url": "https://image4.coupangcdn.com/image/affiliate/banner/0c62cb5612d01febefe11b99ad5f4e45@2x.jpg"},
    ],
    "글루타치온": [
        {"name": "리포소말 글루타치온", "desc": "강력 항산화, 해독 지원", "url": "https://link.coupang.com/TODO"},
    ],
    "밀크씨슬": [
        {"name": "센트휴 수퍼 알부민 밀크씨슬 90", "desc": "간세포 보호, 알코올 해독 지원", "url": "https://link.coupang.com/a/eBnxkt", "image_url": "https://image7.coupangcdn.com/image/affiliate/banner/ad0e0f4ccd7f4b680fb8ffa0d48e371b@2x.jpg"},
    ],
    "종합비타민": [
        {"name": "고려은단 멀티비타민 올인원", "desc": "26종 영양소 한 알에, 식사 대용 기초 보충", "url": "https://link.coupang.com/a/eA9z39", "image_url": "https://image7.coupangcdn.com/image/affiliate/banner/7f200c3c37119030cef29ad65b35beea@2x.jpg"},
    ],
    "혈압계": [
        {"name": "가정용 자동 혈압계", "desc": "의사 권고: 가정 혈압 측정이 진료실보다 정확", "url": "https://link.coupang.com/TODO"},
    ],
    "혈당계": [
        {"name": "케어센스 혈당측정기+시험지110매", "desc": "공복·식후 혈당 자가 모니터링 필수 도구", "url": "https://link.coupang.com/a/eBnmby", "image_url": "https://image5.coupangcdn.com/image/affiliate/banner/00a3bbb569b23c3816ccffdb93c69477@2x.jpg"},
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
        {"name": "닥터스베스트 비오틴 10000mcg 120정", "desc": "탈모·손발톱 강화, 피부 케라틴 합성 지원", "url": "https://link.coupang.com/a/eBnJlU", "image_url": "https://img5c.coupangcdn.com/image/affiliate/banner/288e1229fc87e89def75700b1ae82bff@2x.jpg"},
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
