import streamlit as st

st.set_page_config(
    page_title="frndOS — Maleo FCN Tools",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Hide sidebar completely ───────────────────────────────────────
st.markdown("""
<style>
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stSidebar"]        { display: none !important; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# AUTH
# ═══════════════════════════════════════════════════════════════
def check_auth():
    return st.session_state.get("authenticated", False)


def login_page():
    st.markdown("""
    <style>
    .block-container { max-width: 440px; padding-top: 10vh; }
    </style>
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
# LANDING PAGE — shown after login
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
.block-container { max-width: 820px; padding-top: 3rem; }

.tool-card {
    background: #0E0E1C;
    border: 1px solid #1E1E32;
    border-radius: 16px;
    padding: 28px 28px 24px;
    height: 100%;
}
.card-icon-wrap {
    width: 52px; height: 52px; border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 24px; margin-bottom: 16px;
}
.card-eyebrow {
    font-size: 10px; font-weight: 700; letter-spacing: 1.8px;
    text-transform: uppercase; margin-bottom: 6px;
}
.card-title { font-size: 20px; font-weight: 700; color: #fff; margin-bottom: 10px; }
.card-desc  { font-size: 13px; color: #6b7280; line-height: 1.65; margin-bottom: 16px; }
.card-feature { font-size: 12px; color: #9ca3af; margin-bottom: 5px; line-height: 1.5; }
.badge-live {
    display:inline-block;
    background:#052e16; color:#4ade80; border:1px solid #166534;
    padding:3px 12px; border-radius:20px; font-size:10px; font-weight:700;
    margin-bottom:14px;
}
.badge-preview {
    display:inline-block;
    background:#1c1405; color:#fbbf24; border:1px solid #92400e;
    padding:3px 12px; border-radius:20px; font-size:10px; font-weight:700;
    margin-bottom:14px;
}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────
st.markdown("""
<div style="display:inline-flex;align-items:center;gap:8px;background:#161625;border:1px solid #1E1E32;
            padding:5px 14px;border-radius:20px;font-size:12px;color:#6b7280;margin-bottom:28px;">
  <div style="width:7px;height:7px;border-radius:50%;background:#4ade80;box-shadow:0 0 6px #4ade80;"></div>
  frndOS · Maleo FCN Internal Tools
</div>
""", unsafe_allow_html=True)

st.markdown("<p style='font-size:32px;font-weight:800;color:#fff;margin:0;line-height:1.2;'>AI-Powered</p>", unsafe_allow_html=True)
st.markdown("<p style='font-size:32px;font-weight:800;color:#3B82F6;margin:0 0 10px;line-height:1.2;'>Marketing Intelligence</p>", unsafe_allow_html=True)
st.markdown("<p style='color:#6b7280;font-size:15px;margin-bottom:32px;'>Two tools, one workflow — from data to pitch deck.</p>", unsafe_allow_html=True)

# ── Logged in bar ────────────────────────────────────────────────
col_info, col_logout = st.columns([4, 1])
with col_info:
    st.caption(f"Logged in as: **{st.session_state.get('user_email', '')}**")
with col_logout:
    if st.button("Logout", key="logout_home"):
        st.session_state["authenticated"] = False
        st.session_state["user_email"]    = ""
        st.rerun()

st.markdown("---")

# ── Tool Cards ────────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown("""
    <div class="tool-card">
      <div class="card-icon-wrap" style="background:#0d1b3e;">📊</div>
      <div class="card-eyebrow" style="color:#3B82F6;">Data Intelligence</div>
      <div class="card-title">Brand Analyzer</div>
      <div class="badge-live">● Live Tool</div>
      <div class="card-desc">Pull social media performance data across 6 platforms in one click. Powered by Apify + Claude AI analysis.</div>
      <div class="card-feature">✦ Content Performance (IG, TikTok, X, FB, YouTube, LinkedIn)</div>
      <div class="card-feature">✦ Comment Scraper — multi-URL, auto-detect platform</div>
      <div class="card-feature">✦ Keyword & Hashtag Tracker</div>
      <div class="card-feature">✦ AI Analysis + Excel/CSV export</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("Open Brand Analyzer →", use_container_width=True, type="primary", key="btn_ba"):
        st.switch_page("pages/1_Brand_Analyzer.py")

with col2:
    st.markdown("""
    <div class="tool-card">
      <div class="card-icon-wrap" style="background:#1e0a3e;">🚀</div>
      <div class="card-eyebrow" style="color:#8B5CF6;">Pitch Automation</div>
      <div class="card-title">Campaign Pitch AI Express</div>
      <div class="badge-preview">◎ Preview · Demo Mode</div>
      <div class="card-desc">End-to-end AI-powered pitching system. From client brief to full pitch deck in under 2 hours, operated by 2 people.</div>
      <div class="card-feature">✦ 7-Phase pipeline: Brief → Research → Big Idea → KV → KPIs → Deck</div>
      <div class="card-feature">✦ SC Approval checkpoints at each phase</div>
      <div class="card-feature">✦ frndOS AI assistant — live chat per phase</div>
      <div class="card-feature">✦ Output to Lark Docs + Canva deck</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("Open Pitch Express →", use_container_width=True, key="btn_pitch"):
        st.switch_page("pages/2_Campaign_Pitch_Express.py")

st.markdown("---")
st.markdown("<p style='text-align:center;color:#374151;font-size:12px;'>Maleo FCN · frndOS · Internal use only · Built April 2026</p>",
            unsafe_allow_html=True)
