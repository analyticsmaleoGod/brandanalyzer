from datetime import datetime
from .base import BaseScraper
from config import ACTOR_IDS


class YouTubeScraper(BaseScraper):
    platform_name = "YouTube"

    def get_actor_id(self) -> str:
        return ACTOR_IDS["youtube"]

    def build_input(self, username: str, date_from: datetime, date_to: datetime) -> dict:
        clean = username.strip().lstrip("@").strip("/")
        if "youtube.com" not in clean and "youtu.be" not in clean:
            url = f"https://www.youtube.com/@{clean}"
        else:
            url = clean if clean.startswith("http") else f"https://{clean}"
        return {
            "startUrls": [{"url": url}],
            "maxResults": self.smart_limit(date_from, date_to),
            "sortBy": "date",
        }

    def parse_results(self, raw_items: list, date_from: datetime, date_to: datetime) -> list[dict]:
        posts = []
        for item in raw_items:
            post_date = self.safe_date(
                item.get("date") or item.get("uploadDate") or item.get("publishedAt")
            )
            if post_date is None:
                continue
            if not (date_from <= post_date <= date_to):
                continue

            likes = self.safe_int(item.get("likes") or item.get("likesCount") or item.get("likeCount"))
            comments = self.safe_int(item.get("commentsCount") or item.get("commentCount") or item.get("comments"))
            views = self.safe_int(item.get("viewCount") or item.get("views") or item.get("viewsCount"))

            title = item.get("title") or item.get("text") or ""
            description = item.get("description") or ""
            duration = item.get("duration") or ""

            # YouTube doesn't have shares in public data — use 0
            shares = 0

            er = self.calc_engagement_rate(likes, comments, shares, views=views)

            # Determine type
            if item.get("isShort") or (duration and self._is_short(duration)):
                post_type = "Short"
            elif item.get("isLive") or item.get("isLiveContent"):
                post_type = "Live"
            else:
                post_type = "Video"

            posts.append({
                "platform": "YouTube",
                "date": post_date.strftime("%Y-%m-%d"),
                "type": post_type,
                "caption": title[:300],
                "likes": likes,
                "comments": comments,
                "shares": shares,
                "saves": 0,
                "views": views,
                "engagement_rate": er,
                "url": item.get("url") or item.get("videoUrl") or "",
            })
        return posts

    @staticmethod
    def _is_short(duration_str: str) -> bool:
        """Check if a duration string indicates a Short (<=60s)."""
        try:
            if ":" in str(duration_str):
                parts = str(duration_str).split(":")
                if len(parts) == 2:
                    mins, secs = int(parts[0]), int(parts[1])
                    return mins == 0 and secs <= 60
            return False
        except (ValueError, TypeError):
            return False
