"""
AI Processor Module
Uses Gemini to determine AI relevance, generate summaries and titles in one call.
Optimized for parallel processing.
"""

import os
import asyncio
import json
import re
from dataclasses import dataclass
from typing import Optional
from google import genai


@dataclass
class ProcessedTweet:
    """A tweet that has been processed by AI."""
    id: str
    original_text: str
    author_username: str
    author_name: str
    url: str
    is_ai_related: bool
    summary: str
    title: str
    created_at: str
    image_urls: list[str] = None  # Twitter image URLs


class AIProcessor:
    """Processes tweets using Gemini AI with optimized single-call processing."""

    def __init__(self, api_key: str, model: str = "gemini-2.0-flash", max_concurrent: int = 10):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def process_tweet(self, tweet, max_summary_chars: int = 300) -> Optional[ProcessedTweet]:
        """
        Process a single tweet: check relevance, generate summary and title in ONE API call.
        
        Args:
            tweet: Tweet object from scraper
            max_summary_chars: Maximum summary length
            
        Returns:
            ProcessedTweet if AI-related, None otherwise
        """
        if not tweet.text.strip():
            return None

        prompt = f"""あなたはAIニュースの専門家です。以下のツイートを分析し、価値のあるAIニュースかどうか判断してください。

【タスク】
1. このツイートが「価値のあるAI製品・技術ニュース」かどうか判断する
2. 該当する場合のみ、日本語で要約とタイトルを生成する

【✅ 採用するニュース（is_ai_related: true）】
- 新製品・新サービスの発表（例：ChatGPT Go発表、Claude 3.5リリース）
- 新機能・アップデート（例：メモリ機能追加、API変更）
- 料金変更・キャンペーン（例：無料プラン拡大、値下げ）
- 技術的なブレークスルー・研究成果
- 重要なパートナーシップ・統合（例：○○がGPT-4を採用）
- オープンソースリリース

【❌ 除外するニュース（is_ai_related: false）】
- 人物間の争い・論争・批判（例：○○氏が△△氏を批判）
- 講演・イベント・カンファレンスの告知（具体的な発表内容がない場合）
- 採用情報・求人
- 単なる感想・意見・コメント
- 具体的な内容のない宣伝ツイート
- リツイートの依頼やエンゲージメント稼ぎ

【要約の要件】
- {max_summary_chars}文字以内
- 「です・ます」調で統一
- 専門的で客観的な語調
- 重要な情報を優先
- 技術的な詳細や数字を保持
- 英語の固有名詞（GPT-5、Claude、OpenAI など）はそのまま保持

【タイトルの要件】
- 15文字以内
- 日本語で簡潔に
- 製品名や具体的な内容を含める

【出力形式】必ず以下のJSON形式で出力してください：
{{"is_ai_related": true/false, "summary": "要約テキスト", "title": "タイトル"}}

価値のあるニュースでない場合は：
{{"is_ai_related": false, "summary": "", "title": ""}}

【ツイート内容】
発信元: {tweet.author_name} (@{tweet.author_username})
内容: {tweet.text}

【JSON出力】"""

        async with self.semaphore:
            try:
                response = await asyncio.to_thread(
                    self.client.models.generate_content,
                    model=self.model_name,
                    contents=prompt
                )
                result_text = response.text.strip()
                
                # Extract JSON from response
                json_match = re.search(r'\{[^{}]*\}', result_text)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    result = json.loads(result_text)
                
                if not result.get("is_ai_related", False):
                    return None
                
                summary = result.get("summary", "")
                title = result.get("title", "最新ニュース")
                
                # Ensure summary doesn't exceed max chars
                if len(summary) > max_summary_chars:
                    summary = summary[:max_summary_chars-3] + "..."
                
                # Clean title
                title = title.strip('"\'「」『』')
                if not title:
                    title = "最新ニュース"

                return ProcessedTweet(
                    id=tweet.id,
                    original_text=tweet.text,
                    author_username=tweet.author_username,
                    author_name=tweet.author_name,
                    url=tweet.url,
                    is_ai_related=True,
                    summary=summary,
                    title=title,
                    created_at=tweet.created_at.isoformat() if tweet.created_at else "",
                    image_urls=tweet.image_urls if hasattr(tweet, 'image_urls') else []
                )
            except json.JSONDecodeError as e:
                print(f"⚠️ JSON parse error for @{tweet.author_username}: {e}")
                return None
            except Exception as e:
                print(f"❌ Processing failed for @{tweet.author_username}: {e}")
                return None

    async def batch_process(
        self,
        tweets: list,
        max_summary_chars: int = 300
    ) -> list[ProcessedTweet]:
        """
        Process multiple tweets in parallel with controlled concurrency.
        
        Args:
            tweets: List of Tweet objects
            max_summary_chars: Maximum summary length
            
        Returns:
            List of ProcessedTweet objects (only AI-related ones)
        """
        print(f"🚀 Processing {len(tweets)} tweets in parallel (max {self.semaphore._value} concurrent)...")
        
        # Create tasks for all tweets
        tasks = [
            self.process_tweet(tweet, max_summary_chars)
            for tweet in tweets
        ]
        
        # Execute all tasks in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out None results and exceptions
        processed = []
        for result in results:
            if isinstance(result, ProcessedTweet):
                processed.append(result)
            elif isinstance(result, Exception):
                print(f"⚠️ Task failed with exception: {result}")

        print(f"📝 Processed: {len(processed)}/{len(tweets)} tweets are AI-related")
        return processed


async def main():
    """Test the AI processor."""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Please set GEMINI_API_KEY environment variable")
        return

    processor = AIProcessor(api_key)
    
    # Create mock tweet for testing
    @dataclass
    class MockTweet:
        id: str
        text: str
        author_username: str
        author_name: str
        url: str
        created_at: None
    
    test_tweet = MockTweet(
        id="123",
        text="We're excited to announce GPT-5, our most capable model yet!",
        author_username="OpenAI",
        author_name="OpenAI",
        url="https://x.com/OpenAI/status/123",
        created_at=None
    )
    
    result = await processor.process_tweet(test_tweet)
    if result:
        print(f"✅ AI-related: {result.is_ai_related}")
        print(f"📝 Title: {result.title}")
        print(f"📄 Summary: {result.summary}")
    else:
        print("❌ Not AI-related")


if __name__ == "__main__":
    asyncio.run(main())
