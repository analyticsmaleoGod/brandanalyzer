from datetime import datetime
from .base import BaseScraper
from config import ACTOR_IDS


class TwitterScraper(BaseScraper):
    platform_name = "X (Twitter)"

    def get_actor_id(self) -> str:
        return ACTOR_IDS["x"]

    def build_input(self, username: str, date_from: datetime, date_to: datetime) -> dict:
        clean_username = username.lstrip("@").strip()
        return {
            "handles": [clean_username],
            "tweetsDesired": 500,
            "addUserInfo": True,
        }

    def parse_results(self, raw_items: list, date_from: datetime, date_to: datetime) -> list[dict]:
        posts = []
        for item in raw_items:
            post_date = self.safe_date(
                item.get("createdAt") or item.get("created_at") or item.get("date")
            )
            if post_date is None:
                continue
            if not (date_from <= post_date <= date_to):
                continue

            likes = self.safe_int(item.get("likeCount") or item.get("likes") or item.get("favorite_count"))
            comments = self.safe_int(item.get("replyCount") or item.get("replies") or item.get("reply_count"))
            retweets = self.safe_int(item.get("retweetCount") or item.get("retweets") or item.get("retweet_count"))
            views = self.safe_int(item.get("viewCount") or item.get("views", 0))
            bookmarks = self.safe_int(item.get("bookmarkCount") or item.get("bookmarks", 0))

            text = item.get("text") or item.get("full_text") or item.get("tweet") or ""

            # Determine type
            has_media = item.get("media") or item.get("entities", {}).get("media")
            has_video = item.get("video") or item.get("isVideo")
            if has_video:
                post_type = "Video"
            elif has_media:
                post_type = "Image"
            else:
                post_type = "Text"

            er = self.calc_engagement_rate(likes, comments, retweets, views=views)

            posts.append({
                "platform": "X (Twitter)",
                "date": post_date.strftime("%Y-%m-%d"),
                "type": post_type,
                "caption": text[:300],
                "likes": likes,
                "comments": comments,
                "shares": retweets,
                "saves": bookmarks,
                "views": views,
                "engagement_rate": er,
                "url": item.get("url") or item.get("tweetUrl") or "",
            })
        return posts
