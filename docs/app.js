// BigTech AI News - Frontend Application

let allArticles = [];
let filteredArticles = [];
let currentSource = 'all';
let currentSort = 'date-desc';
let sourceMetadata = {}; // Store source info from index.json
let loadedSources = new Set(); // Track which sources have been fully loaded

// Company logo mapping
const logoMap = {
    'Google Research': 'google-color.svg',
    'Google AI': 'google-color.svg',
    'Google Blog AI': 'google-color.svg',
    'Google DeepMind': 'deepmind-color.svg',
    'NVIDIA Blog': 'nvidia-color.svg',
    'NVIDIA News': 'nvidia-color.svg',
    'Microsoft Research': 'microsoft-color.svg',
    'Microsoft AI News': 'microsoft-color.svg',
    'Anthropic': 'claude-color.svg',
    'Meta AI': 'meta-color.svg',
    'LG AI Research': 'lg-color.svg',
    'OpenAI': 'openai.svg',
    'xAI': 'xai.svg',
    'DeepSeek': 'deepseek-color.svg',
    'DeepSeek Blog': 'deepseek-color.svg',
    'Qwen': 'qwen-color.svg'
};

// Get CSS class for source
function getSourceClass(source) {
    return 'source-' + source.toLowerCase().replace(/\s+/g, '-');
}

// Load data when page loads
document.addEventListener('DOMContentLoaded', async () => {
    await loadArticles();
    setupEventListeners();
});

// Load articles from JSON file (new structure: index.json)
async function loadArticles() {
    try {
        // Load index.json (contains preview articles + source metadata)
        const response = await fetch('data/index.json').catch(() => fetch('../data/index.json'));
        const data = await response.json();

        // Load preview articles
        allArticles = data.preview_articles || [];

        // Store source metadata
        sourceMetadata = {};
        (data.sources || []).forEach(source => {
            sourceMetadata[source.name] = source;
        });

        // Update last updated time
        const updatedAt = data.updated_at || 'Unknown';
        document.getElementById('lastUpdated').textContent = `마지막 업데이트: ${updatedAt}`;

        // Generate source filters
        generateSourceFilters(data.sources || []);

        // Display articles
        filteredArticles = [...allArticles];
        displayArticles();
    } catch (error) {
        console.error('Error loading articles:', error);
        document.getElementById('articlesContainer').innerHTML = `
            <div class="no-results">
                <h2>데이터를 불러올 수 없습니다</h2>
                <p>data/index.json 파일이 없습니다. main.py를 실행하여 데이터를 수집하세요.</p>
            </div>
        `;
    }
}

// Load full articles for a specific source
async function loadSourceArticles(sourceName) {
    // Check if already loaded
    if (loadedSources.has(sourceName)) {
        return;
    }

    const metadata = sourceMetadata[sourceName];
    if (!metadata || !metadata.file) {
        console.warn(`No metadata found for source: ${sourceName}`);
        return;
    }

    try {
        // Load source-specific file
        const response = await fetch(`data/${metadata.file}`).catch(() => fetch(`../${metadata.file}`));
        const data = await response.json();

        const sourceArticles = data.articles || [];

        // Remove preview articles for this source from allArticles
        allArticles = allArticles.filter(a => a.source !== sourceName);

        // Add full source articles
        allArticles.push(...sourceArticles);

        // Mark as loaded
        loadedSources.add(sourceName);

        console.log(`Loaded ${sourceArticles.length} articles from ${sourceName}`);
    } catch (error) {
        console.error(`Error loading source ${sourceName}:`, error);
    }
}

// Generate source filter buttons
function generateSourceFilters(sources) {
    const filterContainer = document.getElementById('sourceFilters');

    // Keep "All" button, add source-specific buttons
    sources.forEach(sourceInfo => {
        const sourceName = sourceInfo.name;
        const btn = document.createElement('button');
        const sourceClass = getSourceClass(sourceName);
        btn.className = `filter-btn ${sourceClass}`;
        btn.dataset.source = sourceName;
        btn.onclick = () => filterBySource(sourceName);

        // Add logo if available
        const logoFile = logoMap[sourceName];
        if (logoFile) {
            const img = document.createElement('img');
            img.src = `assets/${logoFile}`;
            img.alt = `${sourceName} logo`;
            btn.appendChild(img);
        }

        // Add text
        const text = document.createTextNode(sourceName);
        btn.appendChild(text);

        // Add article count badge (use total_articles from metadata)
        const badge = document.createElement('span');
        badge.className = 'article-count-badge';
        badge.textContent = sourceInfo.total_articles.toString();
        btn.appendChild(badge);

        filterContainer.appendChild(btn);
    });
}

// Setup event listeners
function setupEventListeners() {
    // Search
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', (e) => {
        applyFilters();
    });

    // Sort
    const sortSelect = document.getElementById('sortSelect');
    sortSelect.addEventListener('change', (e) => {
        currentSort = e.target.value;
        sortArticles();
        displayArticles();
    });

    // "All" filter button
    const allBtn = document.querySelector('[data-source="all"]');
    if (allBtn) {
        allBtn.onclick = () => filterBySource('all');
    }
}

// Filter by source
async function filterBySource(source) {
    currentSource = source;

    // Load full source data if filtering by specific source
    if (source !== 'all') {
        await loadSourceArticles(source);
    }

    // Update active button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.source === source) {
            btn.classList.add('active');
        }
    });

    applyFilters();
}

// Apply all filters
function applyFilters() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();

    filteredArticles = allArticles.filter(article => {
        // Source filter
        if (currentSource !== 'all' && article.source !== currentSource) {
            return false;
        }

        // Search filter
        if (searchTerm) {
            const searchableText = [
                article.title,
                article.summary,
                article.source,
                ...(article.categories || [])
            ].join(' ').toLowerCase();

            if (!searchableText.includes(searchTerm)) {
                return false;
            }
        }

        return true;
    });

    sortArticles();
    displayArticles();
}

// Sort articles
function sortArticles() {
    switch (currentSort) {
        case 'date-desc':
            filteredArticles.sort((a, b) => {
                const dateA = a.date || a.collected_at || '';
                const dateB = b.date || b.collected_at || '';
                return dateB.localeCompare(dateA);
            });
            break;

        case 'date-asc':
            filteredArticles.sort((a, b) => {
                const dateA = a.date || a.collected_at || '';
                const dateB = b.date || b.collected_at || '';
                return dateA.localeCompare(dateB);
            });
            break;

        case 'source':
            filteredArticles.sort((a, b) => {
                const sourceCompare = a.source.localeCompare(b.source);
                if (sourceCompare !== 0) return sourceCompare;

                // Within same source, sort by date desc
                const dateA = a.date || a.collected_at || '';
                const dateB = b.date || b.collected_at || '';
                return dateB.localeCompare(dateA);
            });
            break;
    }
}

// Display articles
function displayArticles() {
    const container = document.getElementById('articlesContainer');
    const statsElement = document.getElementById('articleCount');

    // Update stats
    statsElement.textContent = `${filteredArticles.length}개의 기사`;

    // Clear container
    container.innerHTML = '';

    if (filteredArticles.length === 0) {
        // Check if it's a specific source filter with no articles
        if (currentSource !== 'all') {
            const logoFile = logoMap[currentSource];
            const logoHtml = logoFile ? `<img src="assets/${logoFile}" alt="${currentSource} logo" style="width: 64px; height: 64px; margin-bottom: 20px; padding: 8px; background: white; border-radius: 50%; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">` : '';

            container.innerHTML = `
                <div class="no-results">
                    ${logoHtml}
                    <h2>${currentSource}</h2>
                    <p style="font-size: 1.1rem; color: var(--text-secondary); margin-top: 10px;">현재 수집된 콘텐츠가 없습니다.</p>
                    <p style="font-size: 0.9rem; color: var(--text-secondary); margin-top: 8px;">이 소스는 아직 기사를 수집하지 못했거나, 접근이 제한되어 있을 수 있습니다.</p>
                </div>
            `;
        } else {
            container.innerHTML = `
                <div class="no-results">
                    <h2>검색 결과가 없습니다</h2>
                    <p>다른 검색어나 필터를 시도해보세요.</p>
                </div>
            `;
        }
        return;
    }

    // Create article cards
    filteredArticles.forEach(article => {
        const card = createArticleCard(article);
        container.appendChild(card);
    });
}

// Create article card element
function createArticleCard(article) {
    const card = document.createElement('div');
    card.className = 'article-card';

    const date = article.date || article.collected_at?.split(' ')[0] || '';
    const formattedDate = formatDate(date);

    const categories = (article.categories || [])
        .filter(c => c && c.trim())
        .map(cat => `<span class="category-tag">${escapeHtml(cat)}</span>`)
        .join('');

    // Get logo and source class
    const logoFile = logoMap[article.source];
    const sourceClass = getSourceClass(article.source);
    const logoHtml = logoFile ? `<img src="assets/${logoFile}" alt="${escapeHtml(article.source)} logo">` : '';

    card.innerHTML = `
        <div class="article-header">
            <span class="article-source ${sourceClass}">
                ${logoHtml}
                ${escapeHtml(article.source)}
            </span>
        </div>
        <h2 class="article-title">
            <a href="${escapeHtml(article.url)}" target="_blank" rel="noopener noreferrer">
                ${escapeHtml(article.title)}
            </a>
        </h2>
        <div class="article-meta">
            ${date ? `<span class="article-date">${formattedDate}</span>` : ''}
            ${article.author ? `<span class="article-author">작성자: ${escapeHtml(article.author)}</span>` : ''}
        </div>
        ${article.summary ? `<p class="article-summary">${escapeHtml(article.summary)}</p>` : ''}
        ${categories ? `<div class="article-categories">${categories}</div>` : ''}
    `;

    return card;
}

// Format date to Korean
function formatDate(dateStr) {
    if (!dateStr) return '';

    try {
        const date = new Date(dateStr);
        const year = date.getFullYear();
        const month = date.getMonth() + 1;
        const day = date.getDate();
        return `${year}년 ${month}월 ${day}일`;
    } catch (error) {
        return dateStr;
    }
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text || '';
    return div.innerHTML;
}
