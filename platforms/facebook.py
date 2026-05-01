from datetime import datetime
from .base import BaseScraper
from config import ACTOR_IDS


class FacebookScraper(BaseScraper):
    platform_name = "Facebook"

    def get_actor_id(self) -> str:
        return ACTOR_IDS["facebook"]

    def build_input(self, username: str, date_from: datetime, date_to: datetime) -> dict:
        clean = username.strip().strip("/")
        if "facebook.com" not in clean:
            url = f"https://www.facebook.com/{clean}"
        else:
            url = clean if clean.startswith("http") else f"https://{clean}"
        return {
            "startUrls":            [{"url": url}],
            "resultsLimit":         self.smart_limit(date_from, date_to),
            "onlyPostsNewerThan":   date_from.strftime("%Y-%m-%d"),
            "onlyPostsOlderThan":   date_to.strftime("%Y-%m-%d"),
        }

    def parse_results(self, raw_items: list, date_from: datetime, date_to: datetime) -> list[dict]:
        posts = []
        for item in raw_items:
            post_date = self.safe_date(
                item.get("time") or item.get("timestamp") or item.get("date") or item.get("postedAt")
            )
            if post_date is None:
                continue
            if not (date_from <= post_date <= date_to):
                continue

            likes    = self.safe_int(item.get("likesCount") or item.get("likes") or item.get("reactions"))
            comments = self.safe_int(item.get("commentsCount") or item.get("comments"))
            shares   = self.safe_int(item.get("sharesCount") or item.get("shares"))
            views    = self.safe_int(item.get("viewsCount") or item.get("views", 0))

            text = item.get("text") or item.get("message") or item.get("postText") or ""

            media_type = item.get("type", "").lower()
            if "video" in media_type or item.get("isVideo"):
                post_type = "Video"
            elif "photo" in media_type or item.get("photoUrl"):
                post_type = "Photo"
            elif "link" in media_type:
                post_type = "Link"
            else:
                post_type = "Post"

            thumbnail = (
                item.get("photoUrl") or
                item.get("thumbnailUrl") or
                item.get("imageUrl") or ""
            )

            er = self.calc_engagement_rate(likes, comments, shares, views=views)

            posts.append({
                "platform":        "Facebook",
                "date":            post_date.strftime("%Y-%m-%d"),
                "type":            post_type,
                "caption":         text[:300],
                "likes":           likes,
                "comments":        comments,
                "shares":          shares,
                "saves":           0,
                "views":           views,
                "engagement_rate": er,
                "url":             item.get("url") or item.get("postUrl") or "",
                "thumbnail":       thumbnail,
            })
        return posts
