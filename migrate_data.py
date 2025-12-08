"""
기존 news.json을 새로운 구조로 마이그레이션
"""

import json
from data_manager import DataManager


def migrate_old_data():
    """기존 news.json을 새 구조로 마이그레이션"""

    # 기존 데이터 로드
    try:
        with open('data/news.json', 'r', encoding='utf-8') as f:
            old_data = json.load(f)
    except FileNotFoundError:
        print("❌ data/news.json 파일을 찾을 수 없습니다.")
        return

    articles = old_data.get('articles', [])

    if not articles:
        print("⚠️ 마이그레이션할 기사가 없습니다.")
        return

    print(f"📦 기존 데이터 로드: {len(articles)}개 기사")
    print(f"   업데이트 시간: {old_data.get('updated_at', 'N/A')}")

    # 새 구조로 저장
    dm = DataManager()
    dm.save_articles(articles)

    print("\n✅ 마이그레이션 완료!")
    print(f"   - data/sources/*.json: 소스별 파일 생성")
    print(f"   - data/index.json: 미리보기 인덱스 생성")
    print(f"   - data/stats.json: 통계 파일 생성")


if __name__ == "__main__":
    migrate_old_data()
