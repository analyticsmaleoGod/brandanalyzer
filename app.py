import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

from config import PLATFORMS, SEARCH_PLATFORMS, get_apify_token
from platforms import SCRAPERS
from platforms.comments import parse_urls, scrape_comments_multi
from platforms.search import search_multi
from utils.export import export_to_excel, export_to_csv, export_comments_to_excel, export_search_to_excel
from utils.ai_analysis import is_available as ai_ok, generate_analysis

# Page config
st.set_page_config(page_title="Brand Analyzer", page_icon="\U0001F4CA", layout="wide", initial_sidebar_state="expanded")
st.markdown("""<style>
.block-container{max-width:920px;padding-top:2rem}
div[data-testid="stMetric"]{background:#f8f9fa;padding:16px;border-radius:10px}
</style>""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## Settings")
    st.markdown("---")
    env_tok = get_apify_token()
    st.markdown("### Apify API Token")
    tok_in = st.text_input("Paste your Apify token", value=env_tok or "", type="password",
                           help="https://console.apify.com/account/integrations")
    api_token = tok_in.strip() or env_tok
    if api_token:
        st.success("Apify token configured")
    else:
        st.warning("No Apify token")
    st.markdown("---")
    st.markdown("### Claude API Key")
    st.caption("Optional - enables AI analysis")
    claude_key = st.text_input("Paste Claude API key", type="password",
                               help="https://console.anthropic.com/settings/keys")
    if claude_key:
        st.success("Claude key configured")
    else:
        st.info("Optional - skip if you don't have one")
    st.markdown("---")
    st.caption("Brand Analyzer v2.0")

# Header
st.markdown("# Brand Analyzer")
st.markdown("Content performance, comments, keywords & hashtags - across platforms")

# Tabs
T_CP, T_FG, T_CMT, T_KW, T_HT = st.tabs([
    "Content Performance", "Follower Growth", "Comment Scraper",
    "Keyword Tracker", "Hashtag Tracker",
])
pkeys = list(PLATFORMS.keys())

# Helpers
def plat_grid(prefix, default_on=True):
    sel = {}
    r1, r2 = st.columns(3), st.columns(3)
    for i, k in enumerate(pkeys):
        pf = PLATFORMS[k]
        with (r1 + r2)[i]:
            on = st.checkbox(f"{pf['icon']} {pf['label']}", value=default_on, key=f"{prefix}_c_{k}")
            u = st.text_input("u", placeholder=pf["hint"], key=f"{prefix}_u_{k}",
                              disabled=not on, label_visibility="collapsed")
            if on and u.strip():
                sel[k] = u.strip()
    return sel

def date_pick(prefix):
    a, b = st.columns(2)
    with a:
        df = st.date_input("From", value=datetime.now() - timedelta(days=90), max_value=datetime.now(), key=f"{prefix}_f")
    with b:
        dt = st.date_input("To", value=datetime.now(), max_value=datetime.now(), key=f"{prefix}_t")
    return df, dt

def fmt_num(n):
    if n >= 1e6: return f"{n/1e6:.1f}M"
    if n >= 1e3: return f"{n/1e3:.1f}K"
    return f"{n:,}"


# TAB 1: CONTENT PERFORMANCE
with T_CP:
    st.markdown("### Select platforms & enter usernames")
    st.caption("Toggle on/off - only selected platforms will be pulled.")
    sel = plat_grid("cp")
    st.markdown("")
    st.markdown("### Date range")
    d_from, d_to = date_pick("cp")
    st.markdown("")
    n = len(sel)
    can = bool(api_token and sel and d_from < d_to)
    if not api_token:
        st.info("Enter Apify API token in the sidebar to start.")

    if st.button(f"Pull Data - {n} platform{'s' if n!=1 else ''}", type="primary",
                 use_container_width=True, disabled=not can, key="cp_go"):
        posts, errs = [], []
        bar, status = st.progress(0), st.empty()
        for i, (pk, uname) in enumerate(sel.items()):
            pf = PLATFORMS[pk]
            status.markdown(f"Pulling **{pf['label']}** for `{uname}`...")
            sc = SCRAPERS.get(pk)
            if not sc:
                errs.append(f"{pf['label']}: not found")
                continue
            try:
                r = sc(api_token).scrape(uname,
                    datetime(d_from.year, d_from.month, d_from.day),
                    datetime(d_to.year, d_to.month, d_to.day, 23, 59, 59))
                posts.extend(r)
                status.markdown(f"**{pf['label']}** - {len(r)} posts")
            except Exception as e:
                errs.append(f"{pf['label']}: {e}")
            bar.progress((i+1)/len(sel))
        bar.empty()
        status.empty()
        plats = [PLATFORMS[k]["label"] for k in sel]
        ai = ""
        if claude_key and posts:
            with st.spinner("AI analyzing..."):
                ai = generate_analysis(claude_key, posts, plats, d_from.strftime("%Y-%m-%d"), d_to.strftime("%Y-%m-%d"))
        st.session_state["cp_r"] = posts
        st.session_state["cp_e"] = errs
        st.session_state["cp_p"] = plats
        st.session_state["cp_from_str"] = d_from.strftime("%Y-%m-%d")
        st.session_state["cp_to_str"] = d_to.strftime("%Y-%m-%d")
        st.session_state["cp_ai"] = ai

    if st.session_state.get("cp_r"):
        posts = st.session_state["cp_r"]
        df = pd.DataFrame(posts)
        plats = st.session_state["cp_p"]
        d_f, d_t = st.session_state["cp_from_str"], st.session_state["cp_to_str"]
        ai = st.session_state.get("cp_ai", "")
        st.markdown("---")
        for e in st.session_state.get("cp_e", []):
            st.warning(e)
        st.success(f"**{len(df)} posts** across {len(plats)} platforms")
        c1,c2,c3,c4 = st.columns(4)
        with c1: st.metric("Total", f"{len(df):,}")
        with c2: st.metric("Avg. ER", f"{df['engagement_rate'].mean():.2f}%" if len(df) else "0%")
        with c3: st.metric("Interactions", fmt_num(int(df[["likes","comments","shares"]].sum().sum())))
        with c4:
            try:
                wk = max((datetime.strptime(d_t,"%Y-%m-%d")-datetime.strptime(d_f,"%Y-%m-%d")).days/7,1)
                st.metric("Freq.", f"{len(df)/wk:.1f}x/wk")
            except:
                st.metric("Freq.", "-")
        st.markdown("### Per platform")
        for i, p in enumerate(plats):
            if i % 3 == 0:
                cols = st.columns(min(len(plats)-i, 3))
            with cols[i%3]:
                pdf = df[df["platform"]==p]
                st.markdown(f"**{p}** - {len(pdf)} posts - {pdf['engagement_rate'].mean():.1f}% ER")
        if ai:
            st.markdown("### AI Analysis")
            st.markdown(ai)
        st.markdown("### All posts")
        disp = df[["platform","date","type","caption","likes","comments","shares","views","engagement_rate"]].copy()
        disp.columns = ["Platform","Date","Type","Caption","Likes","Comments","Shares","Views","ER (%)"]
        st.dataframe(disp.sort_values("Date",ascending=False), use_container_width=True, height=400, hide_index=True)
        st.markdown("### Download")
        c1,c2,_ = st.columns([1,1,2])
        with c1:
            st.download_button("Download .xlsx", export_to_excel(posts,plats,d_f,d_t,ai),
                f"content_{d_f}_{d_t}.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True, key="cp_dx")
        with c2:
            st.download_button("Download .csv", export_to_csv(posts), f"content_{d_f}_{d_t}.csv",
                "text/csv", use_container_width=True, key="cp_dc")


# TAB 2: FOLLOWER GROWTH
with T_FG:
    st.markdown("""<div style="text-align:center;padding:50px 20px;">
        <span style="background:#EEEDFE;color:#534AB7;padding:4px 16px;border-radius:20px;font-size:13px;font-weight:500;">Coming soon</span>
        <p style="font-size:48px;margin:16px 0;">📈</p>
        <p style="color:#666;max-width:400px;margin:0 auto;">Follower growth tracking via Social Blade - coming next.</p>
    </div>""", unsafe_allow_html=True)


# TAB 3: COMMENT SCRAPER
with T_CMT:
    st.markdown("### Paste post URLs")
    st.caption("One URL per line - mix Instagram & TikTok links freely. System auto-detects platform.")
    url_text = st.text_area("URLs", height=150,
        placeholder="https://www.instagram.com/p/ABC123/\nhttps://www.tiktok.com/@nike/video/7345678901234\n...",
        key="cmt_urls", label_visibility="collapsed")

    parsed = parse_urls(url_text) if url_text.strip() else []
    if parsed:
        ig_n = sum(1 for p in parsed if p["platform"] == "instagram")
        tt_n = sum(1 for p in parsed if p["platform"] == "tiktok")
        parts = []
        if ig_n: parts.append(f"{ig_n} Instagram")
        if tt_n: parts.append(f"{tt_n} TikTok")
        st.caption(f"Detected: {' + '.join(parts)} = {len(parsed)} URLs total")

    can_cmt = bool(api_token and parsed)
    if st.button(f"Pull Comments - {len(parsed)} posts", type="primary",
                 use_container_width=True, disabled=not can_cmt, key="cmt_go"):
        status = st.empty()
        def cmt_cb(msg): status.markdown(msg)
        comments = scrape_comments_multi(api_token, parsed, cmt_cb)
        status.empty()
        st.session_state["cmt_r"] = comments

    if st.session_state.get("cmt_r"):
        cmt = st.session_state["cmt_r"]
        if cmt:
            cdf = pd.DataFrame(cmt)
            st.markdown("---")
            st.success(f"**{len(cdf)} comments** from {cdf['source'].nunique()} posts")
            c1,c2,c3,c4 = st.columns(4)
            with c1: st.metric("Comments", f"{len(cdf):,}")
            with c2: st.metric("Posts scraped", cdf["source"].nunique())
            with c3: st.metric("Replies", int(cdf["is_reply"].sum()))
            with c4: st.metric("Avg. likes", f"{cdf['likes'].mean():.1f}")
            st.markdown("### Comments")
            disp = cdf[["source","platform","username","comment","likes","date","is_reply"]].copy()
            disp.columns = ["Source Post","Platform","Username","Comment","Likes","Date","Reply"]
            st.dataframe(disp.sort_values("Likes",ascending=False), use_container_width=True, height=400, hide_index=True)
            st.markdown("### Download")
            c1,c2,_ = st.columns([1,1,2])
            with c1:
                st.download_button("Download .xlsx", export_comments_to_excel(cmt), "comments.xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True, key="cmt_dx")
            with c2:
                st.download_button("Download .csv", cdf.to_csv(index=False), "comments.csv",
                    "text/csv", use_container_width=True, key="cmt_dc")
        else:
            st.markdown("---")
            st.warning("No comments found. Check URLs.")


# SHARED SEARCH TAB FUNCTION
def search_tab(tab_key, search_type, label, placeholder, icon):
    st.markdown(f"### Enter {label.lower()}s")
    st.caption(f"Separate multiple {label.lower()}s with commas.")

    raw = st.text_input(f"{label}s", placeholder=placeholder, key=f"{tab_key}_input",
                        help=f"Separate multiple {label.lower()}s with commas")
    queries = [q.strip() for q in raw.split(",") if q.strip()] if raw else []
    if queries:
        st.caption(f"{len(queries)} {label.lower()}{'s' if len(queries)>1 else ''}: " + ", ".join([f"`{q}`" for q in queries]))

    st.markdown("### Select platforms")
    sp_keys = list(SEARCH_PLATFORMS.keys())
    plat_cols = st.columns(len(sp_keys))
    sel_plats = []
    for i, k in enumerate(sp_keys):
        sp = SEARCH_PLATFORMS[k]
        with plat_cols[i]:
            if st.checkbox(f"{sp['icon']} {sp['label']}", value=i<2, key=f"{tab_key}_p_{k}"):
                sel_plats.append(k)

    st.markdown("### Result limit")
    mode = st.radio("Mode", ["By quantity (per platform)", "By date range"],
                    horizontal=True, key=f"{tab_key}_mode", label_visibility="collapsed")

    max_qty, dt_from, dt_to = 100, None, None
    if "quantity" in mode:
        max_qty = st.slider("Max results per platform", 10, 1000, 100, 10, key=f"{tab_key}_qty")
        mode_key = "quantity"
    else:
        c1, c2 = st.columns(2)
        with c1: dt_from = st.date_input("From", value=datetime.now()-timedelta(days=90), key=f"{tab_key}_df")
        with c2: dt_to = st.date_input("To", value=datetime.now(), key=f"{tab_key}_dt")
        mode_key = "daterange"
        # Smart limit: pull enough to cover the date range, not a fixed 100
        days = max((dt_to - dt_from).days, 1)
        max_qty = max(30, min(int(days * 3 * 1.2), 500))

    st.markdown("")
    can = bool(api_token and queries and sel_plats)
    btn_label = f"{icon} Search - {len(queries)} {label.lower()}{'s' if len(queries)>1 else ''} x {len(sel_plats)} platform{'s' if len(sel_plats)>1 else ''}"

    if st.button(btn_label, type="primary", use_container_width=True, disabled=not can, key=f"{tab_key}_go"):
        status = st.empty()
        def search_cb(msg): status.markdown(msg)
        results = search_multi(
            api_token, queries, sel_plats, search_type, mode_key, max_qty,
            dt_from.strftime("%Y-%m-%d") if dt_from else None,
            dt_to.strftime("%Y-%m-%d") if dt_to else None,
            search_cb
        )
        status.empty()
        st.session_state[f"{tab_key}_r"] = results
        st.session_state[f"{tab_key}_q"] = queries

    if st.session_state.get(f"{tab_key}_r"):
        results = st.session_state[f"{tab_key}_r"]
        queries_used = st.session_state.get(f"{tab_key}_q", [])
        if results:
            rdf = pd.DataFrame(results)
            st.markdown("---")
            st.success(f"**{len(rdf)} posts** found")
            c1,c2,c3,c4 = st.columns(4)
            with c1: st.metric("Posts", f"{len(rdf):,}")
            with c2: st.metric(f"{label}s", len(queries_used))
            with c3: st.metric("Avg. ER", f"{rdf['engagement_rate'].mean():.2f}%")
            with c4: st.metric("Views", fmt_num(int(rdf["views"].sum())))
            st.markdown("### Results")
            disp = rdf[["query","platform","username","date","caption","likes","comments","shares","views","engagement_rate"]].copy()
            disp.columns = [label,"Platform","Username","Date","Caption","Likes","Comments","Shares","Views","ER (%)"]
            st.dataframe(disp.sort_values("Likes",ascending=False), use_container_width=True, height=400, hide_index=True)
            st.markdown("### Download")
            c1,c2,_ = st.columns([1,1,2])
            safe = search_type[:3]
            with c1:
                st.download_button("Download .xlsx", export_search_to_excel(results, queries_used, search_type),
                    f"{safe}_search.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True, key=f"{tab_key}_dx")
            with c2:
                st.download_button("Download .csv", rdf.to_csv(index=False), f"{safe}_search.csv",
                    "text/csv", use_container_width=True, key=f"{tab_key}_dc")
        else:
            st.markdown("---")
            st.warning(f"No results found. Try different {label.lower()}s.")


# TAB 4: KEYWORD TRACKER
with T_KW:
    search_tab("kw", "keyword", "Keyword", "e.g. skincare routine, glass skin, morning routine", "Search")

# TAB 5: HASHTAG TRACKER
with T_HT:
    search_tab("ht", "hashtag", "Hashtag", "e.g. #CleanBeauty, #SkincareRoutine, #GlassSkin", "Search")
