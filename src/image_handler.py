"""
Image Handler Module
Downloads and processes images from tweets.
"""

import os
import asyncio
from pathlib import Path
from PIL import Image
import aiohttp
import aiofiles


class ImageHandler:
    """Handles downloading and processing of tweet images."""

    def __init__(
        self,
        output_dir: str,
        max_width: int = 1280,
        max_height: int = 1000,
        quality: int = 85
    ):
        self.output_dir = Path(output_dir)
        self.max_width = max_width
        self.max_height = max_height
        self.quality = quality
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def download_image(self, url: str, filename: str) -> str:
        """
        Download an image from URL.
        
        Args:
            url: Image URL
            filename: Target filename
            
        Returns:
            Path to downloaded file, or empty string on failure
        """
        try:
            # Ensure we get the best quality version
            if 'pbs.twimg.com' in url and '?format=' not in url:
                url = f"{url}?format=jpg&name=large"

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        file_path = self.output_dir / filename
                        content = await response.read()
                        async with aiofiles.open(file_path, 'wb') as f:
                            await f.write(content)
                        return str(file_path)
                    else:
                        print(f"⚠️ Failed to download {url}: HTTP {response.status}")
                        return ""
        except Exception as e:
            print(f"❌ Error downloading {url}: {e}")
            return ""

    def resize_image(self, path: str) -> str:
        """
        Resize image to fit within max dimensions.
        
        Args:
            path: Path to image file
            
        Returns:
            Path to resized image
        """
        try:
            with Image.open(path) as img:
                # Convert RGBA to RGB if necessary
                if img.mode == 'RGBA':
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background

                # Calculate new size maintaining aspect ratio
                width, height = img.size
                if width > self.max_width or height > self.max_height:
                    ratio = min(self.max_width / width, self.max_height / height)
                    new_size = (int(width * ratio), int(height * ratio))
                    img = img.resize(new_size, Image.Resampling.LANCZOS)

                # Save as JPEG with quality setting
                output_path = Path(path).with_suffix('.jpg')
                img.save(output_path, 'JPEG', quality=self.quality, optimize=True)
                
                # Remove original if different extension
                if str(output_path) != path:
                    os.remove(path)
                
                return str(output_path)
        except Exception as e:
            print(f"❌ Error resizing {path}: {e}")
            return path

    async def process_tweet_images(
        self,
        tweet_id: str,
        image_urls: list[str]
    ) -> list[str]:
        """
        Download and process all images from a tweet.
        
        Args:
            tweet_id: Tweet ID for naming files
            image_urls: List of image URLs
            
        Returns:
            List of local file paths
        """
        processed_paths = []

        for i, url in enumerate(image_urls):
            # Generate filename
            ext = 'jpg'
            if '.png' in url.lower():
                ext = 'png'
            elif '.gif' in url.lower():
                ext = 'gif'
            filename = f"{tweet_id}_{i+1}.{ext}"

            # Download
            local_path = await self.download_image(url, filename)
            if local_path:
                # Resize and optimize
                final_path = self.resize_image(local_path)
                processed_paths.append(final_path)

        return processed_paths

    async def process_all_tweets(
        self,
        processed_tweets: list
    ) -> dict[str, list[str]]:
        """
        Process images for all tweets.
        
        Args:
            processed_tweets: List of ProcessedTweet objects
            
        Returns:
            Dict mapping tweet ID to list of local image paths
        """
        image_map = {}
        total_images = 0

        for tweet in processed_tweets:
            if tweet.image_urls:
                paths = await self.process_tweet_images(
                    tweet.id,
                    tweet.image_urls
                )
                image_map[tweet.id] = paths
                total_images += len(paths)

        print(f"📸 Downloaded and processed {total_images} images")
        return image_map


async def main():
    """Test the image handler."""
    handler = ImageHandler("./test_images")
    
    test_url = "https://pbs.twimg.com/media/example.jpg"
    result = await handler.download_image(test_url, "test.jpg")
    print(f"Downloaded to: {result}")


if __name__ == "__main__":
    asyncio.run(main())
