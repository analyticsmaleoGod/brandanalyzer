import streamlit as st

st.set_page_config(
    page_title="frndOS — Maleo FCN Tools",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Hide sidebar + Streamlit multipage nav completely ─────────────
st.markdown("""
<style>
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stSidebar"]        { display: none !important; }
[data-testid="stSidebarNav"]     { display: none !important; }
.block-container { max-width: 820px; padding-top: 3rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="display:inline-flex;align-items:center;gap:8px;background:#161625;border:1px solid #1E1E32;
            padding:5px 14px;border-radius:20px;font-size:12px;color:#6b7280;margin-bottom:28px;">
  <div style="width:7px;height:7px;border-radius:50%;background:#4ade80;box-shadow:0 0 6px #4ade80;"></div>
  frndOS · Maleo FCN Internal Tools
</div>
""", unsafe_allow_html=True)

st.markdown("<p style='font-size:32px;font-weight:800;color:#111827;margin:0;line-height:1.2;'>AI-Powered</p>", unsafe_allow_html=True)
st.markdown("<p style='font-size:32px;font-weight:800;color:#3B82F6;margin:0 0 10px;line-height:1.2;'>Marketing Intelligence</p>", unsafe_allow_html=True)
st.markdown("<p style='color:#6b7280;font-size:15px;margin-bottom:32px;'>Two tools, one workflow — from data to pitch deck.</p>", unsafe_allow_html=True)

col_info, col_logout = st.columns([4, 1])
with col_info:
    st.caption(f"Logged in as: **{st.session_state.get('user_email', '')}**")
with col_logout:
    if st.button("Logout", key="logout_home"):
        st.session_state["authenticated"] = False
        st.session_state["user_email"]    = ""
        st.rerun()

st.markdown("---")

col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown("""
    <div style="background:#0E0E1C;border:1px solid #1E1E32;border-radius:16px;padding:28px;height:100%;">
      <div style="font-size:10px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;color:#3B82F6;margin-bottom:8px;">📊 Data Intelligence</div>
      <div style="font-size:20px;font-weight:700;color:#fff;margin-bottom:10px;">Brand Analyzer</div>
      <div style="display:inline-block;background:#052e16;color:#4ade80;border:1px solid #166534;padding:3px 12px;border-radius:20px;font-size:10px;font-weight:700;margin-bottom:14px;">● Live Tool</div>
      <div style="font-size:13px;color:#9ca3af;line-height:1.65;margin-bottom:14px;">Pull social media performance data across 6 platforms in one click. Powered by Apify + Claude AI analysis.</div>
      <div style="font-size:12px;color:#6b7280;margin-bottom:5px;">✦ Content Performance (IG, TikTok, X, FB, YouTube, LinkedIn)</div>
      <div style="font-size:12px;color:#6b7280;margin-bottom:5px;">✦ Comment Scraper — multi-URL, auto-detect platform</div>
      <div style="font-size:12px;color:#6b7280;margin-bottom:5px;">✦ Keyword & Hashtag Tracker</div>
      <div style="font-size:12px;color:#6b7280;margin-bottom:20px;">✦ AI Analysis + Excel/CSV export</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Brand Analyzer →", use_container_width=True, type="primary", key="btn_ba"):
        st.switch_page("pages/1_Brand_Analyzer.py")

with col2:
    st.markdown("""
    <div style="background:#0E0E1C;border:1px solid #1E1E32;border-radius:16px;padding:28px;height:100%;">
      <div style="font-size:10px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;color:#8B5CF6;margin-bottom:8px;">🚀 Pitch Automation</div>
      <div style="font-size:20px;font-weight:700;color:#fff;margin-bottom:10px;">Campaign Pitch AI Express</div>
      <div style="display:inline-block;background:#1c1405;color:#fbbf24;border:1px solid #92400e;padding:3px 12px;border-radius:20px;font-size:10px;font-weight:700;margin-bottom:14px;">◎ Preview · Demo Mode</div>
      <div style="font-size:13px;color:#9ca3af;line-height:1.65;margin-bottom:14px;">End-to-end AI-powered pitching system. From client brief to full pitch deck in under 2 hours, operated by 2 people.</div>
      <div style="font-size:12px;color:#6b7280;margin-bottom:5px;">✦ 7-Phase pipeline: Brief → Research → Big Idea → KV → KPIs → Deck</div>
      <div style="font-size:12px;color:#6b7280;margin-bottom:5px;">✦ SC Approval checkpoints at each phase</div>
      <div style="font-size:12px;color:#6b7280;margin-bottom:5px;">✦ frndOS AI assistant — live chat per phase</div>
      <div style="font-size:12px;color:#6b7280;margin-bottom:20px;">✦ Output to Lark Docs + Canva deck</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Pitch Express →", use_container_width=True, key="btn_pitch"):
        st.switch_page("pages/2_Campaign_Pitch_Express.py")


st.markdown("---")
st.markdown("<p style='text-align:center;color:#374151;font-size:12px;'>Maleo FCN · frndOS · Internal use only · Built April 2026</p>", unsafe_allow_html=True)
