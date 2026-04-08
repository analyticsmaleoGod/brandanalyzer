from datetime import datetime
from .base import BaseScraper
from config import ACTOR_IDS


class TikTokScraper(BaseScraper):
    platform_name = "TikTok"

    def get_actor_id(self) -> str:
        return ACTOR_IDS["tiktok"]

    def build_input(self, username: str, date_from: datetime, date_to: datetime) -> dict:
        clean_username = username.lstrip("@").strip()
        return {
            "profiles": [clean_username],
            "resultsPerPage": 500,
            "shouldDownloadCovers": False,
            "shouldDownloadVideos": False,
        }

    def parse_results(self, raw_items: list, date_from: datetime, date_to: datetime) -> list[dict]:
        posts = []
        for item in raw_items:
            # TikTok timestamps can be unix or ISO
            raw_date = item.get("createTimeISO") or item.get("createTime") or item.get("date")
            if isinstance(raw_date, (int, float)):
                try:
                    post_date = datetime.utcfromtimestamp(raw_date)
                except (OSError, ValueError):
                    continue
            else:
                post_date = self.safe_date(raw_date)

            if post_date is None:
                continue
            if not (date_from <= post_date <= date_to):
                continue

            likes = self.safe_int(item.get("diggCount") or item.get("likes") or item.get("likesCount"))
            comments = self.safe_int(item.get("commentCount") or item.get("comments") or item.get("commentsCount"))
            shares = self.safe_int(item.get("shareCount") or item.get("shares") or item.get("sharesCount"))
            views = self.safe_int(item.get("playCount") or item.get("views") or item.get("viewsCount"))
            saves = self.safe_int(item.get("collectCount") or item.get("saves", 0))

            caption = item.get("text") or item.get("desc") or item.get("caption") or ""

            er = self.calc_engagement_rate(likes, comments, shares, views=views)

            posts.append({
                "platform": "TikTok",
                "date": post_date.strftime("%Y-%m-%d"),
                "type": "Video",
                "caption": caption[:300],
                "likes": likes,
                "comments": comments,
                "shares": shares,
                "saves": saves,
                "views": views,
                "engagement_rate": er,
                "url": item.get("webVideoUrl") or item.get("url") or "",
            })
        return posts
