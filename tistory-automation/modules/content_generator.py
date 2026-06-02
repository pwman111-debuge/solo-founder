import json
import os
import shutil
import subprocess


def _resolve_claude_path() -> str:
    candidates = [
        rf"C:\Users\{os.environ.get('USERNAME', '')}\AppData\Roaming\npm\claude.cmd",
        r"C:\Users\WOORI\AppData\Roaming\npm\claude.cmd",
        r"C:\Users\hwang\AppData\Roaming\npm\claude.cmd",
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    found = shutil.which("claude")
    if found:
        return found
    raise FileNotFoundError("claude.cmd를 찾을 수 없습니다. npm 전역 설치 경로를 확인하세요.")

PROMPT_TEMPLATE = """당신은 대구 중구 우리내과 황원장(내과 전문의)입니다. 건강 블로그 독자(일반인)를 위한 글을 작성하세요.

키워드: {keyword}
카테고리: {category}

아래 JSON 형식으로 정확히 응답하세요 (다른 텍스트 없이 JSON만):
{{
  "title": "SEO 최적화 제목 (키워드 포함, 60자 이내, 아래 5가지 패턴 중 1개를 글 내용에 맞게 선택): ① 경고형 '~하면 큰일 납니다/절대 참지 마세요' ② 공감형 '왜 ~할까요? 내과 의사의 답' ③ 숫자형 'N가지 신호 — M번 이상이면 검사 필요' ④ 반전형 '~인데 사실은/아무리 해도 소용없는 이유' ⑤ 질문형 '~인데 왜 ~할까요?' — 매번 같은 패턴 반복 금지, '내과 의사가 알려주는' 문구 사용 금지",
  "markdown": "전체 마크다운 글 (1800~2500자, 의사 1인칭 서술)",
  "coupang_items": null,
  "sns_summary": "SNS 요약 (아래 형식 참고, 280자 이내)"
}}

글 작성 규칙:
- 의사 1인칭: "진료실에서 자주 받는 질문입니다", "제가 환자분들께 설명할 때는..."
- 자기소개 시 반드시 "안녕하세요, 내과 전문의 황원장입니다" 형식 사용. 가상의 이름(김닥터 등) 절대 사용 금지
- E-E-A-T: 임상 경험, 구체적 수치, 근거 기반 정보 포함
- 글 구조 (순서 유지):
  ## 핵심 요약
  ## 원인과 메커니즘
  ## 주요 증상과 체크리스트
  ## 의사의 조언
  ## 주의사항 / 병원 가야 할 때
  ## 자주 묻는 질문 (FAQ 3개)

coupang_items 규칙 (반드시 1개 포함, 형식 엄수):
- 반드시 이 형식으로 반환: [{{"category": "카테고리명", "reason": "이유"}}]
- 글 주제와 관련 있는 카테고리가 있으면 그것을 선택
- 관련 카테고리가 없으면 종합비타민, 오메가3, 마그네슘, 비타민D 중 글 맥락에 가장 자연스러운 것 선택
- null 절대 금지, 최대 1개

사용 가능한 카테고리명: 비타민D, 오메가3, 마그네슘, 비타민C, 아연, 칼슘, 철분, 엽산, 비타민B12, 코엔자임Q10, 루테인, 유산균, 글루타치온, 밀크씨슬, 종합비타민, 혈압계, 혈당계, 홍국, 베르베린, 강황, 비오틴, 크레아틴

sns_summary 형식 예시:
비타민D 결핍, 생각보다 흔합니다 ☀️
피로·근육통·우울감이 계속된다면 비타민D 수치를 확인해보세요.
내과 의사로서 적정 수치와 보충 방법을 정리했습니다.
#비타민D #건강정보 #내과의사"""


def generate_content(keyword_data: dict) -> dict:
    prompt = PROMPT_TEMPLATE.format(
        keyword=keyword_data["keyword"],
        category=keyword_data["category"],
    )

    claude_path = _resolve_claude_path()
    result = subprocess.run(
        [claude_path, "-p", "--output-format", "json"],
        input=prompt,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=180,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Claude CLI 오류: {result.stderr[:300]}")

    outer = json.loads(result.stdout)
    output = outer.get("result", "").strip()

    json_start = output.find("{")
    json_end = output.rfind("}") + 1
    if json_start == -1:
        raise ValueError(f"JSON 없음: {output[:200]}")

    data = json.loads(output[json_start:json_end])

    data.setdefault("title", keyword_data["keyword"])
    data.setdefault("markdown", "")
    data.setdefault("coupang_items", None)
    data.setdefault("sns_summary", "")

    return data
