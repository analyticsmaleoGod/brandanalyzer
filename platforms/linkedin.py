from datetime import datetime
from .base import BaseScraper
from config import ACTOR_IDS


class LinkedInScraper(BaseScraper):
    platform_name = "LinkedIn"

    def get_actor_id(self) -> str:
        return ACTOR_IDS["linkedin"]

    def build_input(self, username: str, date_from: datetime, date_to: datetime) -> dict:
        clean = username.strip().strip("/")
        if "linkedin.com" not in clean:
            url = f"https://www.linkedin.com/company/{clean}"
        else:
            url = clean if clean.startswith("http") else f"https://{clean}"
        return {
            "urls": [url],
            "limitPerSource": 500,
        }

    def parse_results(self, raw_items: list, date_from: datetime, date_to: datetime) -> list[dict]:
        posts = []
        for item in raw_items:
            post_date = self.safe_date(
                item.get("postedAt") or item.get("date") or item.get("publishedAt") or item.get("time")
            )
            if post_date is None:
                continue
            if not (date_from <= post_date <= date_to):
                continue

            likes = self.safe_int(item.get("likesCount") or item.get("likes") or item.get("numLikes"))
            comments = self.safe_int(item.get("commentsCount") or item.get("comments") or item.get("numComments"))
            shares = self.safe_int(item.get("repostsCount") or item.get("shares") or item.get("numReposts", 0))
            views = self.safe_int(item.get("impressionCount") or item.get("views", 0))

            text = item.get("text") or item.get("postText") or item.get("commentary") or ""

            # Determine type
            has_image = item.get("imageUrl") or item.get("images")
            has_video = item.get("videoUrl") or item.get("video")
            has_article = item.get("articleUrl") or item.get("article")
            has_document = item.get("documentUrl") or item.get("document")

            if has_video:
                post_type = "Video"
            elif has_document:
                post_type = "Document"
            elif has_article:
                post_type = "Article"
            elif has_image:
                post_type = "Image"
            else:
                post_type = "Text"

            er = self.calc_engagement_rate(likes, comments, shares, views=views)

            posts.append({
                "platform": "LinkedIn",
                "date": post_date.strftime("%Y-%m-%d"),
                "type": post_type,
                "caption": text[:300],
                "likes": likes,
                "comments": comments,
                "shares": shares,
                "saves": 0,
                "views": views,
                "engagement_rate": er,
                "url": item.get("url") or item.get("postUrl") or "",
            })
        return posts
