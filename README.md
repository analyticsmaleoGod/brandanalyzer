# Brand Analyzer v2

Pull brand content performance, comments, keywords & hashtags across social media platforms.

## Quick Start (Mac)

### Cara paling gampang:

1. Download dan extract brand-analyzer-v2.zip
2. Double-click file START.command
3. Kalau muncul warning "unidentified developer" → klik kanan → Open → Open
4. App otomatis install dependencies (first time only) dan buka di browser
5. Paste Apify token di sidebar kiri

Selesai!

### Dimana dapat Apify token:
1. Buka https://console.apify.com/account/integrations
2. Login / sign up (gratis)
3. Copy "Personal API Token"
4. Paste di sidebar app

### Optional — Claude AI Analysis:
- Buka https://console.anthropic.com/settings/keys
- Copy API key, paste di sidebar app (field kedua)

## Features

- Content Performance: 6 platform + AI analysis
- Comment Scraper: multi-URL, auto-detect platform
- Keyword Tracker: multi-keyword, multi-platform
- Hashtag Tracker: multi-hashtag, multi-platform
- Follower Growth: coming soon

## Manual Start (if double-click doesnt work)

Open Terminal and run:
cd ~/Downloads/brand-analyzer-v2
pip3 install -r requirements.txt
streamlit run app.py
