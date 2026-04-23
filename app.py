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
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# AUTH
# ═══════════════════════════════════════════════════════════════
def check_auth():
    return st.session_state.get("authenticated", False)


def login_page():
    st.markdown("""
    <style>.block-container { max-width: 440px; padding-top: 10vh; }</style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="display:inline-flex;align-items:center;gap:8px;background:#161625;border:1px solid #1E1E32;
                padding:5px 14px;border-radius:20px;font-size:12px;color:#6b7280;margin-bottom:20px;">
      <div style="width:7px;height:7px;border-radius:50%;background:#4ade80;box-shadow:0 0 6px #4ade80;"></div>
      frndOS · Maleo FCN Internal Tools
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 🧠 frndOS")
    st.markdown("Login to access Marketing Intelligence tools.")
    st.markdown("")

    with st.form("login_form"):
        email    = st.text_input("Email", placeholder="yourname@company.com")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        submitted = st.form_submit_button("Login", use_container_width=True, type="primary")

    if submitted:
        try:
            allowed = st.secrets["allowed_emails"]["emails"]
            app_pw  = st.secrets["APP_PASSWORD"]
        except Exception:
            st.error("App not configured. Contact admin.")
            return
        email_clean = email.strip().lower()
        if email_clean not in [e.lower() for e in allowed]:
            st.error("Email not authorized. Contact admin for access.")
        elif password != app_pw:
            st.error("Wrong password.")
        else:
            st.session_state["authenticated"] = True
            st.session_state["user_email"]    = email_clean
            st.rerun()


# ── Auth check ───────────────────────────────────────────────────
if not check_auth():
    login_page()
    st.stop()


# ═══════════════════════════════════════════════════════════════
# LANDING PAGE — after login
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
.block-container { max-width: 820px; padding-top: 3rem; }
/* Card buttons — entire card is the clickable button */
div[data-testid="stButton"] > button {
    background: #0E0E1C !important;
    border: 1px solid #1E1E32 !important;
    border-radius: 16px !important;
    padding: 24px !important;
    width: 100% !important;
    height: auto !important;
    min-height: 320px !important;
    text-align: left !important;
    white-space: pre-wrap !important;
    line-height: 1.7 !important;
    color: #e5e7eb !important;
    font-size: 13px !important;
    cursor: pointer !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
div[data-testid="stButton"] > button:hover {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 1px #3B82F6 !important;
    background: #0E0E1C !important;
    color: #fff !important;
}

/* Logout button override */
div[data-testid="stButton"]:has(button[kind="secondary"]) > button {
    min-height: unset !important;
    padding: 8px 16px !important;
    font-size: 13px !important;
    white-space: nowrap !important;
    background: transparent !important;
    border: 1px solid #e5e7eb !important;
    color: #374151 !important;
}
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
    if st.button("""📊 DATA INTELLIGENCE

Brand Analyzer

● Live Tool

Pull social media performance data across 6 platforms in one click. Powered by Apify + Claude AI analysis.

✦ Content Performance (IG, TikTok, X, FB, YouTube, LinkedIn)
✦ Comment Scraper — multi-URL, auto-detect platform
✦ Keyword & Hashtag Tracker
✦ AI Analysis + Excel/CSV export""", use_container_width=True, key="btn_ba"):
        st.switch_page("pages/1_Brand_Analyzer.py")

with col2:
    if st.button("""🚀 PITCH AUTOMATION

Campaign Pitch AI Express

◎ Preview · Demo Mode

End-to-end AI-powered pitching system. From client brief to full pitch deck in under 2 hours, operated by 2 people.

✦ 7-Phase pipeline: Brief → Research → Big Idea → KV → KPIs → Deck
✦ SC Approval checkpoints at each phase
✦ frndOS AI assistant — live chat per phase
✦ Output to Lark Docs + Canva deck""", use_container_width=True, key="btn_pitch"):
        st.switch_page("pages/2_Campaign_Pitch_Express.py")

st.markdown("---")
st.markdown("<p style='text-align:center;color:#374151;font-size:12px;'>Maleo FCN · frndOS · Internal use only · Built April 2026</p>", unsafe_allow_html=True)
