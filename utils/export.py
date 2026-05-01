import io
from datetime import datetime
import pandas as pd


# ─── Content Performance Export ────────────────────────────────

def _build_summary(df, platforms_used, date_from, date_to):
    rows = []
    total    = len(df)
    avg_er   = round(df["engagement_rate"].mean(), 2) if total > 0 else 0
    total_likes    = int(df["likes"].sum())
    total_comments = int(df["comments"].sum())
    total_shares   = int(df["shares"].sum())

    rows.append({"Section": "CROSS-PLATFORM SUMMARY", "Metric": "Date range",         "Value": f"{date_from} to {date_to}"})
    rows.append({"Section": "",                        "Metric": "Platforms analyzed", "Value": ", ".join(platforms_used)})
    rows.append({"Section": "",                        "Metric": "Total content",      "Value": total})
    rows.append({"Section": "",                        "Metric": "Avg. engagement rate (%)", "Value": avg_er})
    rows.append({"Section": "",                        "Metric": "Total likes",        "Value": total_likes})
    rows.append({"Section": "",                        "Metric": "Total comments",     "Value": total_comments})
    rows.append({"Section": "",                        "Metric": "Total shares",       "Value": total_shares})
    rows.append({"Section": "",                        "Metric": "Total interactions", "Value": total_likes + total_comments + total_shares})

    try:
        d1    = datetime.strptime(date_from, "%Y-%m-%d")
        d2    = datetime.strptime(date_to,   "%Y-%m-%d")
        weeks = max((d2 - d1).days / 7, 1)
        rows.append({"Section": "", "Metric": "Posting freq (per week)", "Value": round(total / weeks, 1)})
    except ValueError:
        pass

    rows.append({"Section": "", "Metric": "", "Value": ""})

    for p in platforms_used:
        pdf = df[df["platform"] == p]
        if pdf.empty:
            continue
        pc = len(pdf)
        rows.append({"Section": f"PLATFORM: {p.upper()}", "Metric": "Total posts",    "Value": pc})
        rows.append({"Section": "",                        "Metric": "Avg. ER (%)",    "Value": round(pdf["engagement_rate"].mean(), 2)})
        rows.append({"Section": "",                        "Metric": "Total likes",    "Value": int(pdf["likes"].sum())})
        rows.append({"Section": "",                        "Metric": "Total comments", "Value": int(pdf["comments"].sum())})
        rows.append({"Section": "",                        "Metric": "Total shares",   "Value": int(pdf["shares"].sum())})
        rows.append({"Section": "",                        "Metric": "Total views",    "Value": int(pdf["views"].sum())})
        if not pdf["type"].empty:
            top = pdf["type"].value_counts()
            rows.append({"Section": "", "Metric": "Top content type",
                         "Value": f"{top.index[0]} ({round(top.iloc[0]/pc*100,1)}%)"})
        rows.append({"Section": "", "Metric": "", "Value": ""})

    return pd.DataFrame(rows)


def _rename_posts(df):
    """Rename columns for display including thumbnail."""
    col_map = {
        "platform":        "Platform",
        "date":            "Date",
        "type":            "Type",
        "caption":         "Caption / Title",
        "likes":           "Likes",
        "comments":        "Comments",
        "shares":          "Shares",
        "saves":           "Saves",
        "views":           "Views",
        "engagement_rate": "ER (%)",
        "url":             "URL",
        "thumbnail":       "Thumbnail URL",
    }
    return df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})


def export_to_excel(all_posts, platforms_used, date_from, date_to, ai_analysis=""):
    df = pd.DataFrame(all_posts)
    if df.empty:
        df = pd.DataFrame(columns=[
            "platform","date","type","caption","likes","comments",
            "shares","saves","views","engagement_rate","url","thumbnail"
        ])
    if "thumbnail" not in df.columns:
        df["thumbnail"] = ""

    summary_df = _build_summary(df, platforms_used, date_from, date_to)
    posts_df   = df.sort_values("date", ascending=False) if not df.empty else df
    posts_df   = _rename_posts(posts_df)

    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        # Sheet 1: Summary
        summary_df.to_excel(w, sheet_name="Summary", index=False)

        # Sheet 2: All Posts
        posts_df.to_excel(w, sheet_name="All Posts", index=False)

        # Sheet per platform
        for p in platforms_used:
            pdf = df[df["platform"] == p]
            if pdf.empty:
                continue
            sheet_name = p[:31]  # Excel max 31 chars
            _rename_posts(pdf.sort_values("date", ascending=False)).to_excel(
                w, sheet_name=sheet_name, index=False
            )

        # AI Analysis sheet
        if ai_analysis:
            ai_df = pd.DataFrame([{"Analysis": line} for line in ai_analysis.split("\n")])
            ai_df.to_excel(w, sheet_name="AI Analysis", index=False)

        _autofit(w)
    return buf.getvalue()


def export_to_csv(all_posts):
    df = pd.DataFrame(all_posts)
    if df.empty:
        return ""
    return df.sort_values("date", ascending=False).to_csv(index=False)


# ─── Comments Export ──────────────────────────────────────────

def export_comments_to_excel(comments):
    df = pd.DataFrame(comments)
    if df.empty:
        return _empty_bytes()

    for col, default in [
        ("source", "unknown"), ("source_url", ""), ("platform", "unknown"),
        ("username", ""),      ("comment", ""),    ("likes", 0),
        ("date", ""),          ("is_reply", False),
    ]:
        if col not in df.columns:
            df[col] = default

    all_df = df.sort_values("likes", ascending=False).rename(columns={
        "source":     "Source Post", "platform": "Platform",
        "username":   "Username",    "comment":  "Comment",
        "likes":      "Likes",       "date":     "Date",
        "is_reply":   "Is Reply",    "source_url": "Source URL",
    })

    breakdown = df.groupby(["source_url", "source", "platform"]).agg(
        total_comments=("comment", "count"),
        replies=("is_reply", "sum"),
        avg_likes=("likes", "mean"),
        max_likes=("likes", "max"),
    ).reset_index()
    breakdown.columns = ["Source URL","Source Post","Platform","Total Comments","Replies","Avg Likes","Max Likes"]
    breakdown["Avg Likes"] = breakdown["Avg Likes"].round(1)

    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        all_df.to_excel(w, sheet_name="All Comments", index=False)
        breakdown.to_excel(w, sheet_name="Per Post Breakdown", index=False)
        _autofit(w)
    return buf.getvalue()


# ─── Keyword / Hashtag Search Export ──────────────────────────

def export_search_to_excel(posts, queries, search_type="keyword"):
    df = pd.DataFrame(posts)
    if df.empty:
        return _empty_bytes()

    label = "Keyword" if search_type == "keyword" else "Hashtag"

    summary_rows = []
    summary_rows.append({"Section": "OVERVIEW", "Metric": f"Total {label.lower()}s searched", "Value": len(queries)})
    summary_rows.append({"Section": "",          "Metric": "Total posts found",  "Value": len(df)})
    summary_rows.append({"Section": "",          "Metric": "Avg. ER (%)",        "Value": round(df["engagement_rate"].mean(), 2) if len(df) else 0})
    summary_rows.append({"Section": "",          "Metric": "Total views",        "Value": int(df["views"].sum())})
    summary_rows.append({"Section": "",          "Metric": "",                   "Value": ""})

    for q in queries:
        qdf = df[df["query"] == q]
        if qdf.empty:
            continue
        summary_rows.append({"Section": f"{label.upper()}: {q}", "Metric": "Posts found",   "Value": len(qdf)})
        summary_rows.append({"Section": "",                       "Metric": "Avg. ER (%)",   "Value": round(qdf["engagement_rate"].mean(), 2)})
        summary_rows.append({"Section": "",                       "Metric": "Total views",   "Value": int(qdf["views"].sum())})
        summary_rows.append({"Section": "",                       "Metric": "Top platform",
                              "Value": qdf["platform"].value_counts().index[0] if len(qdf) else "—"})
        summary_rows.append({"Section": "", "Metric": "", "Value": ""})

    summary_df = pd.DataFrame(summary_rows)

    all_df = df.sort_values("likes", ascending=False).rename(columns={
        "query": label, "platform": "Platform", "username": "Username",
        "date":  "Date", "caption": "Caption",  "likes":    "Likes",
        "comments": "Comments", "shares": "Shares", "views": "Views",
        "engagement_rate": "ER (%)", "url": "URL",
    })

    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        summary_df.to_excel(w, sheet_name="Summary", index=False)
        all_df.to_excel(w, sheet_name="All Posts", index=False)
        for q in queries:
            qdf = df[df["query"] == q]
            if qdf.empty:
                continue
            safe_name = q[:28].replace("/","").replace("\\","").replace("#","")
            qdf.to_excel(w, sheet_name=safe_name, index=False)
        _autofit(w)
    return buf.getvalue()


# ─── Helpers ──────────────────────────────────────────────────

def _autofit(writer):
    for sheet_name in writer.sheets:
        ws = writer.sheets[sheet_name]
        for col in ws.columns:
            mx = max(len(str(cell.value or "")) for cell in col)
            ws.column_dimensions[col[0].column_letter].width = min(mx + 3, 60)


def _empty_bytes():
    buf = io.BytesIO()
    pd.DataFrame().to_excel(buf, engine="openpyxl", index=False)
    return buf.getvalue()
