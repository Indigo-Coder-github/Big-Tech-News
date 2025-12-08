# CLAUDE.md

이 파일은 이 저장소에서 작업할 때 Claude Code (claude.ai/code)에게 가이드를 제공합니다.

## 프로젝트 개요

BigTech AI News Aggregator는 주요 빅테크 기업(Google Research, NVIDIA, Anthropic, Meta AI, DeepMind 등)의 AI 관련 뉴스를 자동으로 수집하여 GitHub Pages에 호스팅되는 정적 웹사이트로 표시하는 웹 스크래핑 및 취합 시스템입니다. 시스템은 GitHub Actions를 통해 매일 자동으로 실행됩니다.

## 핵심 명령어

### 개발 환경

- Windows 11
- VS Code
- Python 3.11+

### 개발

```bash
# 의존성 설치
pip install -r requirements.txt

# 스크래퍼 수동 실행
python main.py

# 웹사이트 로컬 테스트
cd docs && python -m http.server 8000
# http://localhost:8000 방문
```

### 배포

```bash
# GitHub Actions 워크플로우 수동 실행
# GitHub Actions 탭 > "Update AI News" > "Run workflow"

# 또는 main 브랜치에 푸시하여 자동 배포
git push origin main
```

## 아키텍처

### 데이터 흐름

1. **수집**: `main.py`가 `config.yaml`을 통해 여러 소스에서 스크래핑 조율
2. **스크래핑**: `scrapers/` 디렉토리의 소스별 스크래퍼가 기사 가져오기
3. **처리**: 기사를 정규화, 중복 제거, 정렬, 소스당 개수 제한
4. **저장**: `data/news.json`에 메타데이터(updated_at, total_articles)와 함께 출력 저장
5. **표시**: `docs/`의 프론트엔드가 JSON을 로드하고 검색/필터 기능으로 기사 렌더링

### 스크래퍼 아키텍처

**기본 클래스**:

- `BaseScraper` (scrapers/base.py): Rate limiting, 헤더, 정규화를 포함한 추상 기본 클래스
- `RSScraper` (scrapers/rss_scraper.py): feedparser를 사용하는 RSS 피드 파서
- `HTMLScraper` (scrapers/html_scraper.py): BeautifulSoup을 사용하는 HTML 파서 기본 클래스

**소스별 스크래퍼**:

각 스크래퍼는 `RSScraper` 또는 `HTMLScraper`를 상속하고 소스별 파싱 로직 구현:

- `anthropic_scraper.py`: Next.js 임베디드 JSON 데이터 파싱
- `meta_scraper.py`: 폴백 패턴이 있는 기사 카드에서 추출
- `deepmind_scraper.py`: 날짜 추출과 함께 블로그 링크 크롤링
- `google_ai_scraper.py`: 연구 및 업데이트 섹션 찾기
- `lg_research_scraper.py`: Nuxt.js 블로그 파싱
- `nvidia_news_scraper.py`: 뉴스 기사 추출

**새 스크래퍼 추가하기**:

1. `HTMLScraper` 또는 `RSScraper`를 상속하는 `scrapers/new_source_scraper.py` 생성
2. 기사 데이터가 담긴 `List[Dict]`를 반환하는 `fetch()` 메서드 구현
3. `main.py`의 `scraper_map`에 추가 (38-45번째 줄)
4. `config.yaml`에 `scraper: "new_source"` 필드로 소스 설정 추가
5. `main.py` 상단에 클래스 import

### 설정 시스템

`config.yaml` 구조:

```yaml
sources:
  - name: "Source Name"
    type: "rss" | "html"
    url: "https://..."
    enabled: true | false
    scraper: "scraper_key"  # HTML 타입에만 필요

settings:
  user_agent: "..."  # 중요: 배포 전 GitHub URL로 업데이트
  request_delay: 1.5  # Rate limiting (초 단위)
  max_articles_per_source: 50
  output_file: "data/news.json"
```

**중요 설정 사항**:

- `enabled: false` 소스는 건너뜀 (접근 문제가 있는 소스에 유용)
- HTML 소스는 main.py의 `scraper_map`과 일치하는 `scraper` 키 필요
- RSS 소스는 자동으로 `RSScraper` 클래스 사용

### 데이터 형식

**출력 JSON** (`data/news.json`):

```json
{
  "updated_at": "YYYY-MM-DD HH:MM:SS",
  "total_articles": 119,
  "articles": [
    {
      "source": "회사명",
      "title": "기사 제목",
      "url": "https://...",
      "date": "YYYY-MM-DD",
      "summary": "...",
      "author": "...",
      "categories": ["카테고리1", "카테고리2"],
      "collected_at": "YYYY-MM-DD HH:MM:SS"
    }
  ]
}
```

### 프론트엔드 아키텍처

**정적 사이트** (`docs/`):

- `index.html`: 검색, 필터, 정렬 컨트롤이 있는 구조
- `style.css`: CSS 변수를 사용한 반응형 카드 기반 레이아웃
- `app.js`: JSON 가져오기, 필터링, 정렬, 렌더링을 위한 바닐라 JavaScript

**주요 프론트엔드 함수**:

- `loadArticles()`: 페이지 로드 시 `../data/news.json` 가져오기
- `applyFilters()`: 검색어와 소스 필터링 결합
- `sortArticles()`: date-desc, date-asc, source 정렬 지원
- `displayArticles()`: 기사 카드를 동적으로 렌더링

## 윤리적 웹 스크래핑 원칙

이 프로젝트는 윤리적 스크래핑 관행을 엄격히 준수합니다:

1. **robots.txt 준수**: 구현 전 모든 소스의 robots.txt 규칙 분석
2. **Rate Limiting**: 요청 간 최소 1.5초 지연 (config.yaml에서 설정 가능)
3. **User-Agent 식별**: 저장소 링크가 포함된 명확한 식별
4. **콘텐츠 출처 표시**: 모든 기사가 원본 소스로 링크
5. **우회 금지**: 403 에러를 반환하는 소스는 비활성화, 우회하지 않음

**새 소스 추가 전**:

- `https://domain.com/robots.txt`에서 robots.txt 확인
- 대상 경로에 대해 스크래핑이 허용되는지 확인
- 보수적인 rate limiting으로 테스트
- 불확실하면 처음에 `enabled: false`로 설정

## 문제 해결

### 스크래퍼 실패

- 소스 HTML 구조가 변경되지 않았는지 확인 (일반적인 문제)
- robots.txt에 새로운 제한이 추가되지 않았는지 확인
- User-Agent 문자열이 차단되지 않는지 테스트
- 구체적인 오류 메시지는 GitHub Actions 로그 확인

### 데이터 업데이트 안 됨

- GitHub Actions 탭에서 워크플로우가 성공적으로 실행되는지 확인
- 스크래퍼가 0개 기사를 반환했는지 확인 (HTML 구조 변경 가능성)
- 워크플로우에 저장소 쓰기 권한이 있는지 확인
- 로컬 테스트 실행 후 `data/news.json`이 존재하는지 확인

### 프론트엔드에 데이터 표시 안 됨

- `data/news.json`이 존재하고 유효한 JSON인지 확인
- CORS 또는 fetch 오류는 브라우저 콘솔 확인
- 상대 경로 `../data/news.json`이 올바른지 확인
- docs/에서 `python -m http.server 8000`으로 로컬 테스트

### 새 스크래퍼 작동 안 됨

- main.py에 스크래퍼 클래스가 import되었는지 확인
- config.yaml의 스크래퍼 키가 scraper_map과 일치하는지 확인
- 스크래퍼가 HTMLScraper 또는 RSScraper를 상속하는지 확인
- fetch()가 필수 필드가 있는 List[Dict]를 반환하는지 확인

## GitHub Actions 워크플로우

워크플로우 (`.github/workflows/update-news.yml`):

1. 매일 00:00 UTC (09:00 KST)에 실행
2. Python 3.11 및 의존성 설치
3. `python main.py` 실행
4. `data/news.json` 변경 확인
5. 데이터가 업데이트되면 변경사항 커밋
6. `docs/`를 gh-pages 브랜치에 배포

**수동 실행**: Actions 탭 > "Update AI News" > "Run workflow"

**실패한 워크플로우 디버깅**:

1. Actions 탭에서 실패한 워크플로우 클릭
2. 실패한 단계를 확장하여 오류 로그 확인
3. 일반적인 문제: 스크래퍼 예외, 네트워크 타임아웃, HTML 구조 변경
4. 지속적인 문제는 config.yaml에서 해당 소스 비활성화

## 중요 파일

- `config.yaml`: 소스 및 설정의 단일 진실 공급원
- `main.py`: 오케스트레이션 로직 및 데이터 처리 파이프라인
- `scrapers/base.py`: 공유 스크래퍼 기능 및 기사 정규화
- `data/news.json`: 프론트엔드가 사용하는 생성된 출력 (.gitignore에 없음)
- `docs/app.js`: 기사 로딩 및 표시를 위한 프론트엔드 로직

## 배포 체크리스트

GitHub Pages에 배포하기 전:

1. `config.yaml`의 user_agent를 GitHub 저장소 URL로 업데이트
2. 로컬 테스트: `python main.py && cd docs && python -m http.server 8000`
3. `data/news.json`이 성공적으로 생성되었는지 확인
4. GitHub에 푸시하고 GitHub Pages 활성화 (Settings > Pages > Source: GitHub Actions)
5. 첫 워크플로우 실행 수동 트리거 (Actions > Run workflow)
6. gh-pages 브랜치로의 첫 배포까지 5-10분 대기
