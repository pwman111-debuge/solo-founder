# 호칭 규칙

- 황원장님은 나(Claude Code)를 **우팀장**이라고 부른다.
- 나(Claude Code)는 사용자를 **황원장님**이라고 부른다.

---

# 프로젝트 개요

**1인 인터넷 사업 — 월 수익 1,000만원 달성**

- 황원장님(내과 전문의)이 진료 외 시간에 운영하는 1인 인터넷 수익화 프로젝트
- 핵심 채널: **doctorhwang.tistory.com** (건강 콘텐츠 블로그)
- 수익 구조: 애드센스 + 쿠팡파트너스 영양제 제휴
- 목표: **12개월 내 월 1,000만원**

### 핵심 자산
- doctorhwang.tistory.com — 애드센스 승인 완료, 222편+ 누적, 의사 신뢰도 (E-E-A-T)
- tistory-automation 파이프라인 — 키워드 선택 → 글 생성 → 티스토리 발행 → Threads/LinkedIn 동시 발행
- Playwright — SNS 자동 포스팅 운영 중
- GitHub: https://github.com/pwman111-debuge/solo-founder

### 수익화 전략
- 건강 키워드 타게팅 (월 검색량 1만+) → SEO 트래픽 유입
- 일 2~3편 반자동 발행 (황원장님 트리거 → 자동 실행)
- 유사투자자문업 해당 없음

### 수익 목표
| 시점 | 일 방문 | 월 수익 |
|------|---------|--------|
| 6개월 | 3,500명 | 400만원 |
| 12개월 | 12,000명 | 1,400만원 |

---

# 운영 방식

- **반자동 트리거**: 황원장님이 병원에서 딸깍 → 자동 실행 (완전 자동화 X)
- 황원장님 일일 투자 시간: **5~8분** (트리거 + 검수)
- 콘텐츠 검수 필수 — 의사 검수가 신뢰도 핵심

---

# 기술 스택

| 역할 | 도구 |
|------|------|
| 콘텐츠 생성 | Claude Code CLI (`claude -p`, Max*5 구독 내 처리) |
| 이미지 생성 | 미사용 (품질 문제로 제외) |
| 포맷 변환 | markdown-it-py → 티스토리 HTML |
| 자동 발행 | Playwright → 티스토리 |
| SNS 발행 | Threads Graph API + LinkedIn UGC Posts API |
| 제휴 카드 | 쿠팡파트너스 — 모든 글에 1개 필수 삽입 |

---

# 프로젝트 폴더 구조

```
1인창업/
├── CLAUDE.md
└── tistory-automation/
    ├── post_tistory.py              ← 진입점
    ├── .env                         ← API 키, 계정 정보 (git 제외)
    ├── .env.example
    ├── requirements.txt
    ├── run.bat
    ├── config/
    │   ├── keywords.csv             ← 건강 키워드 (used 컬럼으로 중복 방지)
    │   └── coupang_links.py         ← 카테고리별 쿠팡 링크 + 이미지 URL
    ├── modules/
    │   ├── keyword_picker.py
    │   ├── content_generator.py     ← Claude CLI로 글 생성
    │   ├── html_converter.py        ← Markdown → HTML + 쿠팡 카드
    │   ├── tistory_poster.py        ← Playwright 발행
    │   ├── threads_poster.py        ← Threads Graph API
    │   └── linkedin_poster.py       ← LinkedIn UGC API
    └── logs/
        └── post_log.csv
```

## 실행 명령어

```bash
# 기본 3편 발행
python post_tistory.py

# 1편만 발행
python post_tistory.py --count 1

# 키워드 직접 지정
python post_tistory.py --keyword "마그네슘 효능" --count 1
```

---

# 코드 규칙

- MUST: 변수/함수명은 명확하고 의미 있게 작성
- MUST NOT: 불필요한 주석 작성 금지
- MUST NOT: 요청 범위를 벗어난 추가 구현 금지
- MUST: 코드 수정 후 즉시 GitHub(`solo-founder` repo)로 push

---

# 응답 스타일

- 답변은 간결하고 핵심만 전달
- 코드 참조 시 파일 경로와 라인 번호 함께 표기
- 불필요한 설명이나 반복 요약 금지
- "go!" 한 마디면 바로 실행 — 사전 설명 최소화
- 단계별로 진행하며 각 단계마다 다음 행동만 간결하게 안내

---

# 작업 경험 메모

## Cloudflare Pages
- `public/_redirects` — 절대 URL 소스 사용 불가, relative URL만 허용
- 도메인 간 301 리다이렉트 → Cloudflare Bulk Redirects (대시보드)에서 설정

## AdSense
- Next.js `Script strategy="afterInteractive"` → 구글 크롤러 감지 못함
- AdSense 스크립트는 `<head>` 안에 raw `<script>` 태그로 직접 삽입

## 티스토리 자동화
- 티스토리 OpenAPI 2014년 종료 → Playwright 브라우저 자동화로 대체
- 봇 감지 약함, 캡차 거의 없음 → 안정적 자동화 가능
- TinyMCE 에디터: `tinymce.activeEditor.setContent()` + `save()` 로 본문 주입
- 발행 후 URL: RSS 폴링(`/rss`)으로 새 포스트 URL 추출

## Claude Code CLI 콘텐츠 생성
- `claude -p --output-format json` + stdin으로 프롬프트 전달
- claude.cmd 경로: `C:\Users\hwang\AppData\Roaming\npm\claude.cmd`
- Max*5 구독 내 처리 — 별도 API 키 불필요

## 쿠팡파트너스
- 승인 신청 완료 (2026-05-03), 심사 중
- 링크 설정된 카테고리: 비타민D, 오메가3, 마그네슘, 종합비타민
- 나머지 카테고리는 TODO → 승인 후 링크 채울 것
- 모든 글에 쿠팡 카드 1개 필수 삽입 (관련 카테고리 우선, 없으면 범용 폴백)
- 고지 문구는 하단 카드에만 표시 (상단 중복 제거)
