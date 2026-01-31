"""
Formatter Module
Generates Markdown articles from processed tweets.
"""

from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
import random


@dataclass
class NewsItem:
    """A formatted news item ready for output."""
    source: str  # Company name
    title: str
    summary_ja: str
    url: str
    images: list[str]
    emoji: str
    created_at: str


class ArticleFormatter:
    """Formats processed tweets into a Markdown article."""

    def __init__(self, template_path: Optional[str] = None):
        self.template_path = template_path

    def create_news_item(
        self,
        processed_tweet,
        summary_ja: str,
        title: str,
        image_urls: list[str],
        index: int
    ) -> NewsItem:
        """Create a NewsItem from processed data."""
        return NewsItem(
            source=processed_tweet.author_name,
            title=title,
            summary_ja=summary_ja,
            url=processed_tweet.url,
            images=image_urls,  # Use Twitter CDN URLs directly
            emoji="",
            created_at=processed_tweet.created_at
        )

    def generate_toc(self, news_items: list[NewsItem]) -> str:
        """Generate table of contents."""
        lines = ["## 目次\n"]
        for i, item in enumerate(news_items, 1):
            lines.append(f"{i}. [{item.source}] {item.title}")
        return "\n".join(lines)

    def format_news_item(self, item: NewsItem, index: int) -> str:
        """Format a single news item."""
        lines = [
            f"## {index}. 【{item.source}】{item.title}",
            ""
        ]

        # Add summary
        lines.append(item.summary_ja)
        lines.append("")

        # Add X URL on its own line (no emoji!) - note.com auto-embeds on Enter
        lines.append(item.url)
        lines.append("")

        lines.append("---")

        return "\n".join(lines)

    def format_article(
        self,
        date: str,
        datetime_str: str,
        news_items: list[NewsItem]
    ) -> str:
        """
        Format the complete article.
        
        Args:
            date: Date string (e.g., "2026年1月17日")
            datetime_str: Full datetime string
            news_items: List of NewsItem objects
            
        Returns:
            Complete Markdown article
        """
        if not news_items:
            return self._format_no_news(date, datetime_str)

        lines = [
            f"# カエデのAIニュース【{date}】",
            "",
            "> 本日のAI業界の最新ニュースをお届けします。",
            "",
            self.generate_toc(news_items),
            "",
            "---",
            ""
        ]

        # Add each news item
        for i, item in enumerate(news_items, 1):
            lines.append(self.format_news_item(item, i))
            lines.append("")

        # Footer
        lines.extend([
            f"更新日時：{datetime_str}",
            "",
            "---",
            "",
            "*このニュースは自動収集・翻訳されています。*"
        ])

        return "\n".join(lines)

    def _format_no_news(self, date: str, datetime_str: str) -> str:
        """Format article when there's no news."""
        return f"""# カエデのAIニュース【{date}】

> 本日は特に大きなニュースはありませんでした。

明日また最新ニュースをお届けします！

更新日時：{datetime_str}

---

*このニュースは自動収集・翻訳されています。*
"""

    def save_article(
        self,
        content: str,
        output_dir: str,
        filename: str = "article.md"
    ) -> str:
        """
        Save article to file.
        
        Args:
            content: Article content
            output_dir: Output directory
            filename: Output filename
            
        Returns:
            Path to saved file
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        file_path = output_path / filename
        file_path.write_text(content, encoding='utf-8')
        
        print(f"Saved article to {file_path}")
        return str(file_path)


def main():
    """Test the formatter."""
    formatter = ArticleFormatter()
    
    test_items = [
        NewsItem(
            source="OpenAI",
            title="GPT-5発表",
            summary_ja="OpenAIは本日、GPT-5を正式に発表しました。新モデルは推論能力が大幅に向上しています。",
            url="https://x.com/OpenAI/status/123",
            images=["./images/test.jpg"],
            emoji="🚀",
            created_at="2026-01-17T10:00:00"
        )
    ]
    
    article = formatter.format_article("2026年1月17日", "2026年1月17日 07:00", test_items)
    print(article)


if __name__ == "__main__":
    main()
