import pandas as pd
try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

def is_available(): return HAS_ANTHROPIC

def generate_analysis(api_key, all_posts, platforms_used, date_from, date_to):
    if not HAS_ANTHROPIC: return "Error: pip3 install anthropic"
    if not all_posts: return "No data available."
    df = pd.DataFrame(all_posts)
    data_summary = _build_data_summary(df, platforms_used, date_from, date_to)
    try:
        client = anthropic.Anthropic(api_key=api_key)
        msg = client.messages.create(model="claude-sonnet-4-20250514", max_tokens=2000, messages=[{"role":"user","content":f"""You are a senior social media analyst. Analyze this brand performance data and provide actionable qualitative insights.

DATA:
{data_summary}

TOP 10 POSTS BY ENGAGEMENT:
{_top_posts(df)}

Provide in English, professional but warm tone:
## Executive Summary (2-3 sentences)
## Platform Performance (per platform)
## Content Strategy Insights
## Key Strengths
## Areas for Improvement
## Recommendations (3-5 specific, actionable)

Be concise, data-backed, reference specific numbers."""}])
        return msg.content[0].text
    except Exception as e:
        return f"Error: {str(e)}"

def _build_data_summary(df, platforms_used, date_from, date_to):
    lines = [f"Period: {date_from} to {date_to}", f"Platforms: {', '.join(platforms_used)}", f"Total posts: {len(df)}", f"Avg ER: {df['engagement_rate'].mean():.2f}%", ""]
    for p in platforms_used:
        pdf = df[df["platform"]==p]
        if pdf.empty: continue
        ter = pdf.groupby("type")["engagement_rate"].mean().sort_values(ascending=False)
        lines.append(f"=== {p} === Posts: {len(pdf)}, Avg ER: {pdf['engagement_rate'].mean():.2f}%, Avg likes: {int(pdf['likes'].mean()):,}")
        if len(ter) > 0: lines.append(f"  Best type: {ter.index[0]} ({ter.iloc[0]:.2f}%)")
    return "\n".join(lines)

def _top_posts(df, n=10):
    top = df.nlargest(n, "engagement_rate")
    return "\n".join([f"- [{r['platform']}] {r['date']} | {r['type']} | ER:{r['engagement_rate']}% | \"{r['caption'][:60]}\"" for _,r in top.iterrows()]) or "No posts"
