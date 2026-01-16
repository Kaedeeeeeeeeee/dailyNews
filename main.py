"""
AI News Collector - Main Entry Point

Collects AI-related news from X/Twitter, processes with AI,
translates to Japanese, and generates a Markdown article.
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
from src.image_handler import ImageHandler
from src.translator import Translator
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
    print("🤖 AI News Collector - Starting")
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
    ai_processor = AIProcessor(gemini_api_key, settings["ai"]["model"])
    translator = Translator(gemini_api_key, settings["ai"]["model"])
    formatter = ArticleFormatter()

    # Get current date in JST
    jst = ZoneInfo(settings["output"]["timezone"])
    now = datetime.now(jst)
    date_str = now.strftime("%Y年%m月%d日")
    datetime_str = now.strftime("%Y年%m月%d日 %H:%M")
    output_date = now.strftime("%Y-%m-%d")

    # Create output directory
    output_dir = Path(__file__).parent / "output" / output_date
    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    image_handler = ImageHandler(
        str(images_dir),
        max_width=settings["image"]["max_width"],
        max_height=settings["image"]["max_height"],
        quality=settings["image"]["quality"]
    )

    # Step 1: Login to X
    print("\n📡 Step 1: Logging in to X...")
    if not await scraper.login():
        print("❌ Failed to login to X. Exiting.")
        return

    # Step 2: Scrape tweets
    print("\n📥 Step 2: Scraping tweets...")
    all_tweets = await scraper.scrape_all_accounts(
        accounts,
        since_hours=settings["scraping"]["hours_lookback"],
        max_tweets_per_account=settings["scraping"]["max_tweets_per_account"]
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

    # Step 3: Process with AI
    print("\n🤖 Step 3: Processing with AI...")
    processed_tweets = await ai_processor.batch_process(
        tweets_list,
        max_summary_chars=settings["ai"]["summary_max_chars"]
    )

    if not processed_tweets:
        print("⚠️ No AI-related tweets found")
        article = formatter.format_article(date_str, datetime_str, [])
        formatter.save_article(article, str(output_dir))
        return

    # Step 4: Download images
    print("\n📸 Step 4: Downloading images...")
    image_map = await image_handler.process_all_tweets(processed_tweets)

    # Step 5: Translate to Japanese
    print("\n🇯🇵 Step 5: Translating to Japanese...")
    news_items = []
    
    for i, tweet in enumerate(processed_tweets):
        # Translate summary
        summary_ja = await translator.translate_to_japanese(tweet.summary)
        
        # Generate title
        title = await translator.generate_title(tweet.summary, tweet.author_name)
        
        # Get local images
        local_images = image_map.get(tweet.id, [])
        
        # Create news item
        news_item = formatter.create_news_item(
            tweet,
            summary_ja,
            title,
            local_images,
            i
        )
        news_items.append(news_item)

    # Step 6: Generate article
    print("\n📝 Step 6: Generating article...")
    article = formatter.format_article(date_str, datetime_str, news_items)
    output_path = formatter.save_article(article, str(output_dir))

    # Summary
    print("\n" + "=" * 60)
    print("✅ AI News Collection Complete!")
    print("=" * 60)
    print(f"📅 Date: {date_str}")
    print(f"📰 News items: {len(news_items)}")
    print(f"📸 Images downloaded: {sum(len(v) for v in image_map.values())}")
    print(f"📄 Output: {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
