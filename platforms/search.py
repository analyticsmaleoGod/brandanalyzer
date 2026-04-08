from datetime import datetime
from apify_client import ApifyClient
from config import ACTOR_IDS


SEARCH_ACTORS = {
    "instagram_hashtag": "apify/instagram-hashtag-scraper",
    "instagram_keyword": "apify/instagram-scraper",
    "tiktok": "clockworks/free-tiktok-scraper",
    "x": "quacker/twitter-scraper",
    "youtube": "streamers/youtube-scraper",
    "facebook": "apify/facebook-posts-scraper",
    "threads": "apify/threads-scraper",
}


def search_multi(
    api_token: str,
    queries: list,
    platforms: list,
    search_type: str,
    mode: str = "quantity",
    max_per_platform: int = 100,
    date_from: datetime = None,
    date_to: datetime = None,
    progress_callback=None,
) -> list:
    """
    Search for multiple keywords/hashtags across multiple platforms.

    Args:
        queries: list of keyword or hashtag strings
        platforms: list of platform keys e.g. ["instagram", "tiktok"]
        search_type: "keyword" or "hashtag"
        mode: "quantity" or "daterange"
        max_per_platform: max results per platform (quantity mode)
        date_from/date_to: date range filter (daterange mode)
    """
    client = ApifyClient(api_token)
    all_posts = []
    total_ops = len(queries) * len(platforms)
    op = 0

    for query in queries:
        clean_q = query.strip().lstrip("#") if search_type == "hashtag" else query.strip()
        display_q = f"#{clean_q}" if search_type == "hashtag" else clean_q

        for platform in platforms:
            op += 1
            if progress_callback:
                from config import SEARCH_PLATFORMS
                plabel = SEARCH_PLATFORMS.get(platform, {}).get("label", platform)
                progress_callback(f"[{op}/{total_ops}] Searching '{display_q}' on {plabel}...")

            try:
                actor_id = _get_actor(platform, search_type)
                if not actor_id:
                    continue

                limit = max_per_platform if mode == "quantity" else 500
                run_input = _build_input(platform, clean_q, search_type, limit)
                if not run_input:
                    continue

                run = client.actor(actor_id).call(run_input=run_input)
                raw = list(client.dataset(run["defaultDatasetId"]).iterate_items())

                parsed = _parse_results(raw, platform, display_q)

                # Date range filtering
                if mode == "daterange" and date_from and date_to:
                    parsed = [
                        p for p in parsed
                        if p["date"] and date_from.strftime("%Y-%m-%d") <= p["date"] <= date_to.strftime("%Y-%m-%d")
                    ]

                all_posts.extend(parsed)

                if progress_callback:
                    progress_callback(f"✅ {len(parsed)} results for '{display_q}'")

            except Exception as e:
                if progress_callback:
                    progress_callback(f"❌ {display_q} on {platform}: {str(e)}")

    return all_posts


def _get_actor(platform, search_type):
    if platform == "instagram" and search_type == "hashtag":
        return SEARCH_ACTORS["instagram_hashtag"]
    elif platform == "instagram":
        return SEARCH_ACTORS["instagram_keyword"]
    return SEARCH_ACTORS.get(platform, "")


def _build_input(platform, query, search_type, limit):
    q = f"#{query}" if search_type == "hashtag" and platform not in ["instagram"] else query

    if platform == "instagram" and search_type == "hashtag":
        return {"hashtags": [query], "resultsLimit": limit}
    elif platform == "instagram":
        return {"search": query, "resultsLimit": limit, "searchType": "hashtag"}
    elif platform == "tiktok":
        key = "hashtags" if search_type == "hashtag" else "searchQueries"
        return {key: [query], "resultsPerPage": limit}
    elif platform == "x":
        return {"searchTerms": [q], "tweetsDesired": limit}
    elif platform == "youtube":
        return {"searchKeywords": [q], "maxResults": limit}
    elif platform == "facebook":
        return {"searchTerms": [q], "resultsLimit": limit}
    elif platform == "threads":
        return {"searchTerms": [q], "resultsLimit": limit}
    return {}


def _parse_results(raw_items, platform, query):
    posts = []
    for item in raw_items:
        p = _extract_fields(item, platform)
        if not p:
            continue
        p["query"] = query
        posts.append(p)
    return posts


def _extract_fields(item, platform):
    if platform == "instagram":
        caption = item.get("caption") or item.get("text") or ""
        if isinstance(caption, dict):
            caption = caption.get("text", "")
        return _build_post(
            platform="Instagram", item=item, caption=caption,
            likes_keys=["likesCount", "likes"], comment_keys=["commentsCount", "comments"],
            share_keys=["sharesCount", "shares"], view_keys=["videoViewCount", "views"],
            user_keys=["ownerUsername", "username"],
            date_keys=["timestamp", "taken_at", "date"],
            url_keys=["url"],
        )
    elif platform == "tiktok":
        raw_date = item.get("createTimeISO") or item.get("createTime")
        if isinstance(raw_date, (int, float)):
            try:
                raw_date = datetime.utcfromtimestamp(raw_date).strftime("%Y-%m-%dT%H:%M:%SZ")
            except (OSError, ValueError):
                raw_date = None
            item["_parsed_date"] = raw_date
        return _build_post(
            platform="TikTok", item=item,
            caption=item.get("text") or item.get("desc") or "",
            likes_keys=["diggCount", "likes"], comment_keys=["commentCount", "comments"],
            share_keys=["shareCount", "shares"], view_keys=["playCount", "views"],
            user_keys=["authorMeta.name", "author", "nickname"],
            date_keys=["_parsed_date", "createTimeISO", "createTime", "date"],
            url_keys=["webVideoUrl", "url"],
        )
    elif platform == "x":
        return _build_post(
            platform="X (Twitter)", item=item,
            caption=item.get("text") or item.get("full_text") or "",
            likes_keys=["likeCount", "likes", "favorite_count"],
            comment_keys=["replyCount", "replies", "reply_count"],
            share_keys=["retweetCount", "retweets"], view_keys=["viewCount", "views"],
            user_keys=["author.userName", "username"],
            date_keys=["createdAt", "created_at", "date"],
            url_keys=["url", "tweetUrl"],
        )
    elif platform == "youtube":
        return _build_post(
            platform="YouTube", item=item,
            caption=item.get("title") or item.get("text") or "",
            likes_keys=["likes", "likeCount"], comment_keys=["commentsCount", "commentCount"],
            share_keys=[], view_keys=["viewCount", "views"],
            user_keys=["channelName", "author"],
            date_keys=["date", "uploadDate", "publishedAt"],
            url_keys=["url"],
        )
    elif platform == "facebook":
        return _build_post(
            platform="Facebook", item=item,
            caption=item.get("text") or item.get("message") or "",
            likes_keys=["likesCount", "likes"], comment_keys=["commentsCount", "comments"],
            share_keys=["sharesCount", "shares"], view_keys=["viewsCount", "views"],
            user_keys=["pageName", "author"],
            date_keys=["time", "date", "postedAt"],
            url_keys=["url", "postUrl"],
        )
    elif platform == "threads":
        return _build_post(
            platform="Threads", item=item,
            caption=item.get("text") or item.get("caption") or "",
            likes_keys=["likesCount", "likes"], comment_keys=["repliesCount", "comments"],
            share_keys=["repostsCount", "shares"], view_keys=["viewsCount", "views"],
            user_keys=["ownerUsername", "username", "author"],
            date_keys=["timestamp", "date", "postedAt"],
            url_keys=["url", "postUrl"],
        )
    return None


def _build_post(platform, item, caption, likes_keys, comment_keys, share_keys, view_keys, user_keys, date_keys, url_keys):
    likes = _get_int(item, likes_keys)
    comments = _get_int(item, comment_keys)
    shares = _get_int(item, share_keys)
    views = _get_int(item, view_keys)
    username = _get_str(item, user_keys)
    date_str = _get_date(item, date_keys)
    url = _get_str(item, url_keys)

    total = likes + comments + shares
    er = round((total / views) * 100, 2) if views > 0 else 0.0

    return {
        "platform": platform,
        "username": username,
        "date": date_str,
        "caption": caption[:300] if caption else "",
        "likes": likes,
        "comments": comments,
        "shares": shares,
        "views": views,
        "engagement_rate": er,
        "url": url,
    }


def _get_int(item, keys):
    for k in keys:
        if "." in k:
            parts = k.split(".")
            v = item
            for p in parts:
                v = v.get(p, {}) if isinstance(v, dict) else None
                if v is None:
                    break
        else:
            v = item.get(k)
        if v is not None:
            try:
                return int(v)
            except (ValueError, TypeError):
                continue
    return 0


def _get_str(item, keys):
    for k in keys:
        if "." in k:
            parts = k.split(".")
            v = item
            for p in parts:
                v = v.get(p, {}) if isinstance(v, dict) else None
                if v is None:
                    break
            if v:
                return str(v)
        else:
            v = item.get(k)
            if v:
                return str(v)
    return ""


def _get_date(item, keys):
    for k in keys:
        v = item.get(k)
        if not v:
            continue
        if isinstance(v, (int, float)):
            try:
                return datetime.utcfromtimestamp(v).strftime("%Y-%m-%d")
            except (OSError, ValueError):
                continue
        for fmt in ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
            try:
                return datetime.strptime(str(v), fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
    return ""
