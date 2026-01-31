# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Daily AI News Collector (カエデのAIニュース) - Automated system that scrapes AI-related tweets from 50+ X/Twitter accounts, filters and summarizes them using Gemini AI in Japanese, generates markdown articles with cover images, and publishes to note.com.

## Commands

```bash
# Setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
playwright install chromium  # For note.com publishing

# Run main workflow
python main.py

# Run tests
pytest tests/

# Run single test
pytest tests/test_modules.py::TestFormatter::test_format_no_news -v
```

## Required Environment Variables

```bash
X_USERNAME=twitter_username
X_PASSWORD=twitter_password
GEMINI_API_KEY=gemini_api_key
# Optional for GitHub Actions:
AUTH_TOKEN=twitter_cookie_auth_token
CT0=twitter_cookie_ct0
```

## Architecture

### Data Flow
```
TwitterScraper (5 concurrent) → AIProcessor (10 concurrent) → ArticleFormatter → CoverGenerator → NotePublisher
```

### Core Modules (src/)

- **scraper.py** - `TwitterScraper`: Uses Twikit for X scraping. Auth priority: env cookies > file cookies > login. Returns `Tweet` dataclass.
- **ai_processor.py** - `AIProcessor`: Gemini AI for filtering AI-relevant tweets and generating Japanese summaries/titles in single API call. Returns `ProcessedTweet` dataclass.
- **formatter.py** - `ArticleFormatter`: Converts processed tweets to markdown with TOC. Returns `NewsItem` dataclass.
- **cover_generator.py** - `CoverGenerator`: Adds date overlay to `assets/Untitled design.png`.
- **note_publisher.py** - `NotePublisher`: Playwright automation for note.com draft creation.

### Key Files

- `config/accounts.yaml` - List of 50+ X accounts by category (US_Company, French_Company, Chinese_Company, Other)
- `config/settings.yaml` - Scraping hours (24h), max tweets (10), AI model, timezone (Asia/Tokyo)
- `output/YYYY-MM-DD/` - Daily output: `article.md` and `cover.png`

### GitHub Actions (.github/workflows/daily.yml)

Runs at 21:30 UTC (6:30 JST+1) daily:
1. `collect-news` - Scrape, process, generate article
2. `publish-to-note` - Create draft on note.com (conditional)
3. `send-email` - Email notification (conditional)

## Implementation Notes

- All async/await with semaphores for rate limiting
- JST timezone (Asia/Tokyo) for all timestamps and file paths
- ~30% of tweets typically pass AI relevance filter
- note.com publishes as draft only (manual review required)
- Cookies stored in `cookies.json` (X) and `note_cookies.json` (note.com)
