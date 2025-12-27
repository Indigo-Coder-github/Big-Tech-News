# 프로젝트 요약

## BigTech AI News Aggregator - 구현 완료

### 📌 프로젝트 개요

주요 빅테크 기업들의 AI 관련 뉴스와 연구 발표를 자동으로 수집하고 한 눈에 볼 수 있는 웹사이트

### ✅ 구현된 기능

#### 1. 데이터 수집 (17개 소스 작동 중)

- **RSS 기반 (8개) - 날짜 추출 완벽 ✅**
  - Google Research: 50개 기사 수집
  - NVIDIA Blog: 18개 기사 수집
  - Microsoft Research: 10개 기사 수집
  - Microsoft AI News: 7개 기사 수집 (AI 키워드 필터링)
  - OpenAI: 50개 기사 수집
  - Amazon Science: 50개 기사 수집 🆕
  - IBM Research: 50개 기사 수집 🆕
  - Qwen: 44개 기사 수집

- **HTML/Sitemap 스크래핑 (9개) - 날짜 추출 대폭 개선! ⭐**
  - Google DeepMind: 30개 출판물 수집 ✅
  - DeepSeek: 13개 기사 수집 ✅
  - DeepSeek Blog: 15개 기사 수집 ✅
  - Baidu Research: 50개 기사 수집 🆕
  - Meta AI: 12개 기사 수집
  - Anthropic: 13개 기사 수집 ✅
  - Google Blog AI: 20개 기사 수집
  - LG AI Research: 30개 기사 수집 ✅ (API 방식으로 해결!)
  - NVIDIA News: 3개 기사 수집

**총 465개 기사 수집** ⭐
**17개 소스 모두 정상 작동!**

#### 2. 웹 UI

- 반응형 디자인 (모바일/데스크톱 대응)
- 실시간 검색 기능
- 회사별 필터링
- 날짜/소스별 정렬
- 목록형/카드형 뷰 전환 🆕
- 깔끔한 카드 레이아웃
- 회사별 브랜드 색상 및 로고

#### 3. 자동화

- GitHub Actions 워크플로우 설정
- 매일 자동 업데이트
- GitHub Pages 자동 배포

### 🔍 robots.txt 분석 결과

| 사이트 | robots.txt | 스크래핑 허용 여부 |
|--------|------------|-------------------|
| Google Research | 404 (없음) | ✅ 허용 (보수적 접근) |
| NVIDIA Blog | AI 에이전트 명시 허용 | ✅ 완전 허용 |
| Google AI | 완전 허용 (Allow: /) | ✅ 완전 허용 |
| OpenAI | 허용 (/microsoft-for-startups만 제외) | ✅ 허용 |
| Anthropic | 완전 허용 (Allow: /) | ✅ 완전 허용 |
| Meta AI | /blog 명시 제외 없음 | ✅ 허용 |
| Google DeepMind | 404 (없음) | ✅ 허용 (보수적 접근) |
| NVIDIA News | 허용 (/file만 제외) | ✅ 허용 |
| LG AI Research | 없음 (빈 응답) | ✅ 허용 (보수적 접근) |
| Amazon Science | 허용 (10초 crawl-delay) | ✅ 허용 🆕 |
| IBM Research | 허용 (/api, /images만 제외) | ✅ 허용 🆕 |
| Baidu Research | 완전 허용 (Disallow 없음) | ✅ 허용 🆕 |
| Microsoft News | 허용 (10초 crawl-delay) | ✅ 허용 🆕 |

### 📊 기술 스택

#### Backend

- Python 3.11+
- feedparser (RSS 파싱)
- BeautifulSoup4 (HTML 파싱)
- requests (HTTP 요청)
- PyYAML (설정 관리)

#### Frontend

- 순수 HTML/CSS/JavaScript
- 번들러 없음 (정적 파일)
- GitHub Pages 호스팅

#### DevOps

- GitHub Actions (CI/CD)
- 자동 배포 파이프라인

### 🗂️ 프로젝트 구조

```bash
Big Tech News/
├── scrapers/
│   ├── __init__.py
│   ├── base.py                    # 기본 스크래퍼 클래스
│   ├── rss_scraper.py            # RSS 파서
│   ├── html_scraper.py           # HTML 스크래퍼 기본
│   ├── anthropic_scraper.py      # Anthropic 전용
│   ├── meta_scraper.py           # Meta AI 전용
│   ├── deepmind_scraper.py       # DeepMind 전용
│   ├── google_ai_scraper.py      # Google AI 전용
│   ├── lg_research_scraper.py    # LG Research 전용
│   ├── nvidia_news_scraper.py    # NVIDIA News 전용
│   ├── microsoft_ai_scraper.py   # Microsoft AI News 전용
│   ├── microsoft_ai_news_scraper.py  # Microsoft AI News RSS + 필터링 🆕
│   ├── qwen_scraper.py           # Qwen 전용
│   ├── deepseek_scraper.py       # DeepSeek API Docs 전용
│   ├── deepseek_blog_scraper.py  # DeepSeek Blog 전용 (Sitemap)
│   ├── amazon_science_scraper.py # Amazon Science RSS 🆕
│   ├── ibm_research_scraper.py   # IBM Research RSS 🆕
│   └── baidu_research_scraper.py # Baidu Research HTML 🆕
├── data/                          # 수집된 데이터 (.gitignore)
│   ├── index.json                # 프리뷰 데이터
│   ├── news.json                 # 전체 데이터
│   └── sources/                  # 소스별 데이터
├── docs/
│   ├── index.html                # 메인 페이지
│   ├── style.css                 # 스타일시트
│   ├── app.js                    # 프론트엔드 로직
│   ├── assets/                   # 회사 로고 SVG
│   └── data/                     # 프론트엔드용 데이터 (.gitignore)
├── .github/workflows/
│   └── update-news.yml           # GitHub Actions 워크플로우
├── config.yaml                    # 설정 파일
├── main.py                        # 메인 실행 스크립트
├── requirements.txt               # Python 의존성
├── .gitignore
├── README.md
├── CLAUDE.md                      # Claude Code 가이드
├── DEPLOYMENT.md                  # 배포 가이드
└── SUMMARY.md                     # 이 파일
```

### 🎯 윤리적 사용 원칙

1. **robots.txt 준수**: 모든 사이트의 robots.txt 규칙을 철저히 분석하고 준수
2. **Rate Limiting**: 최소 1.5초 간격으로 요청 제한
3. **User-Agent 명시**: 명확한 식별 정보 제공
4. **원문 링크**: 모든 기사에 원본 링크 제공
5. **저작권 존중**: 원문 전체 복사 없이 요약/링크만 제공

### 🚀 다음 단계 개선 사항

#### 1. 접근 제한 사이트 해결

- OpenAI, xAI: User-Agent 전략 개선
- LG AI Research: Playwright/Selenium 도입 검토 (Nuxt.js 동적 렌더링)

#### 2. 기능 추가

- [ ] AI 기반 자동 요약
- [ ] 카테고리 자동 분류
- [ ] 이메일 알림 기능
- [ ] RSS 피드 제공
- [ ] 북마크 기능

#### 3. 성능 최적화

- [ ] 캐싱 전략
- [ ] 증분 업데이트 (변경된 것만)
- [ ] 이미지 썸네일 추가

#### 4. 추가 소스

- ~~Microsoft AI Blog~~ ✅ 완료
- ~~Amazon Science~~ ✅ 완료
- ~~IBM Research~~ ✅ 완료
- ~~Baidu Research~~ ✅ 완료

### 📈 현재 성과

- ✅ **17개 소스 모두 정상 작동!**
- ✅ **총 465개 기사 자동 수집**
- ✅ Amazon Science 스크래퍼 구현 (RSS + HTML 엔티티 디코딩) 🆕
- ✅ IBM Research 스크래퍼 구현 (RSS 피드) 🆕
- ✅ Baidu Research 스크래퍼 구현 (HTML 파싱, 날짜 형식 변환) 🆕
- ✅ Microsoft AI News AI 키워드 필터링 적용 🆕
- ✅ 목록형/카드형 뷰 전환 기능 추가 🆕
- ✅ 17개 회사 브랜드 색상 및 로고 적용
- ✅ LG AI Research API 방식으로 복구 (30개 기사)
- ✅ 완전 자동화된 워크플로우
- ✅ GitHub Pages 배포 완료
- ✅ 윤리적 웹 스크래핑 준수
- ✅ 데이터 파일 .gitignore 등록 (GitHub Actions에서만 생성)

### 💡 사용 방법

1. **로컬 실행**

   ```bash
   python main.py
   cd docs && python -m http.server 8000
   ```

2. **GitHub Pages 배포**
   - DEPLOYMENT.md 참조
   - 저장소 푸시 후 자동 배포

3. **자동 업데이트**
   - 매일 00:00 UTC 자동 실행
   - 수동 실행: GitHub Actions > Run workflow

### 🎓 배운 점

1. **웹 스크래핑 전략**
   - RSS가 가능하면 RSS 우선 사용
   - robots.txt 철저한 분석의 중요성
   - User-Agent 명시의 중요성

2. **데이터 수집의 어려움**
   - 각 사이트마다 다른 HTML 구조
   - 동적 콘텐츠 처리의 복잡성
   - 403 에러 대응 전략

3. **자동화의 가치**
   - GitHub Actions로 완전 자동화
   - 무료로 운영 가능한 인프라
   - CI/CD 파이프라인 구축

### 📝 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능

### 🙏 감사의 말

이 프로젝트는 빅테크 기업들이 공개한 정보를 바탕으로 만들어졌습니다. 모든 콘텐츠의 저작권은 원 저작자에게 있습니다.
