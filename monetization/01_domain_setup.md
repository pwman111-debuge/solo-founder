# PHASE 1 — 도메인 구매 및 교체

## 도메인 후보

| 후보 | 추천도 | 이유 |
|------|--------|------|
| `genesisreport.com` | ⭐⭐⭐ 1순위 | 브랜드명 일치, 애드센스 신뢰도 높음 |
| `genesisstock.com` | ⭐⭐ 2순위 | 대안 |

---

## Step 1 — Cloudflare Registrar에서 도메인 구매

1. [dash.cloudflare.com](https://dash.cloudflare.com) 로그인
2. 좌측 메뉴 → **Domain Registration** → **Register Domains**
3. 원하는 도메인 검색
4. 구매 (연 $10.44, 자동갱신 설정 권장)

---

## Step 2 — Cloudflare Pages에 커스텀 도메인 연결

1. Cloudflare 대시보드 → **Workers & Pages**
2. 현재 프로젝트 선택
3. **Custom domains** 탭 → **Set up a custom domain**
4. 구매한 도메인 입력 → DNS 레코드 자동 생성됨
5. DNS 전파 대기 (30분~24시간)

---

## Step 3 — 확인 사항

- [ ] 커스텀 도메인으로 사이트 정상 접속
- [ ] HTTPS 인증서 자동 발급 완료 (`https://` 자물쇠 아이콘 확인)
- [ ] 기존 `pages.dev` URL도 여전히 작동하는지 확인 (리다이렉트 설정 옵션)

---

## 비용

- 도메인: 연 $10.44 (약 14,000원)
- Cloudflare Pages 호스팅: 무료 유지

---

## 완료 후 다음 단계

→ [02_linkprice.md](02_linkprice.md)로 이동
