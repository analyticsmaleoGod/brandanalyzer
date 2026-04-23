import streamlit as st
import time

st.set_page_config(
    page_title="Campaign Pitch AI Express — frndOS",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# AUTH GUARD
# ─────────────────────────────────────────────
if not st.session_state.get("authenticated", False):
    st.switch_page("Home.py")

# ─────────────────────────────────────────────
# GLOBAL STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base ── */
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stSidebar"]        { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stMain"] > div { padding: 0 !important; }

/* ── Layout shell ── */
.pitch-shell {
    display: grid;
    grid-template-columns: 220px 1fr 300px;
    grid-template-rows: 56px 1fr;
    height: 100vh;
    background: #08080f;
    font-family: 'Inter', system-ui, sans-serif;
    overflow: hidden;
}

/* ── Top bar ── */
.topbar {
    grid-column: 1 / -1;
    background: #0d0d1a;
    border-bottom: 1px solid #1a1a2e;
    display: flex;
    align-items: center;
    padding: 0 20px;
    gap: 16px;
    height: 56px;
}
.topbar-logo {
    font-size: 13px;
    font-weight: 700;
    color: #fff;
    letter-spacing: 0.5px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.topbar-logo-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #4ade80;
    box-shadow: 0 0 6px #4ade80;
}
.topbar-sep { width: 1px; height: 20px; background: #1a1a2e; }
.topbar-pitch-name { font-size: 13px; color: #fff; font-weight: 600; }
.topbar-campaign    { font-size: 12px; color: #4b5563; }
.topbar-badge {
    margin-left: auto;
    font-size: 10px; font-weight: 700; letter-spacing: 1.2px;
    padding: 3px 10px; border-radius: 20px;
    background: #1a1a2e; color: #6b7280; border: 1px solid #1a1a2e;
}
.topbar-people {
    font-size: 11px; color: #6b7280;
    display: flex; gap: 14px;
}
.topbar-people span b { color: #e5e7eb; font-weight: 600; }

/* ── Left nav ── */
.leftnav {
    background: #0d0d1a;
    border-right: 1px solid #1a1a2e;
    padding: 16px 0;
    overflow-y: auto;
}
.leftnav-section {
    font-size: 9px; font-weight: 700; letter-spacing: 1.8px;
    color: #374151; padding: 0 16px; margin: 0 0 8px;
    text-transform: uppercase;
}
.nav-item {
    display: flex; align-items: center; gap: 10px;
    padding: 8px 16px; cursor: pointer;
    font-size: 12px; color: #6b7280;
    border-left: 2px solid transparent;
    transition: all 0.15s;
}
.nav-item:hover  { background: #111127; color: #d1d5db; }
.nav-item.active { background: #111127; color: #fff; border-left-color: var(--phase-color); }
.nav-item.done   { color: #4ade80; }
.nav-item.pending{ color: #374151; cursor: not-allowed; }
.nav-dot {
    width: 8px; height: 8px; border-radius: 50%;
    flex-shrink: 0;
}
.nav-label { font-size: 12px; line-height: 1.3; }
.nav-check { margin-left: auto; font-size: 10px; color: #4ade80; }

.nav-divider { border: none; border-top: 1px solid #1a1a2e; margin: 12px 0; }

.output-link {
    display: flex; align-items: center; gap: 8px;
    padding: 7px 16px; font-size: 11px; color: #4b5563;
}
.output-link.synced { color: #4ade80; }
.output-link-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: currentColor; flex-shrink: 0;
}

/* ── Main content ── */
.main-content {
    overflow-y: auto;
    padding: 28px 32px;
    background: #08080f;
}

/* ── Phase header ── */
.phase-header {
    display: flex; align-items: center; gap: 12px;
    margin-bottom: 6px;
}
.phase-icon { font-size: 18px; }
.phase-title { font-size: 22px; font-weight: 700; color: #fff; }
.phase-status-badge {
    font-size: 10px; font-weight: 700; letter-spacing: 1px;
    padding: 3px 10px; border-radius: 20px;
}
.badge-active  { background: #1a1a2e; color: #60a5fa; border: 1px solid #1e3a5f; }
.badge-done    { background: #052e16; color: #4ade80; border: 1px solid #166534; }
.badge-pending { background: #111; color: #4b5563; border: 1px solid #1f2937; }
.phase-desc { font-size: 13px; color: #4b5563; margin-bottom: 24px; }

/* ── Pipeline strip ── */
.pipeline-strip {
    display: flex; gap: 4px; margin-bottom: 28px;
    align-items: center;
}
.pipe-step {
    display: flex; align-items: center; gap: 6px;
    font-size: 10px; font-weight: 600; letter-spacing: 0.5px;
    padding: 5px 10px; border-radius: 20px;
    white-space: nowrap;
}
.pipe-step.done    { background: #052e16; color: #4ade80; border: 1px solid #166534; }
.pipe-step.active  { background: #0d1b3e; color: #60a5fa; border: 1px solid #1d4ed8; }
.pipe-step.pending { background: #0d0d1a; color: #374151; border: 1px solid #1a1a2e; }
.pipe-arrow { color: #1f2937; font-size: 10px; }

/* ── Output cards ── */
.out-card {
    background: #0d0d1a;
    border: 1px solid #1a1a2e;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.out-card-title { font-size: 15px; font-weight: 700; color: #fff; margin-bottom: 2px; }
.out-card-sub   { font-size: 11px; color: #4b5563; margin-bottom: 16px; }

.table-row {
    display: grid; grid-template-columns: 160px 1fr;
    gap: 8px 16px; padding: 10px 0;
    border-bottom: 1px solid #1a1a2e;
    align-items: start;
}
.table-row:last-child { border-bottom: none; }
.table-label { font-size: 12px; color: #4b5563; padding-top: 1px; }
.table-value { font-size: 13px; color: #e5e7eb; line-height: 1.5; }

.signal-card {
    background: #111127;
    border: 1px solid #1a1a2e;
    border-radius: 8px;
    padding: 14px 16px;
    margin-bottom: 10px;
}
.signal-tag  { font-size: 10px; font-weight: 700; letter-spacing: 1px; color: #6b7280; margin-bottom: 4px; }
.signal-text { font-size: 13px; color: #d1d5db; line-height: 1.5; }

.territory-card {
    background: #111127;
    border: 1px solid #1a1a2e;
    border-radius: 10px;
    padding: 18px 20px;
    margin-bottom: 12px;
}
.territory-num   { font-size: 10px; font-weight: 700; letter-spacing: 2px; color: #4b5563; margin-bottom: 6px; }
.territory-name  { font-size: 16px; font-weight: 700; color: #fff; margin-bottom: 10px; }
.territory-row   { display: flex; gap: 8px; margin-bottom: 6px; align-items: flex-start; }
.territory-key   { font-size: 11px; color: #6b7280; width: 70px; flex-shrink: 0; padding-top: 1px; }
.territory-val   { font-size: 13px; color: #d1d5db; line-height: 1.4; }
.territory-why   {
    background: #0d1b3e; border: 1px solid #1d4ed8;
    border-radius: 6px; padding: 8px 12px;
    font-size: 12px; color: #93c5fd; margin-top: 10px;
}

.pillar-card {
    background: #111127; border: 1px solid #1a1a2e;
    border-radius: 8px; padding: 14px 16px;
    text-align: center;
}
.pillar-name { font-size: 11px; font-weight: 700; letter-spacing: 1px; color: #6b7280; margin-bottom: 4px; text-transform: uppercase; }
.pillar-pct  { font-size: 28px; font-weight: 800; color: #fff; margin-bottom: 4px; }
.pillar-desc { font-size: 11px; color: #4b5563; line-height: 1.4; }

.timeline-item {
    display: grid; grid-template-columns: 100px 90px 1fr;
    gap: 12px; padding: 12px 0;
    border-bottom: 1px solid #1a1a2e;
    align-items: center;
}
.timeline-item:last-child { border-bottom: none; }
.timeline-weeks { font-size: 12px; font-weight: 700; color: #fff; }
.timeline-phase { font-size: 11px; font-weight: 700; letter-spacing: 0.5px; color: #6b7280; text-transform: uppercase; }
.timeline-desc  { font-size: 12px; color: #9ca3af; line-height: 1.4; }

.kv-row {
    display: grid; grid-template-columns: 160px 1fr;
    gap: 8px 16px; padding: 12px 0;
    border-bottom: 1px solid #1a1a2e;
}
.kv-row:last-child { border-bottom: none; }
.kv-label { font-size: 12px; font-weight: 600; color: #6b7280; }
.kv-val   { font-size: 13px; color: #e5e7eb; line-height: 1.5; }

.slide-item {
    background: #111127; border: 1px solid #1a1a2e;
    border-radius: 6px; padding: 9px 14px;
    font-size: 12px; color: #9ca3af;
    margin-bottom: 6px;
}

/* ── Approval panel ── */
.approval-panel {
    background: #0d0d1a;
    border: 1px solid #1a1a2e;
    border-radius: 12px;
    padding: 20px 24px;
    margin-top: 20px;
}
.approval-title { font-size: 13px; font-weight: 700; color: #fff; margin-bottom: 14px; letter-spacing: 0.3px; }

/* ── Lark sync badge ── */
.lark-synced {
    display: inline-flex; align-items: center; gap: 6px;
    background: #052e16; border: 1px solid #166534;
    border-radius: 6px; padding: 6px 12px;
    font-size: 12px; color: #4ade80; font-weight: 600;
    margin-top: 16px;
}

/* ── Right chat panel ── */
.chat-panel {
    background: #0d0d1a;
    border-left: 1px solid #1a1a2e;
    display: flex; flex-direction: column;
    overflow: hidden;
}
.chat-header {
    padding: 14px 16px 12px;
    border-bottom: 1px solid #1a1a2e;
    display: flex; align-items: center; gap: 8px;
    flex-shrink: 0;
}
.chat-header-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: #4ade80; box-shadow: 0 0 6px #4ade80;
}
.chat-header-title { font-size: 13px; font-weight: 700; color: #fff; }
.chat-header-sub   { font-size: 10px; color: #4b5563; margin-left: auto; }
.chat-messages     { flex: 1; overflow-y: auto; padding: 14px 14px 0; }

.chat-bubble-ai, .chat-bubble-user {
    border-radius: 10px; padding: 9px 12px;
    font-size: 12px; line-height: 1.5;
    margin-bottom: 10px; max-width: 90%;
}
.chat-bubble-ai {
    background: #111127; color: #d1d5db;
    border: 1px solid #1a1a2e;
}
.chat-bubble-user {
    background: #0d1b3e; color: #93c5fd;
    border: 1px solid #1d4ed8;
    margin-left: auto;
}
.chat-sender { font-size: 9px; font-weight: 700; letter-spacing: 1px; color: #4b5563; margin-bottom: 3px; text-transform: uppercase; }
.chat-input-area {
    padding: 12px 14px;
    border-top: 1px solid #1a1a2e;
    flex-shrink: 0;
}

/* ── Run button ── */
.stButton > button {
    background: #1d4ed8 !important;
    border: none !important;
    border-radius: 8px !important;
    color: #fff !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 10px 20px !important;
    transition: background 0.2s !important;
}
.stButton > button:hover { background: #2563eb !important; }
.stButton > button[kind="secondary"] {
    background: #111127 !important;
    border: 1px solid #1a1a2e !important;
    color: #9ca3af !important;
}
.stButton > button[kind="secondary"]:hover {
    background: #1a1a2e !important;
    color: #fff !important;
}

/* ── Locked state ── */
.locked-state {
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; padding: 60px 20px; text-align: center;
    color: #374151;
}
.locked-icon  { font-size: 36px; margin-bottom: 12px; }
.locked-title { font-size: 15px; font-weight: 700; color: #4b5563; margin-bottom: 6px; }
.locked-sub   { font-size: 12px; color: #374151; }

/* ── Warning / info ── */
.flag-box {
    background: #1c1405; border: 1px solid #92400e;
    border-radius: 8px; padding: 12px 16px; margin-top: 12px;
}
.flag-title { font-size: 11px; font-weight: 700; color: #fbbf24; margin-bottom: 6px; letter-spacing: 0.5px; }
.flag-item  { font-size: 12px; color: #d97706; margin-bottom: 3px; line-height: 1.5; }

.info-box {
    background: #0d1b3e; border: 1px solid #1d4ed8;
    border-radius: 8px; padding: 12px 16px; margin-bottom: 16px;
    font-size: 12px; color: #93c5fd; line-height: 1.5;
}

/* ── Checklist ── */
div[data-testid="stCheckbox"] label {
    font-size: 13px !important;
    color: #d1d5db !important;
}

/* ── Dataframe ── */
.stDataFrame { border-radius: 8px; overflow: hidden; }

/* Hide streamlit branding */
#MainMenu { display: none; }
footer     { display: none; }
header     { display: none; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DEMO DATA
# ─────────────────────────────────────────────

CLIENT   = "Lumia Skincare"
CAMPAIGN = "Real Radiance — Q3 2026"
SC       = "Ryan"
CE       = "Lukman"

PHASES = [
    {
        "id": "brief", "name": "Brief Decoder", "icon": "🔵",
        "color": "#3B82F6", "desc": "Reads & decodes client brief", "btn": "Decode Brief",
        "chat": [
            ("ai", "Brief uploaded. Analyzing document structure and extracting objectives..."),
            ("ai", "Found 3 unclear points in the brief. Auto-filling based on past pitches for Lumia."),
            ("ai", "Done. Business Brief completed and saved to Lark Docs. Ready for Research phase?"),
        ],
        "output_title": "Business Brief — Lumia Skincare",
        "output_sub":   "Real Radiance Campaign · Q3 2026",
        "output": {
            "type": "table",
            "rows": [
                ("Client",             "Lumia Skincare"),
                ("Product",            "Lumia Hydra-Glow Serum — new product launch"),
                ("Campaign Period",    "July – September 2026 (12 weeks)"),
                ("Business Objective", "Drive awareness and first-trial among millennial women in urban Indonesia"),
                ("Target Audience",    "Primary: Women 22–32, urban, skincare-aware · Secondary: Beginners seeking entry product"),
                ("Platforms",         "Instagram, TikTok"),
                ("Budget",            "Rp 300,000,000"),
                ("Objective Type",    "Awareness (Primary) + Consideration (Secondary)"),
            ],
            "flags": [
                "Campaign duration was unclear → inferred as Q3 (12 weeks)",
                "KPI targets not specified → to be generated in Analytics phase",
                "Distribution channel not mentioned → assumed online-only",
            ],
        },
    },
    {
        "id": "research", "name": "Research", "icon": "🟢",
        "color": "#10B981", "desc": "Market signals & competitor analysis", "btn": "Run Research",
        "chat": [
            ("ai", "Pulling market signals for skincare category in Indonesia..."),
            ("ai", "Found 4 market signals and 2 competitor movements relevant to this brief."),
            ("ai", "Strategy Findings saved to Lark Docs under Research section. Ready for Big Idea?"),
        ],
        "output_title": "Strategy Findings",
        "output_sub":   "Skincare Category · Indonesia · Q3 2026",
        "output": {
            "type": "signals",
            "items": [
                ("📈", "TREND",      '"Glass skin" & "dewy aesthetic" searches up 34% MoM on TikTok Indonesia'),
                ("👥", "AUDIENCE",   '71% of skincare purchase decisions influenced by TikTok "before/after" content'),
                ("🔥", "CONTENT",    "Serum-focused routines generate 2.3× higher saves vs. other skincare formats"),
                ("⚡", "COMPETITOR", 'Wardah "Flawless" line drove 89M TikTok views in 6 weeks via heavy UGC activation'),
            ],
        },
    },
    {
        "id": "bigidea", "name": "Big Idea", "icon": "🟡",
        "color": "#F59E0B", "desc": "3 campaign territories", "btn": "Generate Ideas",
        "chat": [
            ("ai", "Generating 3 big idea territories grounded in brief and research findings..."),
            ("ai", "Done. 3 territories ready for SC review. Select one territory to proceed."),
        ],
        "output_title": "Big Idea Territories",
        "output_sub":   "SC to select one territory to proceed",
        "output": {
            "type": "territories",
            "items": [
                {
                    "num": "01", "name": "Glow Like You Mean It",
                    "theme": "Self-confidence through real skin",
                    "message": "You don't need filters. You need Lumia.",
                    "tone": "Empowering, warm, authentic",
                    "why": "Taps into the anti-filter movement gaining strong traction on TikTok",
                },
                {
                    "num": "02", "name": "The Hydra Formula",
                    "theme": "Science-led efficacy storytelling",
                    "message": "72-hour hydration, proven on real skin.",
                    "tone": "Credible, clean, modern",
                    "why": "Differentiates from emotion-led competitors, builds ingredient trust",
                },
                {
                    "num": "03", "name": "Your Glow, Your Rules",
                    "theme": "Personalization & self-expression",
                    "message": "Every glow is different. Lumia unlocks yours.",
                    "tone": "Playful, inclusive, Gen-Z friendly",
                    "why": "Broad appeal, high shareability, natural fit for UGC challenge activation",
                },
            ],
        },
    },
    {
        "id": "rollout", "name": "Campaign Rollout", "icon": "🟣",
        "color": "#8B5CF6", "desc": "Content pillars, platform strategy & timeline", "btn": "Build Rollout",
        "chat": [
            ("ai", 'Expanding "Glow Like You Mean It" into full campaign rollout...'),
            ("ai", "Content pillars, platform strategy, and 12-week timeline generated. Saved to Lark Docs."),
        ],
        "output_title": "Campaign Rollout — Glow Like You Mean It",
        "output_sub":   "12-week execution plan · Instagram + TikTok",
        "output": {
            "type": "rollout",
            "pillars":  [("Education", "40%", "Ingredient deep-dives, routine guides, expert tips"),
                         ("Transformation", "35%", "Before/after, skin journey, real results"),
                         ("Community", "25%", "UGC reposts, challenges, creator collabs")],
            "platforms":[("Instagram", "Reels (hero), Carousels (edu), Stories (polls + CTAs)"),
                         ("TikTok",    "Tutorials, Before/After, UGC challenge #GlowLikeYouMeanIt")],
            "timeline": [("Wk 1–3",  "Teaser",  "Build intrigue, seed UGC creators, tease product"),
                         ("Wk 4–8",  "Launch",  "Hero content push, paid amplification, creator activations"),
                         ("Wk 9–12", "Sustain", "Community UGC, engagement nurture, retargeting")],
        },
    },
    {
        "id": "kv", "name": "KV Generator", "icon": "🟠",
        "color": "#F97316", "desc": "Visual direction & moodboard", "btn": "Generate KV Direction",
        "chat": [
            ("ai", "Generating key visual direction based on campaign brief and big idea territory..."),
            ("ai", "KV direction and moodboard references ready. CE to review and refine before production."),
        ],
        "output_title": "KV Direction — Glow Like You Mean It",
        "output_sub":   "Visual identity for Real Radiance campaign",
        "output": {
            "type": "kv",
            "specs": [
                ("Color Palette",    "Warm ivory, soft gold, pearl white — avoid stark whites and cool tones"),
                ("Aesthetic",        "Dewy close-ups, golden hour lighting, natural skin textures"),
                ("Talent Direction", "Real-looking skin, minimal makeup, relatable faces — not model-perfect"),
                ("Typography Feel",  "Clean, light weight, modern humanist sans-serif"),
                ("Overall Mood",     "Warm confidence — soft luxury, not aspirational distance"),
            ],
        },
    },
    {
        "id": "analytics", "name": "Analytics & KPIs", "icon": "🔷",
        "color": "#06B6D4", "desc": "Success criteria & KPI framework", "btn": "Generate KPI Framework",
        "chat": [
            ("ai", "Reading approved brief... Campaign objective: Awareness (Primary) + Consideration (Secondary)."),
            ("ai", "No historical Lumia data found — generating benchmarked estimates for skincare category."),
            ("ai", "KPI framework with Realistic vs Breakthrough targets generated. SC to review and finalize."),
        ],
        "output_title": "Success Criteria — Real Radiance Campaign",
        "output_sub":   "Objective: Awareness + Consideration · Platforms: IG + TikTok · Skincare category benchmarks",
        "output": {
            "type": "analytics",
            "note": "No historical data for Lumia — all targets are benchmarked estimates from skincare category norms",
            "kpis": [
                ("Awareness",     "TikTok",    "Total Views",     "5,000,000",  "12,000,000"),
                ("Awareness",     "TikTok",    "Reach",           "2,500,000",  "6,000,000"),
                ("Awareness",     "Instagram", "Impressions",     "3,000,000",  "7,000,000"),
                ("Awareness",     "Instagram", "Follower Growth", "+2,000",     "+5,000"),
                ("Consideration", "TikTok",    "Engagement Rate", "4.5%",       "7.0%"),
                ("Consideration", "TikTok",    "Video Saves",     "15,000",     "40,000"),
                ("Consideration", "Instagram", "Engagement Rate", "3.2%",       "5.5%"),
                ("Consideration", "Instagram", "Story Replies",   "500",        "1,500"),
                ("Consideration", "All",       "UGC Volume",      "200 posts",  "600 posts"),
            ],
        },
    },
    {
        "id": "deck", "name": "Deck Builder", "icon": "🟩",
        "color": "#22C55E", "desc": "Pushes to Canva deck template", "btn": "Build Deck",
        "chat": [
            ("ai", "Reading all approved outputs from Lark Docs..."),
            ("ai", "Assembling 14-slide pitch deck in Canva template..."),
            ("ai", "✅ Deck assembled and pushed to Canva. Link saved to Lark Docs. Ready for final approval."),
        ],
        "output_title": "Pitch Deck — Real Radiance",
        "output_sub":   "14 slides assembled · Awaiting final approval",
        "output": {
            "type": "deck",
            "slides": [
                "01 — Cover & Campaign Title",
                "02 — Executive Summary",
                "03 — Market Opportunity",
                "04 — Business Brief",
                "05 — Research Insights",
                '06 — Big Idea: "Glow Like You Mean It"',
                "07 — Key Message & Tone",
                "08 — Campaign Rollout Overview",
                "09 — Platform Strategy",
                "10 — Content Direction & Examples",
                "11 — KV Direction & Moodboard",
                "12 — Success Criteria & KPIs",
                "13 — Campaign Timeline",
                "14 — Investment & Next Steps",
            ],
        },
    },
]

CHECKLISTS = {
    "brief":     ["Objective clearly stated", "Target audience defined", "Campaign period confirmed", "All unclear points resolved by SC"],
    "research":  ["Market signals relevant to brief", "Competitor activity noted", "Audience insights are actionable", "Findings align with objective"],
    "bigidea":   ["Territory 01 reviewed", "Territory 02 reviewed", "Territory 03 reviewed", "One territory selected to proceed"],
    "rollout":   ["Content pillars are aligned", "Platform strategy makes sense", "12-week timeline is feasible", "CE can execute the deliverables"],
    "kv":        ["Visual direction fits brand", "Moodboard references are adequate", "CE aligned on direction", "Ready for production"],
    "analytics": ["Objective type correctly identified", "Platforms match brief scope", "Realistic targets achievable", "Breakthrough targets inspiring but credible"],
    "deck":      ["All phases reflected in deck", "Slide flow tells a coherent story", "KPIs and timeline are correct", "Ready for client delivery"],
}

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
def init_state():
    if "pitch_phase"     not in st.session_state: st.session_state.pitch_phase     = 0
    if "pitch_statuses"  not in st.session_state: st.session_state.pitch_statuses  = ["active"] + ["pending"] * (len(PHASES) - 1)
    if "pitch_outputs"   not in st.session_state: st.session_state.pitch_outputs   = {}
    if "pitch_chat"      not in st.session_state: st.session_state.pitch_chat      = [("ai", "Welcome to Campaign Pitch AI Express. Brief Decoder is ready — upload the client brief to begin.")]
    if "pitch_approval"  not in st.session_state: st.session_state.pitch_approval  = {}
    if "pitch_checklist" not in st.session_state: st.session_state.pitch_checklist = {}

init_state()

# ─────────────────────────────────────────────
# OUTPUT RENDERERS
# ─────────────────────────────────────────────
def render_output(phase):
    out = phase["output"]
    t   = out["type"]

    st.markdown(f"""
    <div class="out-card-title">{phase['output_title']}</div>
    <div class="out-card-sub">{phase['output_sub']}</div>
    """, unsafe_allow_html=True)

    if t == "table":
        html = ""
        for label, value in out["rows"]:
            html += f'<div class="table-row"><div class="table-label">{label}</div><div class="table-value">{value}</div></div>'
        st.markdown(f'<div class="out-card">{html}</div>', unsafe_allow_html=True)
        if out.get("flags"):
            flags_html = "".join(f'<div class="flag-item">⚠ {f}</div>' for f in out["flags"])
            st.markdown(f'<div class="flag-box"><div class="flag-title">AUTO-FILLED BY AI — SC TO VERIFY</div>{flags_html}</div>', unsafe_allow_html=True)

    elif t == "signals":
        for icon, tag, text in out["items"]:
            st.markdown(f"""
            <div class="signal-card">
              <div class="signal-tag">{icon} {tag}</div>
              <div class="signal-text">{text}</div>
            </div>""", unsafe_allow_html=True)

    elif t == "territories":
        for item in out["items"]:
            st.markdown(f"""
            <div class="territory-card">
              <div class="territory-num">TERRITORY {item['num']}</div>
              <div class="territory-name">{item['name']}</div>
              <div class="territory-row">
                <div class="territory-key">Theme</div>
                <div class="territory-val">{item['theme']}</div>
              </div>
              <div class="territory-row">
                <div class="territory-key">Message</div>
                <div class="territory-val"><em>"{item['message']}"</em></div>
              </div>
              <div class="territory-row">
                <div class="territory-key">Tone</div>
                <div class="territory-val">{item['tone']}</div>
              </div>
              <div class="territory-why">💡 {item['why']}</div>
            </div>""", unsafe_allow_html=True)

    elif t == "rollout":
        # Pillars
        st.markdown('<div style="font-size:11px;font-weight:700;letter-spacing:1.2px;color:#4b5563;margin-bottom:12px;text-transform:uppercase;">Content Pillars</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for i, (name, pct, desc) in enumerate(out["pillars"]):
            with cols[i]:
                st.markdown(f'<div class="pillar-card"><div class="pillar-name">{name}</div><div class="pillar-pct">{pct}</div><div class="pillar-desc">{desc}</div></div>', unsafe_allow_html=True)
        st.markdown('<div style="margin-top:20px;font-size:11px;font-weight:700;letter-spacing:1.2px;color:#4b5563;margin-bottom:10px;text-transform:uppercase;">Platform Strategy</div>', unsafe_allow_html=True)
        for name, formats in out["platforms"]:
            st.markdown(f'<div class="signal-card"><div class="signal-tag">{name}</div><div class="signal-text">{formats}</div></div>', unsafe_allow_html=True)
        st.markdown('<div style="margin-top:8px;font-size:11px;font-weight:700;letter-spacing:1.2px;color:#4b5563;margin-bottom:10px;text-transform:uppercase;">12-Week Timeline</div>', unsafe_allow_html=True)
        tl_html = ""
        for weeks, phase_name, desc in out["timeline"]:
            tl_html += f'<div class="timeline-item"><div class="timeline-weeks">{weeks}</div><div class="timeline-phase">{phase_name}</div><div class="timeline-desc">{desc}</div></div>'
        st.markdown(f'<div class="out-card">{tl_html}</div>', unsafe_allow_html=True)

    elif t == "kv":
        kv_html = ""
        for label, value in out["specs"]:
            kv_html += f'<div class="kv-row"><div class="kv-label">{label}</div><div class="kv-val">{value}</div></div>'
        st.markdown(f'<div class="out-card">{kv_html}</div>', unsafe_allow_html=True)

    elif t == "analytics":
        st.markdown(f'<div class="info-box">ℹ {out["note"]}</div>', unsafe_allow_html=True)
        import pandas as pd
        df = pd.DataFrame(out["kpis"], columns=["Objective", "Platform", "Metric", "Realistic ✅", "Breakthrough 🌟"])
        st.dataframe(df, use_container_width=True, hide_index=True)

    elif t == "deck":
        st.markdown('<div class="lark-synced">✅ Deck pushed to Canva — Link saved to Lark Docs</div>', unsafe_allow_html=True)
        st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
        cols = st.columns(2)
        for i, slide in enumerate(out["slides"]):
            with cols[i % 2]:
                st.markdown(f'<div class="slide-item">{slide}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# BUILD LEFT NAV HTML
# ─────────────────────────────────────────────
def build_leftnav():
    phase_idx = st.session_state.pitch_phase
    nav_html = '<div class="leftnav">'
    nav_html += '<div class="leftnav-section">Phases</div>'

    for i, p in enumerate(PHASES):
        s = st.session_state.pitch_statuses[i]
        is_sel = phase_idx == i
        css_class = "nav-item"
        if s == "done":
            css_class += " done"
        elif s == "active" and is_sel:
            css_class += " active"
        elif s == "pending":
            css_class += " pending"

        dot_color = p["color"] if (s == "active" and is_sel) else ("#4ade80" if s == "done" else "#1f2937")
        check = '<span class="nav-check">✓</span>' if s == "done" else ""
        nav_html += f'''
        <div class="{css_class}" style="--phase-color:{p['color']}">
          <div class="nav-dot" style="background:{dot_color};{'box-shadow:0 0 5px ' + p['color'] if (s == "active" and is_sel) else ''}"></div>
          <div class="nav-label">{p['name']}</div>
          {check}
        </div>'''

    nav_html += '<hr class="nav-divider">'
    nav_html += '<div class="leftnav-section">Output</div>'

    # Lark Docs status
    any_done = any(s == "done" for s in st.session_state.pitch_statuses)
    lark_class = "output-link synced" if any_done else "output-link"
    lark_icon  = "✓" if any_done else "○"
    nav_html += f'<div class="{lark_class}"><div class="output-link-dot"></div>Lark Docs {lark_icon}</div>'

    deck_done = st.session_state.pitch_statuses[6] == "done"
    canva_class = "output-link synced" if deck_done else "output-link"
    canva_icon  = "✓" if deck_done else "○"
    nav_html += f'<div class="{canva_class}"><div class="output-link-dot"></div>Canva Deck {canva_icon}</div>'
    nav_html += '</div>'
    return nav_html

# ─────────────────────────────────────────────
# BUILD PIPELINE STRIP HTML
# ─────────────────────────────────────────────
def build_pipeline():
    html = '<div class="pipeline-strip">'
    for i, p in enumerate(PHASES):
        s = st.session_state.pitch_statuses[i]
        icon = "✓ " if s == "done" else ("▶ " if s == "active" else "")
        html += f'<div class="pipe-step {s}">{icon}{p["name"]}</div>'
        if i < len(PHASES) - 1:
            html += '<div class="pipe-arrow">›</div>'
    html += '</div>'
    return html

# ─────────────────────────────────────────────
# BUILD CHAT HTML
# ─────────────────────────────────────────────
def build_chat_messages():
    html = '<div class="chat-messages" id="chat-messages">'
    for role, text in st.session_state.pitch_chat[-20:]:
        if role == "ai":
            html += f'<div><div class="chat-sender">frndOS</div><div class="chat-bubble-ai">{text}</div></div>'
        else:
            html += f'<div style="display:flex;flex-direction:column;align-items:flex-end;"><div class="chat-sender" style="text-align:right;">You</div><div class="chat-bubble-user">{text}</div></div>'
    html += '</div>'
    return html

# ─────────────────────────────────────────────
# 3-COLUMN LAYOUT SHELL via columns
# ─────────────────────────────────────────────

# Top bar
topbar_statuses = st.session_state.pitch_statuses
total   = len(PHASES)
done_ct = sum(1 for s in topbar_statuses if s == "done")
prog_pct = int(done_ct / total * 100)

st.markdown(f"""
<div class="topbar">
  <div class="topbar-logo">
    <div class="topbar-logo-dot"></div>
    frndOS
  </div>
  <div class="topbar-sep"></div>
  <div class="topbar-pitch-name">🚀 Campaign Pitch AI Express</div>
  <div class="topbar-sep"></div>
  <div class="topbar-campaign">{CLIENT} · {CAMPAIGN}</div>
  <div class="topbar-sep"></div>
  <div class="topbar-people">
    <span>SC: <b>{SC}</b></span>
    <span>CE: <b>{CE}</b></span>
  </div>
  <div class="topbar-badge">{done_ct}/{total} PHASES COMPLETE</div>
</div>
""", unsafe_allow_html=True)

# ── 3-column layout ──────────────────────────
col_nav, col_main, col_chat = st.columns([1.1, 4.5, 1.8])

# ── LEFT NAV ────────────────────────────────
with col_nav:
    st.markdown(build_leftnav(), unsafe_allow_html=True)
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if st.button("← Hub", use_container_width=True, key="back_hub"):
        st.switch_page("Home.py")
    # Phase nav buttons (invisible but functional)
    st.markdown("<div style='margin-top:4px'></div>", unsafe_allow_html=True)
    for i, p in enumerate(PHASES):
        s = st.session_state.pitch_statuses[i]
        is_sel = st.session_state.pitch_phase == i
        if st.button(
            p["name"],
            key=f"nav_{i}",
            use_container_width=True,
            disabled=(s == "pending"),
            type="primary" if is_sel else "secondary",
        ):
            st.session_state.pitch_phase = i
            st.rerun()

# ── MAIN CONTENT ─────────────────────────────
with col_main:
    idx   = st.session_state.pitch_phase
    phase = PHASES[idx]
    s     = st.session_state.pitch_statuses[idx]

    # Pipeline strip
    st.markdown(build_pipeline(), unsafe_allow_html=True)

    # Phase header
    badge_class = {"active": "badge-active", "done": "badge-done", "pending": "badge-pending"}[s]
    badge_label = {"active": "Active", "done": "Done ✓", "pending": "Locked"}[s]

    st.markdown(f"""
    <div class="phase-header">
      <div class="phase-icon">{phase['icon']}</div>
      <div class="phase-title">{phase['name']}</div>
      <div class="phase-status-badge {badge_class}">{badge_label}</div>
    </div>
    <div class="phase-desc">{phase['desc']}</div>
    """, unsafe_allow_html=True)

    # LOCKED
    if s == "pending":
        st.markdown("""
        <div class="locked-state">
          <div class="locked-icon">🔒</div>
          <div class="locked-title">Phase Locked</div>
          <div class="locked-sub">Complete and approve the previous phase to unlock.</div>
        </div>""", unsafe_allow_html=True)
        st.stop()

    # OUTPUT rendered
    if st.session_state.pitch_outputs.get(idx):
        render_output(phase)

        # APPROVAL PANEL
        if st.session_state.pitch_approval.get(idx):
            st.markdown('<div style="margin-top:24px;"></div>', unsafe_allow_html=True)
            st.markdown('<div class="approval-title">SC Approval Checklist</div>', unsafe_allow_html=True)

            checklist_items = CHECKLISTS.get(phase["id"], [])
            checks = st.session_state.pitch_checklist.get(idx, {})
            for j, item in enumerate(checklist_items):
                checked = st.checkbox(item, value=checks.get(j, False), key=f"chk_{idx}_{j}")
                checks[j] = checked
            st.session_state.pitch_checklist[idx] = checks
            all_checked = all(checks.get(j, False) for j in range(len(checklist_items)))

            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            col_a, col_r, _ = st.columns([2, 2, 3])
            with col_a:
                if st.button("✓ Approve & Continue", type="primary", use_container_width=True,
                             key=f"approve_{idx}", disabled=not all_checked):
                    st.session_state.pitch_statuses[idx] = "done"
                    if idx + 1 < len(PHASES):
                        st.session_state.pitch_statuses[idx + 1] = "active"
                        st.session_state.pitch_phase = idx + 1
                    st.session_state.pitch_approval[idx] = False
                    st.session_state.pitch_chat.append(
                        ("ai", f"{phase['name']} approved ✓" + (f" Moving to {PHASES[idx+1]['name']}." if idx+1 < len(PHASES) else " All phases complete!"))
                    )
                    st.rerun()
            with col_r:
                if st.button("✕ Request Revision", use_container_width=True, key=f"revise_{idx}"):
                    st.session_state[f"show_revision_{idx}"] = True
                    st.rerun()

            if not all_checked:
                st.caption("Complete all checklist items to enable approval.")

            if st.session_state.get(f"show_revision_{idx}"):
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                note = st.text_area("Revision notes", placeholder="Describe what needs to be revised...", key=f"rev_note_{idx}")
                if st.button("Submit Revision", key=f"submit_rev_{idx}"):
                    if note.strip():
                        st.session_state.pitch_chat.append(("user", f"Revision needed: {note}"))
                        st.session_state.pitch_chat.append(("ai", f"Got it. Regenerating {phase['name']} based on your feedback..."))
                        st.session_state.pitch_chat.append(("ai", f"{phase['name']} updated. Please review the revised output above."))
                        st.session_state[f"show_revision_{idx}"] = False
                        st.rerun()

        elif s == "done":
            st.markdown('<div class="lark-synced" style="margin-top:20px;">✅ Approved by SC — Output synced to Lark Docs</div>', unsafe_allow_html=True)

    else:
        # RUN BUTTON
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        if st.button(f"▶ {phase['btn']}", type="primary", key=f"run_{idx}"):
            for role, text in phase["chat"]:
                st.session_state.pitch_chat.append((role, text))
            st.session_state.pitch_outputs[idx]  = True
            st.session_state.pitch_approval[idx] = True
            st.rerun()

# ── RIGHT CHAT PANEL ──────────────────────────
with col_chat:
    st.markdown("""
    <div class="chat-panel" style="height:calc(100vh - 56px); display:flex; flex-direction:column; border-left:1px solid #1a1a2e; background:#0d0d1a;">
      <div class="chat-header">
        <div class="chat-header-dot"></div>
        <div class="chat-header-title">frndOS assistant</div>
        <div class="chat-header-sub">AI · Demo</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Chat messages in scrollable container
    chat_container = st.container(height=int(500))
    with chat_container:
        for role, text in st.session_state.pitch_chat[-20:]:
            if role == "ai":
                with st.chat_message("assistant"):
                    st.markdown(f"<span style='font-size:12px;line-height:1.5;color:#d1d5db;'>{text}</span>", unsafe_allow_html=True)
            else:
                with st.chat_message("user"):
                    st.markdown(f"<span style='font-size:12px;line-height:1.5;'>{text}</span>", unsafe_allow_html=True)

    user_msg = st.chat_input("Ask frndOS...", key="pitch_chat_input")
    if user_msg:
        st.session_state.pitch_chat.append(("user", user_msg))
        # Context-aware responses
        phase_name = PHASES[st.session_state.pitch_phase]["name"]
        responses = {
            "brief":     "I can help clarify the brief. What specific point needs attention?",
            "research":  "Good question — I can pull additional signals if needed. What category are you looking at?",
            "bigidea":   "All 3 territories are grounded in the research. Need help comparing them?",
            "rollout":   "The rollout is built around the approved territory. Want me to adjust the timeline split?",
            "kv":        "Visual direction is set. CE should confirm with the brand guidelines before production.",
            "analytics": "KPIs are benchmarked against skincare category norms. Want me to adjust the targets?",
            "deck":      "Deck is ready for final review. All 14 slides reflect approved outputs from each phase.",
        }
        phase_id = PHASES[st.session_state.pitch_phase]["id"]
        bot_reply = responses.get(phase_id, f"Got it — I'll take note of that for the {phase_name} phase.")
        st.session_state.pitch_chat.append(("ai", bot_reply))
        st.rerun()
