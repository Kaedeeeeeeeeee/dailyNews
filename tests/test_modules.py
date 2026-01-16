"""
Tests for AI Processor and Formatter Modules
"""

import pytest
import asyncio
import os


# Check for API key
HAS_API_KEY = bool(os.getenv('GEMINI_API_KEY'))


class TestAIProcessor:
    """Test cases for AIProcessor class (requires GEMINI_API_KEY)."""

    @pytest.fixture
    def processor(self):
        from src.ai_processor import AIProcessor
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            pytest.skip("GEMINI_API_KEY not set")
        return AIProcessor(api_key)

    @pytest.mark.asyncio
    @pytest.mark.skipif(not HAS_API_KEY, reason="GEMINI_API_KEY not set")
    async def test_is_ai_related_positive(self, processor):
        """Test that AI-related content is correctly identified."""
        text = "We are excited to announce GPT-5 today!"
        result = await processor.is_ai_related(text)
        assert result is True

    @pytest.mark.asyncio
    @pytest.mark.skipif(not HAS_API_KEY, reason="GEMINI_API_KEY not set")
    async def test_is_ai_related_negative(self, processor):
        """Test that non-AI content is correctly identified."""
        text = "Join us for our annual company picnic this Saturday!"
        result = await processor.is_ai_related(text)
        assert result is False

    @pytest.mark.asyncio
    @pytest.mark.skipif(not HAS_API_KEY, reason="GEMINI_API_KEY not set")
    async def test_generate_summary(self, processor):
        """Test summary generation."""
        text = "OpenAI announced GPT-5 today with improved reasoning capabilities."
        summary = await processor.generate_summary(text, max_chars=100)
        assert len(summary) <= 100
        assert len(summary) > 0


class TestFormatter:
    """Test cases for ArticleFormatter class (no API key required)."""

    def test_generate_toc(self):
        """Test table of contents generation."""
        from src.formatter import ArticleFormatter, NewsItem
        
        formatter = ArticleFormatter()
        items = [
            NewsItem(
                source="OpenAI",
                title="Test Title",
                summary_ja="テスト",
                url="https://example.com",
                images=[],
                emoji="🚀",
                created_at="2026-01-17T10:00:00"
            )
        ]
        
        toc = formatter.generate_toc(items)
        assert "OpenAI" in toc
        assert "Test Title" in toc

    def test_format_no_news(self):
        """Test article generation when there's no news."""
        from src.formatter import ArticleFormatter
        
        formatter = ArticleFormatter()
        article = formatter.format_article("2026年1月17日", "2026年1月17日 07:00", [])
        assert "特に大きなニュースはありませんでした" in article

    def test_format_article_with_news(self):
        """Test article generation with news items."""
        from src.formatter import ArticleFormatter, NewsItem
        
        formatter = ArticleFormatter()
        items = [
            NewsItem(
                source="OpenAI",
                title="GPT-5発表",
                summary_ja="OpenAIは本日、GPT-5を正式に発表しました。",
                url="https://x.com/OpenAI/status/123",
                images=["./images/test.jpg"],
                emoji="🚀",
                created_at="2026-01-17T10:00:00"
            )
        ]
        
        article = formatter.format_article("2026年1月17日", "2026年1月17日 07:00", items)
        assert "AI最新ニュース" in article
        assert "OpenAI" in article
        assert "GPT-5発表" in article
        assert "原文を見る" in article
