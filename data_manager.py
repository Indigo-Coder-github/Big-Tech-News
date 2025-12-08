"""
데이터 저장 및 관리 모듈
소스별 파일 분할 및 index.json 생성
"""

import json
import os
from datetime import datetime
from typing import List, Dict
from pathlib import Path


class DataManager:
    """데이터 저장 및 인덱스 관리"""

    def __init__(self, base_dir: str = "data"):
        self.base_dir = Path(base_dir)
        self.sources_dir = self.base_dir / "sources"
        self.index_file = self.base_dir / "index.json"
        self.stats_file = self.base_dir / "stats.json"

        # 디렉토리 생성
        self.sources_dir.mkdir(parents=True, exist_ok=True)

    def save_articles(self, articles: List[Dict]):
        """
        기사를 소스별로 분할 저장하고 index.json 생성

        Args:
            articles: 전체 기사 리스트
        """
        # 소스별로 그룹화
        articles_by_source = self._group_by_source(articles)

        # 소스별 파일 저장
        for source, source_articles in articles_by_source.items():
            self._save_source_file(source, source_articles)

        # index.json 생성 (최신 글 미리보기)
        self._create_index(articles_by_source)

        # stats.json 생성 (통계)
        self._create_stats(articles_by_source)

        print(f"[OK] Saved articles from {len(articles_by_source)} sources.")

    def _group_by_source(self, articles: List[Dict]) -> Dict[str, List[Dict]]:
        """기사를 소스별로 그룹화"""
        groups = {}
        for article in articles:
            source = article.get('source', 'Unknown')
            if source not in groups:
                groups[source] = []
            groups[source].append(article)

        # 각 소스 내에서 날짜순 정렬 (최신순)
        for source in groups:
            groups[source].sort(
                key=lambda x: x.get('date', '1900-01-01'),
                reverse=True
            )

        return groups

    def _save_source_file(self, source: str, articles: List[Dict]):
        """소스별 파일 저장"""
        # 파일명: 소스명을 소문자로 변환하고 공백을 하이픈으로
        filename = source.lower().replace(' ', '-').replace('/', '-') + '.json'
        filepath = self.sources_dir / filename

        data = {
            'source': source,
            'total_articles': len(articles),
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'articles': articles
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"  [FILE] {filename}: {len(articles)} articles")

    def _create_index(self, articles_by_source: Dict[str, List[Dict]], preview_count: int = 10):
        """
        index.json 생성 (각 소스의 최신 N개만 포함)

        Args:
            articles_by_source: 소스별 그룹화된 기사
            preview_count: 각 소스당 포함할 최신 기사 수
        """
        # 각 소스의 최신 N개만 추출
        preview_articles = []
        source_info = []

        for source, articles in articles_by_source.items():
            # 최신 N개만
            latest_articles = articles[:preview_count]
            preview_articles.extend(latest_articles)

            # 소스 정보
            filename = source.lower().replace(' ', '-').replace('/', '-') + '.json'
            source_info.append({
                'name': source,
                'file': f'sources/{filename}',
                'total_articles': len(articles),
                'latest_date': articles[0].get('date', 'N/A') if articles else 'N/A',
                'preview_count': len(latest_articles)
            })

        # 전체를 날짜순으로 정렬
        preview_articles.sort(
            key=lambda x: x.get('date', '1900-01-01'),
            reverse=True
        )

        # 소스 정보도 이름순 정렬
        source_info.sort(key=lambda x: x['name'])

        index_data = {
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_sources': len(articles_by_source),
            'total_articles': sum(len(arts) for arts in articles_by_source.values()),
            'preview_articles': preview_articles,
            'sources': source_info
        }

        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, ensure_ascii=False, indent=2)

        print(f"  [INDEX] index.json: {len(preview_articles)} preview articles")

    def _create_stats(self, articles_by_source: Dict[str, List[Dict]]):
        """통계 파일 생성"""
        total_articles = sum(len(arts) for arts in articles_by_source.values())
        articles_with_dates = sum(
            1 for arts in articles_by_source.values()
            for art in arts
            if art.get('date') and art['date'] != 'N/A'
        )

        stats = {
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_sources': len(articles_by_source),
            'total_articles': total_articles,
            'articles_with_dates': articles_with_dates,
            'date_extraction_rate': f"{(articles_with_dates / total_articles * 100):.1f}%" if total_articles > 0 else "0%",
            'by_source': {
                source: {
                    'count': len(articles),
                    'with_dates': sum(1 for a in articles if a.get('date') and a['date'] != 'N/A'),
                    'latest_date': articles[0].get('date', 'N/A') if articles else 'N/A'
                }
                for source, articles in sorted(articles_by_source.items())
            }
        }

        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)

        print(f"  [STATS] stats.json: statistics file created")

    def load_source_articles(self, source: str) -> List[Dict]:
        """특정 소스의 전체 기사 로드"""
        filename = source.lower().replace(' ', '-').replace('/', '-') + '.json'
        filepath = self.sources_dir / filename

        if not filepath.exists():
            return []

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('articles', [])

    def load_index(self) -> Dict:
        """index.json 로드"""
        if not self.index_file.exists():
            return {}

        with open(self.index_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_all_sources(self) -> List[str]:
        """모든 소스 목록 반환"""
        index = self.load_index()
        return [s['name'] for s in index.get('sources', [])]


if __name__ == "__main__":
    # 테스트 코드
    print("DataManager 모듈 테스트")
    dm = DataManager()
    print(f"Base directory: {dm.base_dir}")
    print(f"Sources directory: {dm.sources_dir}")
