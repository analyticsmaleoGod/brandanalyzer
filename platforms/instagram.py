from datetime import datetime
from .base import BaseScraper
from config import ACTOR_IDS


class InstagramScraper(BaseScraper):
    platform_name = "Instagram"

    def get_actor_id(self) -> str:
        return ACTOR_IDS["instagram"]

    def build_input(self, username: str, date_from: datetime, date_to: datetime) -> dict:
        clean_username = username.lstrip("@").strip()
        return {
            "username":           [clean_username],
            "resultsLimit":       self.smart_limit(date_from, date_to),
            "onlyPostsNewerThan": date_from.strftime("%Y-%m-%d"),
        }

    def parse_results(self, raw_items: list, date_from: datetime, date_to: datetime) -> list[dict]:
        posts = []
        for item in raw_items:
            post_date = self.safe_date(
                item.get("timestamp") or item.get("taken_at") or item.get("date")
            )
            if post_date is None:
                continue
            if not (date_from <= post_date <= date_to):
                continue

            likes     = self.safe_int(item.get("likesCount") or item.get("likes"))
            comments  = self.safe_int(item.get("commentsCount") or item.get("comments"))
            shares    = self.safe_int(item.get("sharesCount") or item.get("shares", 0))
            saves     = self.safe_int(item.get("savesCount") or item.get("saves", 0))
            views     = self.safe_int(item.get("videoViewCount") or item.get("views", 0))
            followers = self.safe_int(item.get("ownerFollowerCount") or item.get("followers", 0))

            post_type = item.get("type", "").lower()
            if not post_type:
                if item.get("isVideo") or item.get("videoUrl"):
                    post_type = "reel"
                elif item.get("childPosts") or item.get("sidecarChildren"):
                    post_type = "carousel"
                else:
                    post_type = "image"

            caption = item.get("caption") or item.get("text") or ""
            if isinstance(caption, dict):
                caption = caption.get("text", "")

            thumbnail = (
                item.get("displayUrl") or
                item.get("thumbnailUrl") or
                item.get("previewUrl") or ""
            )

            er = self.calc_engagement_rate(likes, comments, shares, followers, views)

            posts.append({
                "platform":        "Instagram",
                "date":            post_date.strftime("%Y-%m-%d"),
                "type":            post_type.capitalize(),
                "caption":         caption[:300],
                "likes":           likes,
                "comments":        comments,
                "shares":          shares,
                "saves":           saves,
                "views":           views,
                "engagement_rate": er,
                "url":             item.get("url") or item.get("shortCode", ""),
                "thumbnail":       thumbnail,
            })
        return posts
