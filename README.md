# BigTech AI News Aggregator

빅테크 기업들의 AI 관련 뉴스와 연구 발표를 한 곳에서 볼 수 있는 웹사이트입니다.

## ✨ 특징

- 🔄 매일 자동 업데이트 (GitHub Actions)
- 🔍 통합 검색 기능
- 🏷️ 회사별 필터링
- 📱 반응형 디자인
- 🚀 GitHub Pages로 무료 호스팅

## 📊 모니터링 대상

### ✅ 활성화된 소스 (12개)

| 회사 | URL | 수집 방식 | 상태 | 날짜 추출 |
|------|-----|----------|------|----------|
| **Google Research** | https://research.google/blog/ | RSS | ✅ 작동 (50개 수집) | ✅ 완벽 |
| **Google DeepMind** | https://deepmind.google/research/publications | HTML | ✅ 작동 (20개 수집) | ✅ 완벽 ⭐ |
| **NVIDIA Blog** | https://blogs.nvidia.com/ | RSS | ✅ 작동 (18개 수집) | ✅ 완벽 |
| **DeepSeek** | https://api-docs.deepseek.com | HTML | ✅ 작동 (12개 수집) | ✅ 완벽 |
| **Microsoft Research** | https://www.microsoft.com/en-us/research/ | RSS | ✅ 작동 (10개 수집) | ✅ 완벽 |
| **Microsoft AI News** | https://news.microsoft.com/source/topics/ai/ | RSS | ✅ 작동 (10개 수집) | ✅ 완벽 |
| **DeepSeek Blog** | https://deepseek.ai/blog | Sitemap | ✅ 작동 (8개 수집) | ✅ 완벽 🆕 |
| **Qwen** | https://qwenlm.github.io/blog/ | HTML | ✅ 작동 (5개 수집) | ✅ 완벽 |
| **Meta AI** | https://ai.meta.com/blog/ | HTML | ✅ 작동 (5개 수집) | ⚠️ React 렌더링 |
| **Anthropic** | https://www.anthropic.com/news | HTML | ✅ 작동 (4개 수집) | ✅ 완벽 |
| **Google AI** | https://ai.google | HTML | ✅ 작동 (3개 수집) | ⚠️ 최소 정보 |
| **NVIDIA News** | https://nvidianews.nvidia.com/ | HTML | ✅ 작동 (1개 수집) | ⚠️ 추출 실패 |

**총 수집 기사: 146개** (196개 수집 → 중복 제거 후 196개 → 소스당 제한 적용 후 146개)
**날짜 추출: 137개 (94%)** ⭐ - Sitemap 기반 DeepSeek Blog 추가로 더욱 개선!

### ⚠️ 문제 있는 소스 (1개)

| 회사 | 상태 | 설명 |
|------|------|------|
| **LG AI Research** | ⚠️ 0개 수집 | HTML 구조 변경으로 스크래퍼 수정 필요 |

### 🔍 비활성화된 소스 (3개)

| 회사 | 상태 | 이유 |
|------|------|------|
| **OpenAI** | ❌ 비활성화 | 403 에러 - 접근 제한 |
| **xAI** | ❌ 비활성화 | 403 에러 - 접근 제한 |
| **LG AI Research** | ⚠️ 수정 필요 | Nuxt.js 동적 렌더링 - Playwright/Selenium 필요 |

## 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 데이터 수집

```bash
python main.py
```

### 3. 로컬에서 웹사이트 보기

```bash
cd docs
python -m http.server 8000
```

브라우저에서 `http://localhost:8000` 접속

**참고**: `python main.py` 실행 시 자동으로 `docs/data/news.json`이 생성되어 로컬 서버에서 바로 접근 가능합니다.

## 프로젝트 구조

```
Big Tech News/
├── scrapers/          # 각 소스별 스크래퍼
├── data/             # 수집된 JSON 데이터
├── docs/             # GitHub Pages 사이트
├── .github/workflows/ # 자동화
├── config.yaml       # 설정 파일
└── main.py          # 메인 스크립트
```

## 윤리적 사용

- robots.txt 규칙 준수
- Rate limiting 적용 (최소 1.5초 간격)
- 명확한 User-Agent 식별
- 원문 링크 제공
- 저작권 표시

## 라이선스

MIT License
