from .instagram import InstagramScraper
from .tiktok import TikTokScraper
from .twitter import TwitterScraper
from .facebook import FacebookScraper
from .youtube import YouTubeScraper
from .linkedin import LinkedInScraper

SCRAPERS = {
    "instagram": InstagramScraper,
    "tiktok": TikTokScraper,
    "x": TwitterScraper,
    "facebook": FacebookScraper,
    "youtube": YouTubeScraper,
    "linkedin": LinkedInScraper,
}
