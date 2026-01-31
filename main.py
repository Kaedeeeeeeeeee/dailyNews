"""
AI News Collector - Main Entry Point

Collects AI-related news from X/Twitter, processes with AI,
translates to Japanese, and generates a Markdown article.

Optimized for parallel processing.
"""

import os
import asyncio
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import yaml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from src.scraper import TwitterScraper
from src.ai_processor import AIProcessor
from src.formatter import ArticleFormatter, NewsItem


def load_config():
    """Load configuration files."""
    config_dir = Path(__file__).parent / "config"
    
    with open(config_dir / "accounts.yaml", "r", encoding="utf-8") as f:
        accounts_config = yaml.safe_load(f)
    
    with open(config_dir / "settings.yaml", "r", encoding="utf-8") as f:
        settings = yaml.safe_load(f)
    
    return accounts_config, settings


async def main():
    """Main execution flow."""
    print("=" * 60)
    print("🤖 AI News Collector - Starting (Optimized)")
    print("=" * 60)

    # Load configuration
    accounts_config, settings = load_config()
    accounts = accounts_config.get("accounts", [])
    
    # Get credentials from environment
    x_username = os.getenv("X_USERNAME")
    x_password = os.getenv("X_PASSWORD")
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    if not all([x_username, x_password, gemini_api_key]):
        print("❌ Missing required environment variables!")
        print("   Required: X_USERNAME, X_PASSWORD, GEMINI_API_KEY")
        return

    # Initialize components
    scraper = TwitterScraper(x_username, x_password)
    ai_processor = AIProcessor(
        gemini_api_key, 
        settings["ai"]["model"],
        max_concurrent=10  # Process 10 tweets in parallel
    )
    formatter = ArticleFormatter()

    # Get current date in JST
    jst = ZoneInfo(settings["output"]["timezone"])
    now = datetime.now(jst)
    date_str = now.strftime("%Y年%m月%d日")
    datetime_str = now.strftime("%Y年%m月%d日 %H:%M")
    output_date = now.strftime("%Y-%m-%d")

    # Create output directory
    output_dir = Path(__file__).parent / "output" / output_date
    output_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Login to X
    print("\n📡 Step 1: Logging in to X...")
    if not await scraper.login():
        print("❌ Failed to login to X. Exiting.")
        return

    # Step 2: Scrape tweets (parallel)
    print("\n📥 Step 2: Scraping tweets (parallel)...")
    all_tweets = await scraper.scrape_all_accounts(
        accounts,
        since_hours=settings["scraping"]["hours_lookback"],
        max_tweets_per_account=settings["scraping"]["max_tweets_per_account"],
        max_concurrent=5  # 5 concurrent scraping tasks
    )

    # Flatten all tweets
    tweets_list = []
    for username, tweets in all_tweets.items():
        tweets_list.extend(tweets)

    if not tweets_list:
        print("⚠️ No tweets found in the last 24 hours")
        # Still generate an article saying no news
        article = formatter.format_article(date_str, datetime_str, [])
        formatter.save_article(article, str(output_dir))
        print("✅ Generated 'no news' article")
        return

    print(f"📊 Total tweets to process: {len(tweets_list)}")

    # Step 3: Process with AI (parallel, single call per tweet)
    print("\n🤖 Step 3: Processing with AI (parallel)...")
    processed_tweets = await ai_processor.batch_process(
        tweets_list,
        max_summary_chars=settings["ai"]["summary_max_chars"]
    )

    if not processed_tweets:
        print("⚠️ No AI-related tweets found")
        article = formatter.format_article(date_str, datetime_str, [])
        formatter.save_article(article, str(output_dir))
        return

    # Step 4: Format article (title already generated in AI processing)
    print("\n📝 Step 4: Generating article...")
    news_items = []
    
    for i, tweet in enumerate(processed_tweets):
        # Create news item (title and summary already available from AI processor)
        news_item = NewsItem(
            source=tweet.author_name,
            title=tweet.title,
            summary_ja=tweet.summary,
            url=tweet.url,
            images=tweet.image_urls or [],  # Twitter image URLs
            emoji="",
            created_at=tweet.created_at
        )
        news_items.append(news_item)

    # Generate and save article
    article = formatter.format_article(date_str, datetime_str, news_items)
    output_path = formatter.save_article(article, str(output_dir))

    # Summary
    print("\n" + "=" * 60)
    print("✅ AI News Collection Complete!")
    print("=" * 60)
    print(f"📅 Date: {date_str}")
    print(f"📰 News items: {len(news_items)}")
    print(f"📄 Output: {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

