-- 政策信息自动化流水线 — SQLite Schema v1.0

CREATE TABLE IF NOT EXISTS raw_articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    publish_time TEXT,
    source_name TEXT NOT NULL,
    body_text TEXT,
    body_hash TEXT NOT NULL,
    event_fingerprint TEXT,
    summary_256 TEXT,
    first_seen_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    is_repost INTEGER DEFAULT 0,
    has_similar INTEGER DEFAULT 0,
    canonical_id INTEGER,
    priority_rank INTEGER DEFAULT 99,
    crawl_count INTEGER DEFAULT 1,
    last_crawled_at TEXT,
    status TEXT DEFAULT 'new'
);

CREATE TABLE IF NOT EXISTS ai_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id INTEGER NOT NULL UNIQUE,
    public_impact_score REAL,
    relevance_score REAL,
    novelty_score REAL,
    explainability_score REAL,
    timeliness_score REAL,
    total_score REAL,
    category TEXT,
    scored_at TEXT DEFAULT (datetime('now', 'localtime')),
    score_version TEXT DEFAULT 'v1',
    FOREIGN KEY (article_id) REFERENCES raw_articles(id)
);

CREATE TABLE IF NOT EXISTS fact_extracts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id INTEGER NOT NULL UNIQUE,
    event_summary TEXT,
    government_action TEXT,
    affected_groups TEXT,
    effective_date TEXT,
    key_numbers TEXT,
    official_reason TEXT,
    public_impact TEXT,
    next_signal TEXT,
    facts TEXT,
    inferences TEXT,
    uncertainties TEXT,
    publish_advice TEXT,
    extracted_at TEXT DEFAULT (datetime('now', 'localtime')),
    model_used TEXT,
    FOREIGN KEY (article_id) REFERENCES raw_articles(id)
);

CREATE TABLE IF NOT EXISTS publish_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id INTEGER NOT NULL,
    feishu_record_id TEXT,
    review_status TEXT DEFAULT 'pending',
    reviewed_by TEXT,
    reviewed_at TEXT,
    published_at TEXT,
    xhs_image_path TEXT,
    notes TEXT,
    FOREIGN KEY (article_id) REFERENCES raw_articles(id)
);

CREATE TABLE IF NOT EXISTS crawl_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name TEXT NOT NULL,
    crawl_url TEXT NOT NULL,
    status TEXT,
    articles_found INTEGER DEFAULT 0,
    new_articles INTEGER DEFAULT 0,
    error_message TEXT,
    duration_ms INTEGER,
    crawled_at TEXT DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS event_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_fingerprint TEXT NOT NULL UNIQUE,
    canonical_article_id INTEGER,
    member_count INTEGER DEFAULT 1,
    best_source TEXT,
    created_at TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (canonical_article_id) REFERENCES raw_articles(id)
);
