from datetime import datetime
from apify_client import ApifyClient


COMMENT_ACTORS = {
    "instagram": "apify/instagram-comment-scraper",
    "tiktok": "clockworks/free-tiktok-scraper",
}


def detect_platform(url: str):
    """Auto-detect platform from URL."""
    u = url.strip().lower()
    if "instagram.com" in u:
        return "instagram"
    elif "tiktok.com" in u:
        return "tiktok"
    return None


def parse_urls(text: str) -> list:
    """Parse multi-line URL input into list of {url, platform, short_id}."""
    results = []
    seen = set()
    for line in text.strip().split("\n"):
        url = line.strip()
        if not url or not url.startswith("http") or url in seen:
            continue
        platform = detect_platform(url)
        if platform:
            short_id = url.rstrip("/").split("/")[-1][:15]
            results.append({"url": url, "platform": platform, "short_id": short_id})
            seen.add(url)
    return results


def scrape_comments_multi(api_token: str, urls: list, progress_callback=None) -> list:
    """Scrape comments from multiple URLs across platforms."""
    client = ApifyClient(api_token)
    all_comments = []

    for i, item in enumerate(urls):
        platform = item["platform"]
        actor_id = COMMENT_ACTORS.get(platform)
        if not actor_id:
            continue

        if progress_callback:
            plabel = "Instagram" if platform == "instagram" else "TikTok"
            progress_callback(f"[{i+1}/{len(urls)}] Pulling comments from {plabel}: ...{item['short_id']}")

        try:
            if platform == "instagram":
                run_input = {"directUrls": [item["url"]], "resultsLimit": 1000}
            elif platform == "tiktok":
                run_input = {"postURLs": [item["url"]], "commentsPerPost": 1000, "maxRepliesPerComment": 50}
            else:
                continue

            run = client.actor(actor_id).call(run_input=run_input)
            raw = list(client.dataset(run["defaultDatasetId"]).iterate_items())
            parsed = _parse_comments(raw, platform, item["url"], item["short_id"])
            all_comments.extend(parsed)

            if progress_callback:
                progress_callback(f"✅ {len(parsed)} comments from ...{item['short_id']}")

        except Exception as e:
            if progress_callback:
                progress_callback(f"❌ ...{item['short_id']}: {str(e)}")

    return all_comments


def _parse_comments(raw_items, platform, source_url, short_id):
    comments = []
    for item in raw_items:
        if platform == "instagram":
            username = item.get("ownerUsername") or item.get("username") or ""
            text = item.get("text") or item.get("comment") or ""
            likes = _si(item.get("likesCount") or item.get("likes"))
            raw_date = item.get("timestamp") or item.get("createdAt")
            is_reply = bool(item.get("repliedToCommentId") or item.get("parentId"))
        elif platform == "tiktok":
            username = item.get("uniqueId") or item.get("nickname") or item.get("username") or ""
            text = item.get("text") or item.get("comment") or ""
            likes = _si(item.get("diggCount") or item.get("likes") or item.get("likesCount"))
            raw_date = item.get("createTimeISO") or item.get("createTime") or item.get("date")
            is_reply = bool(item.get("replyCommentId") or item.get("parentId"))
            if isinstance(raw_date, (int, float)):
                try:
                    raw_date = datetime.utcfromtimestamp(raw_date).strftime("%Y-%m-%dT%H:%M:%SZ")
                except (OSError, ValueError):
                    raw_date = None
        else:
            continue

        if not text:
            continue

        comments.append({
            "source_url": source_url,
            "source_id": short_id,
            "platform": "Instagram" if platform == "instagram" else "TikTok",
            "username": username,
            "comment": text[:500],
            "likes": likes,
            "date": _pd(raw_date),
            "is_reply": is_reply,
        })
    return comments


def _pd(raw_date):
    if not raw_date:
        return ""
    for fmt in ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
        try:
            return datetime.strptime(str(raw_date), fmt).strftime("%Y-%m-%d %H:%M")
        except ValueError:
            continue
    return ""


def _si(v, d=0):
    if v is None:
        return d
    try:
        return int(v)
    except (ValueError, TypeError):
        return d
