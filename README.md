# BigTech AI News Aggregator

A website that aggregates AI-related news and research publications from major BigTech companies in one place.

**Live Site: https://indigo-coder-github.github.io/Big-Tech-News/**

[한국어](README.ko.md)

## Features

- Daily automatic updates (GitHub Actions, 09:00 KST)
- Unified search functionality
- Filter by company
- List/Card view toggle
- Responsive design
- Free hosting on GitHub Pages

## Monitored Sources (17 sources)

| Company | Collection Method | Status |
|---------|------------------|--------|
| **Google Research** | RSS | ✅ Active |
| **Google Blog AI** | RSS | ✅ Active |
| **Google DeepMind** | HTML | ✅ Active |
| **NVIDIA Blog** | RSS | ✅ Active |
| **NVIDIA News** | RSS | ✅ Active |
| **Microsoft Research** | RSS | ✅ Active |
| **Microsoft AI News** | RSS + AI Filtering | ✅ Active |
| **Anthropic** | HTML | ✅ Active |
| **Meta AI** | HTML | ✅ Active |
| **OpenAI** | RSS | ✅ Active |
| **DeepSeek** | HTML | ✅ Active |
| **DeepSeek Blog** | Sitemap | ✅ Active |
| **Qwen** | RSS | ✅ Active |
| **LG AI Research** | API | ✅ Active |
| **Amazon Science** | RSS | ✅ Active |
| **IBM Research** | RSS | ✅ Active |
| **Baidu Research** | HTML | ✅ Active |

## Installation & Usage

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Collect Data

```bash
python main.py
```

### 3. View Website Locally

```bash
cd docs
python -m http.server 8000
```

Visit `http://localhost:8000` in your browser

## Project Structure

```
Big Tech News/
├── scrapers/           # Source-specific scrapers
├── data/               # Collected JSON data
│   ├── index.json      # Preview data
│   └── sources/        # Full data per source
├── docs/               # GitHub Pages site
├── .github/workflows/  # GitHub Actions automation
├── config.yaml         # Configuration file
└── main.py             # Main script
```

## Ethical Usage

- Compliance with robots.txt rules
- Rate limiting applied (minimum 1.5 second intervals)
- Clear User-Agent identification
- Links to original sources provided

## License

MIT License
