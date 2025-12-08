# 배포 가이드

이 문서는 BigTech AI News Aggregator를 GitHub Pages에 배포하는 방법을 설명합니다.

## 사전 준비

1. GitHub 계정
2. Git 설치
3. Python 3.11+ 설치

## 배포 단계

### 1. GitHub 저장소 생성

1. GitHub에서 새 저장소 생성
   - 저장소 이름: `big-tech-news` (또는 원하는 이름)
   - Public으로 설정 (GitHub Pages 무료 사용)

### 2. 로컬 저장소와 연결

```bash
cd "d:\python project\Big Tech News"
git init
git add .
git commit -m "Initial commit: BigTech AI News Aggregator"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/big-tech-news.git
git push -u origin main
```

### 3. GitHub Pages 설정

1. GitHub 저장소로 이동
2. Settings > Pages로 이동
3. Source: "GitHub Actions" 선택
4. 이미 `.github/workflows/update-news.yml`이 있으므로 자동으로 배포됩니다

### 4. GitHub Actions 첫 실행

#### 방법 1: 수동 실행

1. GitHub 저장소의 "Actions" 탭으로 이동
2. "Update AI News" 워크플로우 선택
3. "Run workflow" 버튼 클릭

#### 방법 2: 자동 실행 대기

- 매일 00:00 UTC (09:00 KST)에 자동으로 실행됩니다

### 5. 사이트 접속

배포가 완료되면 다음 URL에서 사이트 확인:

```
https://YOUR_USERNAME.github.io/big-tech-news/
```

## config.yaml 수정 사항

배포 전에 `config.yaml`의 User-Agent를 수정하세요:

```yaml
settings:
  user_agent: "BigTechNewsAggregator/1.0 (+https://github.com/YOUR_USERNAME/big-tech-news)"
```

## 문제 해결

### 워크플로우가 실패하는 경우

1. GitHub Actions 탭에서 실패한 워크플로우 확인
2. 로그를 확인하여 어떤 스크래퍼에서 문제가 발생했는지 확인
3. 필요시 `config.yaml`에서 해당 소스를 `enabled: false`로 설정

### 데이터가 업데이트되지 않는 경우

1. GitHub Actions 탭에서 워크플로우 실행 상태 확인
2. 워크플로우가 실행되었지만 커밋이 없는 경우:
   - 데이터에 변경사항이 없었을 가능성
   - 스크래퍼에서 0개의 기사를 수집했을 가능성

### GitHub Pages가 보이지 않는 경우

1. Settings > Pages에서 배포 상태 확인
2. "Your site is published at..." 메시지 확인
3. 첫 배포는 최대 10분 정도 소요될 수 있습니다

## 커스텀 도메인 설정 (선택사항)

자신의 도메인을 사용하려면:

1. Settings > Pages > Custom domain에 도메인 입력
2. DNS 설정에서 CNAME 레코드 추가:
   ```
   CNAME: YOUR_USERNAME.github.io
   ```

## 업데이트 주기 변경

`.github/workflows/update-news.yml`의 cron 표현식을 수정:

```yaml
schedule:
  - cron: '0 0 * * *'  # 매일 00:00 UTC
  # - cron: '0 */6 * * *'  # 6시간마다
  # - cron: '0 0 * * 0'  # 매주 일요일
```

## 로컬 테스트

배포 전 로컬에서 테스트:

```bash
# 데이터 수집
python main.py

# 웹사이트 확인
cd docs
python -m http.server 8000
# http://localhost:8000 접속
```

## 비용

- GitHub Pages: 무료 (Public 저장소)
- GitHub Actions: 월 2,000분 무료 (일일 실행 시 충분)
- 추가 비용 없음

## 보안 고려사항

1. API 키나 비밀번호를 절대 커밋하지 마세요
2. `.gitignore`에 민감한 정보 추가
3. robots.txt를 항상 존중하세요
4. Rate limiting을 준수하세요

## 추가 리소스

- [GitHub Pages 문서](https://docs.github.com/en/pages)
- [GitHub Actions 문서](https://docs.github.com/en/actions)
- [Cron 표현식 생성기](https://crontab.guru/)
