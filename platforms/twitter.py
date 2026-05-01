from datetime import datetime
from .base import BaseScraper
from config import ACTOR_IDS


class TwitterScraper(BaseScraper):
    platform_name = "X (Twitter)"

    def get_actor_id(self):
        return ACTOR_IDS["x"]

    def build_input(self, username, date_from, date_to):
    clean = username.lstrip("@").strip()
    return {
        "startUrls": [f"https://x.com/{clean}"],
        "maxItems": max(50, self.smart_limit(date_from, date_to)),
        "sort": "Latest",
    }

    def parse_results(self, raw_items, date_from, date_to):
        posts = []
        for item in raw_items:
            post_date = self.safe_date(
                item.get("createdAt") or item.get("created_at")
                or item.get("date") or item.get("timestamp")
            )
            if not post_date or not (date_from <= post_date <= date_to):
                continue

            likes     = self.safe_int(item.get("likeCount") or item.get("likes") or item.get("favorite_count") or item.get("favoriteCount"))
            comments  = self.safe_int(item.get("replyCount") or item.get("replies") or item.get("reply_count"))
            retweets  = self.safe_int(item.get("retweetCount") or item.get("retweets") or item.get("retweet_count"))
            views     = self.safe_int(item.get("viewCount") or item.get("views", 0))
            bookmarks = self.safe_int(item.get("bookmarkCount") or item.get("bookmarks", 0))

            text  = item.get("text") or item.get("full_text") or item.get("tweet") or ""
            media = item.get("media") or item.get("entities", {}).get("media") or []

            has_video = item.get("isVideo") or any(
                m.get("type") == "video" for m in media if isinstance(m, dict)
            )
            has_image = bool(media) and not has_video
            ptype = "Video" if has_video else "Image" if has_image else "Text"

            thumbnail = ""
            if media and isinstance(media, list) and isinstance(media[0], dict):
                thumbnail = media[0].get("media_url_https") or media[0].get("url") or ""

            url = item.get("url") or item.get("tweetUrl") or ""

            posts.append({
                "platform":        "X (Twitter)",
                "date":            post_date.strftime("%Y-%m-%d"),
                "type":            ptype,
                "caption":         text[:300],
                "likes":           likes,
                "comments":        comments,
                "shares":          retweets,
                "saves":           bookmarks,
                "views":           views,
                "engagement_rate": self.calc_engagement_rate(likes, comments, retweets, views=views),
                "url":             url,
                "thumbnail":       thumbnail,
            })
        return posts
