import os
from dotenv import load_dotenv

load_dotenv()

ACTOR_IDS = {
    "instagram": "apify/instagram-post-scraper",
    "tiktok": "clockworks/free-tiktok-scraper",
    "x": "quacker/twitter-scraper",
    "facebook": "apify/facebook-posts-scraper",
    "youtube": "streamers/youtube-scraper",
    "linkedin": "anchor/linkedin-company-scraper",
    "threads": "apify/threads-scraper",
}

PLATFORMS = {
    "instagram": {"label": "Instagram", "icon": "📸", "hint": "@username", "color": "#C13584"},
    "tiktok": {"label": "TikTok", "icon": "🎵", "hint": "@username", "color": "#010101"},
    "x": {"label": "X (Twitter)", "icon": "✖", "hint": "@username", "color": "#000000"},
    "facebook": {"label": "Facebook", "icon": "📘", "hint": "Page name or URL", "color": "#1877F2"},
    "youtube": {"label": "YouTube", "icon": "▶️", "hint": "@channel or URL", "color": "#FF0000"},
    "linkedin": {"label": "LinkedIn", "icon": "💼", "hint": "Company name or URL", "color": "#0A66C2"},
}

# Platforms available for keyword/hashtag search
SEARCH_PLATFORMS = {
    "instagram": {"label": "Instagram", "icon": "📸"},
    "tiktok": {"label": "TikTok", "icon": "🎵"},
    "x": {"label": "X (Twitter)", "icon": "✖"},
    "threads": {"label": "Threads", "icon": "🔗"},
    "youtube": {"label": "YouTube", "icon": "▶️"},
}

# Platforms supported for comment scraping (auto-detected from URL)
COMMENT_PLATFORMS = ["instagram", "tiktok"]


def get_apify_token():
    return os.getenv("APIFY_API_TOKEN", "").strip() or None
