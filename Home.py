import streamlit as st

st.set_page_config(
    page_title="frndOS — Maleo FCN Tools",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ═══════════════════════════════════════════════════════════════
# AUTH: Email whitelist + shared password
# ═══════════════════════════════════════════════════════════════
def check_auth():
    return st.session_state.get("authenticated", False)


def login_page():
    st.markdown("""<style>
    [data-testid="collapsedControl"] { display: none; }
    .block-container { max-width: 440px; padding-top: 10vh; }
    </style>""", unsafe_allow_html=True)

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
        email = st.text_input("Email", placeholder="yourname@company.com")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        submitted = st.form_submit_button("Login", use_container_width=True, type="primary")

    if submitted:
        try:
            allowed = st.secrets["allowed_emails"]["emails"]
            app_pw = st.secrets["APP_PASSWORD"]
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
            st.session_state["user_email"] = email_clean
            st.rerun()


# ─── Check auth ───
if not check_auth():
    login_page()
    st.stop()


# ═══════════════════════════════════════════════════════════════
# LANDING PAGE (only shows after login)
# ═══════════════════════════════════════════════════════════════

st.markdown("""
<style>
[data-testid="collapsedControl"] { display: none; }
.block-container { max-width: 780px; padding-top: 3rem; }

.tool-card {
    background: #0E0E1C;
    border: 1px solid #1E1E32;
    border-radius: 16px;
    padding: 28px;
    transition: border-color 0.2s;
    height: 100%;
}
.card-label { font-size: 11px; font-weight: 700; letter-spacing: 1.5px; margin-bottom: 8px; }
.card-title { font-size: 20px; font-weight: 700; color: #fff; margin-bottom: 8px; }
.card-desc  { font-size: 13px; color: #6b7280; line-height: 1.6; margin-bottom: 16px; }
.feature    { font-size: 12px; color: #9ca3af; margin-bottom: 5px; }
.status-live    { background:#052e16; color:#4ade80; border:1px solid #166534; padding:3px 10px; border-radius:20px; font-size:10px; font-weight:700; }
.status-preview { background:#1c1405; color:#fbbf24; border:1px solid #92400e; padding:3px 10px; border-radius:20px; font-size:10px; font-weight:700; }
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────────────
st.markdown("""
<div style="display:inline-flex;align-items:center;gap:8px;background:#161625;border:1px solid #1E1E32;
            padding:5px 14px;border-radius:20px;font-size:12px;color:#6b7280;margin-bottom:28px;">
  <div style="width:7px;height:7px;border-radius:50%;background:#4ade80;box-shadow:0 0 6px #4ade80;"></div>
  frndOS · Maleo FCN Internal Tools
</div>
""", unsafe_allow_html=True)

st.markdown("## AI-Powered\n# Marketing Intelligence")
st.markdown("<p style='color:#6b7280;font-size:15px;margin-bottom:32px;'>Two tools, one workflow — from data to pitch deck.</p>",
            unsafe_allow_html=True)

st.info("💡 **Brand Analyzer** uses Apify to pull live data. "
        "**Campaign Pitch Express** is a demo prototype and requires no external credentials.")

# Logged in as
st.caption(f"Logged in as: {st.session_state.get('user_email', '')}")
if st.button("Logout", key="logout_home"):
    st.session_state["authenticated"] = False
    st.session_state["user_email"] = ""
    st.rerun()

st.markdown("---")

# ── Tool Cards ───────────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown("""
    <div class="tool-card">
      <div class="card-label" style="color:#3B82F6;">📊 DATA INTELLIGENCE</div>
      <div class="card-title">Brand Analyzer</div>
      <span class="status-live">● Live Tool</span>
      <p class="card-desc" style="margin-top:12px;">Pull social media performance data across 6 platforms in one click. Powered by Apify + Claude AI analysis.</p>
      <div class="feature">✦ Content Performance (IG, TikTok, X, FB, YouTube, LinkedIn)</div>
      <div class="feature">✦ Comment Scraper — multi-URL, auto-detect platform</div>
      <div class="feature">✦ Keyword & Hashtag Tracker</div>
      <div class="feature">✦ AI Analysis + Excel/CSV export</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("Open Brand Analyzer →", use_container_width=True, type="primary", key="btn_ba"):
        st.switch_page("pages/1_Brand_Analyzer.py")

with col2:
    st.markdown("""
    <div class="tool-card">
      <div class="card-label" style="color:#8B5CF6;">🚀 PITCH AUTOMATION</div>
      <div class="card-title">Campaign Pitch AI Express</div>
      <span class="status-preview">◎ Preview · Demo Mode</span>
      <p class="card-desc" style="margin-top:12px;">End-to-end AI-powered pitching system. From client brief to full pitch deck in under 2 hours, operated by 2 people.</p>
      <div class="feature">✦ 7-Phase pipeline: Brief → Research → Big Idea → KV → KPIs → Deck</div>
      <div class="feature">✦ SC Approval checkpoints at each phase</div>
      <div class="feature">✦ frndOS AI assistant — live chat per phase</div>
      <div class="feature">✦ Output to Lark Docs + Canva deck</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("Open Pitch Express →", use_container_width=True, key="btn_pitch"):
        st.switch_page("pages/2_Campaign_Pitch_Express.py")

st.markdown("---")
st.markdown("<p style='text-align:center;color:#374151;font-size:12px;'>Maleo FCN · frndOS · Internal use only · Built April 2026</p>",
            unsafe_allow_html=True)
