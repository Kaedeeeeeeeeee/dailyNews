"""
AI Processor Module
Uses Gemini to determine AI relevance and generate summaries.
"""

import os
import asyncio
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
    image_urls: list[str]
    is_ai_related: bool
    summary: str
    created_at: str


class AIProcessor:
    """Processes tweets using Gemini AI."""

    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model

    async def is_ai_related(self, content: str) -> bool:
        """
        Determine if content is AI-related.
        
        Args:
            content: Tweet text to analyze
            
        Returns:
            True if AI-related, False otherwise
        """
        if not content.strip():
            return False

        prompt = f"""判断以下内容是否与 AI/人工智能相关。
考虑以下领域：
- 机器学习、深度学习
- 大语言模型 (LLM)、GPT、Claude 等
- AI 产品发布、更新
- AI 研究论文
- AI 工具和应用
- AI 公司新闻

只回答 "YES" 或 "NO"，不要解释。

内容: {content}"""

        try:
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_name,
                contents=prompt
            )
            answer = response.text.strip().upper()
            return "YES" in answer
        except Exception as e:
            print(f"❌ AI relevance check failed: {e}")
            # Default to True for AI company accounts
            return True

    async def generate_summary(self, content: str, max_chars: int = 300) -> str:
        """
        Generate a concise summary of the content.
        
        Args:
            content: Tweet text to summarize
            max_chars: Maximum characters for summary
            
        Returns:
            Summary text
        """
        if not content.strip():
            return ""

        prompt = f"""以下の内容を日本語で簡潔なニュース要約にしてください。

要件：
1. {max_chars}文字以内
2. 「です・ます」調で統一
3. 専門的で客観的な語調
4. 重要な情報を優先
5. 技術的な詳細や数字を保持
6. 英語の固有名詞（GPT-5、Claude、OpenAI など）はそのまま保持
7. 内容が短い場合は、そのまま日本語に整理

原文: {content}

日本語要約:"""

        try:
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_name,
                contents=prompt
            )
            summary = response.text.strip()
            # Ensure it doesn't exceed max chars
            if len(summary) > max_chars:
                summary = summary[:max_chars-3] + "..."
            return summary
        except Exception as e:
            print(f"Summary generation failed (will retry): {e}")
            # Retry once
            try:
                await asyncio.sleep(2)
                response = await asyncio.to_thread(
                    self.client.models.generate_content,
                    model=self.model_name,
                    contents=prompt
                )
                summary = response.text.strip()
                if len(summary) > max_chars:
                    summary = summary[:max_chars-3] + "..."
                return summary
            except Exception as e2:
                print(f"Summary generation failed after retry: {e2}")
                # Fallback: return original but mark it
                if len(content) > max_chars:
                    return content[:max_chars-3] + "..."
                return content

    async def process_tweet(self, tweet, max_summary_chars: int = 300) -> Optional[ProcessedTweet]:
        """
        Process a single tweet: check relevance and generate summary.
        
        Args:
            tweet: Tweet object from scraper
            max_summary_chars: Maximum summary length
            
        Returns:
            ProcessedTweet if AI-related, None otherwise
        """
        # Check if AI-related
        is_related = await self.is_ai_related(tweet.text)
        if not is_related:
            return None

        # Generate summary
        summary = await self.generate_summary(tweet.text, max_summary_chars)

        return ProcessedTweet(
            id=tweet.id,
            original_text=tweet.text,
            author_username=tweet.author_username,
            author_name=tweet.author_name,
            url=tweet.url,
            image_urls=tweet.image_urls,
            is_ai_related=True,
            summary=summary,
            created_at=tweet.created_at.isoformat() if tweet.created_at else ""
        )

    async def batch_process(
        self,
        tweets: list,
        max_summary_chars: int = 300
    ) -> list[ProcessedTweet]:
        """
        Process multiple tweets in batch.
        
        Args:
            tweets: List of Tweet objects
            max_summary_chars: Maximum summary length
            
        Returns:
            List of ProcessedTweet objects (only AI-related ones)
        """
        processed = []
        
        for tweet in tweets:
            result = await self.process_tweet(tweet, max_summary_chars)
            if result:
                processed.append(result)
            # Small delay to avoid rate limiting
            await asyncio.sleep(0.5)

        print(f"📝 Processed: {len(processed)}/{len(tweets)} tweets are AI-related")
        return processed


async def main():
    """Test the AI processor."""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Please set GEMINI_API_KEY environment variable")
        return

    processor = AIProcessor(api_key)
    
    test_texts = [
        "We're excited to announce GPT-5, our most capable model yet!",
        "Join us for our annual company picnic this Saturday!",
        "New research paper: Scaling Laws for Neural Language Models",
    ]
    
    for text in test_texts:
        is_related = await processor.is_ai_related(text)
        print(f"AI-related: {is_related} | {text[:50]}...")


if __name__ == "__main__":
    asyncio.run(main())
