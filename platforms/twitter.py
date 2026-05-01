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
            "twitterHandles": [clean],
            "start": date_from.strftime("%Y-%m-%d"),
            "end": date_to.strftime("%Y-%m-%d"),
            "maxItems": max(50, self.smart_limit(date_from, date_to)),
            "sort": "Latest",
            "includeSearchTerms": False,
        }

    def parse_results(self, raw_items, date_from, date_to):
        posts = []
        for item in raw_items:
            raw_date = item.get("createdAt") or item.get("created_at") or item.get("date")
            post_date = None
            if raw_date:
                try:
                    from email.utils import parsedate_to_datetime
                    post_date = parsedate_to_datetime(raw_date).replace(tzinfo=None)
                except Exception:
                    post_date = self.safe_date(raw_date)

            if not post_date or not (date_from <= post_date <= date_to):
                continue

            likes     = self.safe_int(item.get("likeCount") or item.get("likes") or item.get("favoriteCount"))
            comments  = self.safe_int(item.get("replyCount") or item.get("replies") or item.get("reply_count"))
            retweets  = self.safe_int(item.get("retweetCount") or item.get("retweets"))
            views     = self.safe_int(item.get("viewCount") or item.get("views", 0))
            bookmarks = self.safe_int(item.get("bookmarkCount") or item.get("bookmarks", 0))
            followers = self.safe_int(
                (item.get("author") or {}).get("followers") or
                item.get("ownerFollowerCount") or 0
            )

            text = item.get("text") or item.get("fullText") or ""

            media = item.get("media") or []
            has_video = any(
                isinstance(m, dict) and m.get("type") in ("video", "animated_gif")
                for m in item.get("extendedEntities", {}).get("media", [])
            )
            has_image = bool(media) and not has_video
            ptype = "Video" if has_video else "Image" if has_image else "Text"

            thumbnail = ""
            if isinstance(media, list) and media:
                first = media[0]
                if isinstance(first, str):
                    thumbnail = first
                elif isinstance(first, dict):
                    thumbnail = first.get("media_url_https") or first.get("url") or ""

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
                "engagement_rate": self.calc_engagement_rate(likes, comments, retweets, followers=followers, views=views),
                "url":             item.get("url") or item.get("twitterUrl") or "",
                "thumbnail":       thumbnail,
            })
        return posts
