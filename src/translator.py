"""
Translator Module
Translates content to Japanese using Gemini.
"""

import os
import asyncio
from google import genai


class Translator:
    """Translates text to Japanese using Gemini AI."""

    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model

    async def translate_to_japanese(self, text: str) -> str:
        """
        Translate text to Japanese.
        
        Args:
            text: Text to translate (any language)
            
        Returns:
            Japanese translation
        """
        if not text.strip():
            return ""

        prompt = f"""以下のAIニュースの要約を日本語に翻訳してください。

要件：
1. 正式で専門的な語調を使用
2. 技術用語は正確に翻訳
3. 英語の固有名詞（GPT-5、Claude、OpenAI など）はそのまま保持
4. 自然で読みやすい日本語にする
5. 「です・ます」調で統一

原文：
{text}

日本語訳："""

        try:
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_name,
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            print(f"❌ Translation failed: {e}")
            return text  # Return original if translation fails

    async def batch_translate(self, texts: list[str]) -> list[str]:
        """
        Translate multiple texts to Japanese.
        
        Args:
            texts: List of texts to translate
            
        Returns:
            List of Japanese translations
        """
        translations = []
        
        for text in texts:
            translation = await self.translate_to_japanese(text)
            translations.append(translation)
            # Rate limiting
            await asyncio.sleep(0.5)

        print(f"🇯🇵 Translated {len(translations)} items to Japanese")
        return translations

    async def generate_title(self, summary: str, author: str) -> str:
        """
        Generate a short Japanese title for the news item.
        
        Args:
            summary: News summary (may be in English or Japanese)
            author: Author/company name
            
        Returns:
            Short Japanese title
        """
        prompt = f"""以下のニュース内容から、日本語で短いタイトル（15文字以内）を作成してください。
内容が英語の場合は、日本語に翻訳してタイトルを作成してください。
タイトルのみを出力し、他に何も含めないでください。

内容：{summary[:200]}
発信元：{author}

日本語タイトル："""

        try:
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_name,
                contents=prompt
            )
            title = response.text.strip()
            # Remove quotes if present
            title = title.strip('"\'"「」『』')
            if title:
                return title
            return "最新ニュース"
        except Exception as e:
            print(f"Title generation failed (will retry): {e}")
            # Retry once
            try:
                await asyncio.sleep(2)
                response = await asyncio.to_thread(
                    self.client.models.generate_content,
                    model=self.model_name,
                    contents=prompt
                )
                title = response.text.strip()
                title = title.strip('"\'"「」『』')
                if title:
                    return title
                return "最新ニュース"
            except Exception as e2:
                print(f"Title generation failed after retry: {e2}")
                return "最新ニュース"


async def main():
    """Test the translator."""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Please set GEMINI_API_KEY environment variable")
        return

    translator = Translator(api_key)
    
    test_text = "OpenAI announced GPT-5 today with improved reasoning capabilities."
    result = await translator.translate_to_japanese(test_text)
    print(f"Original: {test_text}")
    print(f"Japanese: {result}")


if __name__ == "__main__":
    asyncio.run(main())
