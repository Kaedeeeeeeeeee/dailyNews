"""
Twitter/X Scraper Module
Uses Twikit to fetch tweets from specified accounts without API key.
"""

import asyncio
import os
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass
from typing import Optional
from twikit import Client


@dataclass
class Tweet:
    """Represents a scraped tweet."""
    id: str
    text: str
    created_at: datetime
    author_username: str
    author_name: str
    url: str
    image_urls: list[str]
    retweet_count: int
    like_count: int


class TwitterScraper:
    """Scraper for X/Twitter using Twikit."""

    def __init__(self, username: str, password: str, cookies_path: str = "cookies.json"):
        self.username = username
        self.password = password
        self.cookies_path = cookies_path
        self.client = Client('en-US')

    async def login(self) -> bool:
        """Login to X/Twitter. Uses cookies from env or file if available."""
        try:
            # Priority 1: Load cookies from environment variables (for GitHub Actions)
            auth_token = os.getenv('AUTH_TOKEN')
            ct0 = os.getenv('CT0')
            
            if auth_token and ct0:
                self.client.set_cookies({
                    'auth_token': auth_token,
                    'ct0': ct0
                })
                print("✅ Loaded cookies from environment variables")
                return True
            
            # Priority 2: Load cookies from file
            if os.path.exists(self.cookies_path):
                self.client.load_cookies(self.cookies_path)
                print("✅ Loaded cookies from file")
                return True
            
            # Priority 3: Login with username/password
            await self.client.login(
                auth_info_1=self.username,
                password=self.password
            )
            self.client.save_cookies(self.cookies_path)
            print("✅ Logged in and saved cookies")
            return True
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False

    async def get_user_tweets(
        self,
        screen_name: str,
        since_hours: int = 24,
        max_tweets: int = 10
    ) -> list[Tweet]:
        """
        Get recent tweets from a user.
        
        Args:
            screen_name: Twitter username (without @)
            since_hours: Only fetch tweets from the last N hours
            max_tweets: Maximum number of tweets to fetch
            
        Returns:
            List of Tweet objects
        """
        tweets = []
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=since_hours)

        try:
            user = await self.client.get_user_by_screen_name(screen_name)
            if not user:
                print(f"⚠️ User @{screen_name} not found")
                return tweets

            user_tweets = await user.get_tweets('Tweets', count=max_tweets)
            
            for tweet in user_tweets:
                created_at = tweet.created_at_datetime
                if created_at and created_at >= cutoff_time:
                    image_urls = []
                    if hasattr(tweet, 'media') and tweet.media:
                        for media in tweet.media:
                            if hasattr(media, 'media_url_https'):
                                image_urls.append(media.media_url_https)

                    tweets.append(Tweet(
                        id=tweet.id,
                        text=tweet.text or "",
                        created_at=created_at,
                        author_username=screen_name,
                        author_name=user.name or screen_name,
                        url=f"https://x.com/{screen_name}/status/{tweet.id}",
                        image_urls=image_urls,
                        retweet_count=tweet.retweet_count or 0,
                        like_count=tweet.favorite_count or 0
                    ))

            print(f"📥 @{screen_name}: {len(tweets)} tweets (last {since_hours}h)")

        except Exception as e:
            print(f"❌ Error fetching @{screen_name}: {e}")

        return tweets

    async def scrape_all_accounts(
        self,
        accounts: list[dict],
        since_hours: int = 24,
        max_tweets_per_account: int = 10
    ) -> dict[str, list[Tweet]]:
        """
        Scrape tweets from multiple accounts.
        
        Args:
            accounts: List of account dicts with 'username' key
            since_hours: Only fetch tweets from the last N hours
            max_tweets_per_account: Maximum tweets per account
            
        Returns:
            Dict mapping username to list of tweets
        """
        results = {}
        total_tweets = 0

        for account in accounts:
            username = account.get('username', '')
            if not username:
                continue

            tweets = await self.get_user_tweets(
                screen_name=username,
                since_hours=since_hours,
                max_tweets=max_tweets_per_account
            )
            results[username] = tweets
            total_tweets += len(tweets)

            # Rate limiting - small delay between requests
            await asyncio.sleep(1)

        print(f"\n📊 Total: {total_tweets} tweets from {len(accounts)} accounts")
        return results


async def main():
    """Test the scraper."""
    username = os.getenv('X_USERNAME')
    password = os.getenv('X_PASSWORD')

    if not username or not password:
        print("❌ Please set X_USERNAME and X_PASSWORD environment variables")
        return

    scraper = TwitterScraper(username, password)
    if await scraper.login():
        tweets = await scraper.get_user_tweets('OpenAI', since_hours=48)
        for tweet in tweets:
            print(f"\n---\n{tweet.author_username}: {tweet.text[:100]}...")


if __name__ == "__main__":
    asyncio.run(main())
