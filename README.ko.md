# BigTech AI News Aggregator

빅테크 기업들의 AI 관련 뉴스와 연구 발표를 한 곳에서 볼 수 있는 웹사이트입니다.

**Live Site: https://indigo-coder-github.github.io/Big-Tech-News/**

[English](README.md)

## 특징

- 매일 자동 업데이트 (GitHub Actions, 한국시간 09:00)
- 통합 검색 기능
- 회사별 필터링
- 목록형/카드형 뷰 전환
- 반응형 디자인
- GitHub Pages로 무료 호스팅

## 모니터링 대상 (17개 소스)

| 회사 | 수집 방식 | 상태 |
|------|----------|------|
| **Google Research** | RSS | ✅ 활성 |
| **Google Blog AI** | RSS | ✅ 활성 |
| **Google DeepMind** | HTML | ✅ 활성 |
| **NVIDIA Blog** | RSS | ✅ 활성 |
| **NVIDIA News** | RSS | ✅ 활성 |
| **Microsoft Research** | RSS | ✅ 활성 |
| **Microsoft AI News** | RSS + AI 필터링 | ✅ 활성 |
| **Anthropic** | HTML | ✅ 활성 |
| **Meta AI** | HTML | ✅ 활성 |
| **OpenAI** | RSS | ✅ 활성 |
| **DeepSeek** | HTML | ✅ 활성 |
| **DeepSeek Blog** | Sitemap | ✅ 활성 |
| **Qwen** | RSS | ✅ 활성 |
| **LG AI Research** | API | ✅ 활성 |
| **Amazon Science** | RSS | ✅ 활성 |
| **IBM Research** | RSS | ✅ 활성 |
| **Baidu Research** | HTML | ✅ 활성 |

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

## 프로젝트 구조

```
Big Tech News/
├── scrapers/           # 각 소스별 스크래퍼
├── data/               # 수집된 JSON 데이터
│   ├── index.json      # 프리뷰 데이터
│   └── sources/        # 소스별 전체 데이터
├── docs/               # GitHub Pages 사이트
├── .github/workflows/  # GitHub Actions 자동화
├── config.yaml         # 설정 파일
└── main.py             # 메인 스크립트
```

## 윤리적 사용

- robots.txt 규칙 준수
- Rate limiting 적용 (최소 1.5초 간격)
- 명확한 User-Agent 식별
- 원문 링크 제공

## 라이선스

MIT License
