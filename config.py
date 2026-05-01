import os
from dotenv import load_dotenv

load_dotenv()

ACTOR_IDS = {
    "instagram": "apify/instagram-post-scraper",
    "tiktok": "clockworks/free-tiktok-scraper",
    "x": "apidojo/twitter-scraper-lite",
    "facebook": "apify/facebook-posts-scraper",
    "youtube": "streamers/youtube-scraper",
    "linkedin": "anchor/linkedin-company-scraper",
    "threads": "george.the.developer/threads-scraper",
}

PLATFORMS = {
    "instagram": {"label": "Instagram", "icon": "📸", "hint": "@username", "color": "#C13584"},
    "tiktok": {"label": "TikTok", "icon": "🎵", "hint": "@username", "color": "#010101"},
    "x": {"label": "X (Twitter)", "icon": "✖", "hint": "@username", "color": "#000000"},
    "facebook": {"label": "Facebook", "icon": "📘", "hint": "Page name or URL", "color": "#1877F2"},
    "youtube": {"label": "YouTube", "icon": "▶️", "hint": "@channel or URL", "color": "#FF0000"},
    "linkedin": {"label": "LinkedIn", "icon": "💼", "hint": "Company name or URL", "color": "#0A66C2"},
}

SEARCH_PLATFORMS = {
    "instagram": {"label": "Instagram", "icon": "📸"},
    "tiktok": {"label": "TikTok", "icon": "🎵"},
    "x": {"label": "X (Twitter)", "icon": "✖"},
    "threads": {"label": "Threads", "icon": "🔗"},
    "youtube": {"label": "YouTube", "icon": "▶️"},
}

COMMENT_PLATFORMS = {
    "instagram.com": "instagram",
    "tiktok.com": "tiktok",
}


def get_apify_token():
    """Get token from: Streamlit Cloud secrets → .env → None"""
    try:
        import streamlit as st
        token = st.secrets.get("APIFY_API_TOKEN", "")
        if token:
            return token.strip()
    except Exception:
        pass
    return os.getenv("APIFY_API_TOKEN", "").strip() or None
