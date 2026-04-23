import streamlit as st
import time

st.set_page_config(
    page_title="Campaign Pitch AI Express — frndOS",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# DEMO DATA
# ─────────────────────────────────────────────

CLIENT   = "Lumia Skincare"
CAMPAIGN = "Real Radiance — Q3 2026"

PHASES = [
    {
        "id": "brief", "name": "Brief Decoder", "icon": "🔵",
        "color": "#3B82F6", "desc": "Reads & decodes client brief", "btn": "Decode Brief",
        "chat": [
            ("ai",   "Brief uploaded. Analyzing document structure and extracting objectives..."),
            ("ai",   "Found 3 unclear points in the brief. Auto-filling based on past pitches for Lumia."),
            ("ai",   "Done. Business Brief completed and saved to Lark Docs. Ready for Research phase?"),
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
                ("📈", "Trend",      '"Glass skin" & "dewy aesthetic" searches up 34% MoM on TikTok Indonesia'),
                ("👥", "Audience",   '71% of skincare purchase decisions influenced by TikTok "before/after" content'),
                ("🔥", "Content",    "Serum-focused routines generate 2.3× higher saves vs. other skincare formats"),
                ("⚡", "Competitor", 'Wardah "Flawless" line drove 89M TikTok views in 6 weeks via heavy UGC activation'),
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
            ("ai", "✅ Deck assembled and pushed to Canva. Link saved to Lark Docs. Ready for Jeff's final approval."),
        ],
        "output_title": "Pitch Deck — Real Radiance",
        "output_sub":   "14 slides assembled · Awaiting Jeff's final approval",
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
# SESSION STATE INIT
# ─────────────────────────────────────────────

def init_state():
    if "pitch_phase"    not in st.session_state: st.session_state.pitch_phase    = 0
    if "pitch_statuses" not in st.session_state: st.session_state.pitch_statuses = ["active"] + ["pending"] * (len(PHASES) - 1)
    if "pitch_outputs"  not in st.session_state: st.session_state.pitch_outputs  = {}
    if "pitch_chat"     not in st.session_state: st.session_state.pitch_chat     = [("ai", "Welcome to Campaign Pitch AI Express. Brief Decoder is ready — upload the client brief to begin.")]
    if "pitch_approval" not in st.session_state: st.session_state.pitch_approval = {}
    if "pitch_checklist"not in st.session_state: st.session_state.pitch_checklist= {}

init_state()

# ─────────────────────────────────────────────
# SIDEBAR — Phase Navigation + Chat
# ─────────────────────────────────────────────

with st.sidebar:
    if st.button("← Back to Hub", use_container_width=True):
        st.switch_page("Home.py")
    st.markdown("---")

    # Header
    st.markdown(f"""
    <div style="margin-bottom:8px;">
      <div style="font-size:11px;color:#6b7280;font-weight:700;letter-spacing:1.5px;margin-bottom:6px;">PITCH SESSION</div>
      <div style="font-size:14px;font-weight:700;color:#fff;">{CLIENT}</div>
      <div style="font-size:12px;color:#6b7280;">{CAMPAIGN}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex;gap:12px;margin:8px 0 12px;font-size:12px;color:#9ca3af;">
      <span>SC: <b style="color:#fff">Ryan</b></span>
      <span>CE: <b style="color:#fff">Lukman</b></span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("<div style='font-size:10px;font-weight:700;letter-spacing:1.5px;color:#4b5563;margin-bottom:8px;'>PHASES</div>", unsafe_allow_html=True)

    for i, p in enumerate(PHASES):
        s = st.session_state.pitch_statuses[i]
        is_sel = st.session_state.pitch_phase == i
        status_icon = "✓" if s == "done" else ("▶" if s == "active" else "○")
        label = f"{p['icon']} {p['name']}  {status_icon}" if s == "done" else f"{p['icon']} {p['name']}"
        if st.button(label, key=f"nav_{i}", use_container_width=True,
                     type="primary" if is_sel else "secondary",
                     disabled=(s == "pending")):
            st.session_state.pitch_phase = i
            st.rerun()

    st.markdown("---")
    st.markdown("<div style='font-size:10px;font-weight:700;letter-spacing:1.5px;color:#4b5563;margin-bottom:8px;'>OUTPUT</div>", unsafe_allow_html=True)
    st.markdown("○ Lark Docs")
    st.markdown("○ Canva Deck")

    # ── Chat panel ──────────────────────────────
    st.markdown("---")
    st.markdown("""
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
      <div style="width:8px;height:8px;border-radius:50%;background:#4ade80;box-shadow:0 0 5px #4ade80;"></div>
      <span style="font-size:13px;font-weight:600;color:#fff;">frndOS assistant</span>
    </div>
    """, unsafe_allow_html=True)

    chat_container = st.container(height=220)
    with chat_container:
        for role, text in st.session_state.pitch_chat[-12:]:
            with st.chat_message("assistant" if role == "ai" else "user"):
                st.write(text)

    user_msg = st.chat_input("Ask frndOS...", key="pitch_chat_input")
    if user_msg:
        st.session_state.pitch_chat.append(("user", user_msg))
        st.session_state.pitch_chat.append(("ai", "Got it — I'll take note of that for the current phase."))
        st.rerun()

# ─────────────────────────────────────────────
# HELPERS — Render output by type
# ─────────────────────────────────────────────

def render_output(phase):
    out = phase["output"]
    t   = out["type"]

    if t == "table":
        for label, value in out["rows"]:
            c1, c2 = st.columns([1, 2])
            with c1: st.markdown(f"<span style='color:#6b7280;font-size:13px;'>{label}</span>", unsafe_allow_html=True)
            with c2: st.markdown(f"<span style='font-size:13px;'>{value}</span>", unsafe_allow_html=True)
            st.divider()
        if out.get("flags"):
            st.warning("⚠ **Auto-filled by AI — SC to verify:**\n" + "\n".join(f"• {f}" for f in out["flags"]))

    elif t == "signals":
        for icon, tag, text in out["items"]:
            with st.container(border=True):
                st.markdown(f"**{icon} {tag}**")
                st.markdown(text)

    elif t == "territories":
        for item in out["items"]:
            with st.expander(f"**{item['num']} — {item['name']}**", expanded=True):
                st.markdown(f"🎯 **Theme:** {item['theme']}")
                st.markdown(f"💬 *\"{item['message']}\"*")
                st.markdown(f"🎨 **Tone:** {item['tone']}")
                st.markdown(f"💡 **Why:** {item['why']}")

    elif t == "rollout":
        st.markdown("**Content Pillars**")
        cols = st.columns(3)
        for i, (name, pct, desc) in enumerate(out["pillars"]):
            with cols[i]:
                st.metric(name, pct)
                st.caption(desc)
        st.markdown("**Platform Strategy**")
        for name, formats in out["platforms"]:
            st.markdown(f"- **{name}:** {formats}")
        st.markdown("**12-Week Timeline**")
        for weeks, phase_name, desc in out["timeline"]:
            with st.container(border=True):
                c1, c2 = st.columns([1, 3])
                with c1: st.markdown(f"**{weeks}**\n\n{phase_name}")
                with c2: st.markdown(desc)

    elif t == "kv":
        for label, value in out["specs"]:
            c1, c2 = st.columns([1, 2])
            with c1: st.markdown(f"**{label}**")
            with c2: st.markdown(value)
            st.divider()

    elif t == "analytics":
        st.info(f"ℹ {out['note']}")
        import pandas as pd
        df = pd.DataFrame(out["kpis"], columns=["Objective", "Platform", "Metric", "Realistic ✅", "Breakthrough 🌟"])
        st.dataframe(df, use_container_width=True, hide_index=True)

    elif t == "deck":
        st.success("✅ **Deck pushed to Canva** — Link saved to Lark Docs · Awaiting Jeff's final approval")
        cols = st.columns(2)
        for i, slide in enumerate(out["slides"]):
            with cols[i % 2]:
                st.markdown(f"<div style='background:#0E0E1C;border:1px solid #1E1E32;border-radius:8px;padding:8px 12px;font-size:12px;color:#9ca3af;margin-bottom:6px;'>{slide}</div>",
                            unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────

idx   = st.session_state.pitch_phase
phase = PHASES[idx]
s     = st.session_state.pitch_statuses[idx]

# Page header (pipeline progress strip)
st.markdown(f"# 🚀 Campaign Pitch AI Express")
cols_strip = st.columns(len(PHASES))
for i, p in enumerate(PHASES):
    ps = st.session_state.pitch_statuses[i]
    with cols_strip[i]:
        if ps == "done":
            st.markdown(f"<div style='text-align:center;font-size:10px;color:#4ade80;'>✓<br>{p['name']}</div>", unsafe_allow_html=True)
        elif ps == "active":
            st.markdown(f"<div style='text-align:center;font-size:10px;color:{p['color']};font-weight:700;'>▶<br>{p['name']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align:center;font-size:10px;color:#4b5563;'>○<br>{p['name']}</div>", unsafe_allow_html=True)
st.markdown("---")

# Phase title
status_badge = {"done": "✅ Done", "active": "⚡ Active", "pending": "🔒 Pending"}[s]
st.markdown(f"### {phase['icon']} {phase['name']} &nbsp; `{status_badge}`")
st.caption(phase["desc"])

# Locked state
if s == "pending":
    st.info("🔒 This phase is locked. Complete and approve previous phases to unlock.")
    st.stop()

# Output (if already run)
if st.session_state.pitch_outputs.get(idx):
    st.markdown(f"#### {phase['output_title']}")
    st.caption(phase["output_sub"])
    st.markdown("")
    render_output(phase)

    # ── Approval panel ─────────────────────────
    if st.session_state.pitch_approval.get(idx):
        st.markdown("---")
        st.markdown("#### SC Approval Checklist")
        checklist_items = CHECKLISTS.get(phase["id"], [])
        checks = st.session_state.pitch_checklist.get(idx, {})
        for j, item in enumerate(checklist_items):
            checked = st.checkbox(item, value=checks.get(j, False), key=f"chk_{idx}_{j}")
            checks[j] = checked
        st.session_state.pitch_checklist[idx] = checks

        all_checked = all(checks.get(j, False) for j in range(len(checklist_items)))
        st.markdown("")

        col_a, col_r = st.columns(2)
        with col_a:
            if st.button("✓ Approve & Continue", type="primary", use_container_width=True,
                         key=f"approve_{idx}", disabled=not all_checked):
                # Advance to next phase
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

        # Revision notes input
        if st.session_state.get(f"show_revision_{idx}"):
            st.markdown("")
            note = st.text_area("Revision notes", placeholder="Describe what needs to be revised...", key=f"rev_note_{idx}")
            if st.button("Submit Revision", key=f"submit_rev_{idx}"):
                if note.strip():
                    st.session_state.pitch_chat.append(("user", f"Revision needed: {note}"))
                    st.session_state.pitch_chat.append(("ai", f"Got it. Regenerating {phase['name']} based on your feedback..."))
                    st.session_state.pitch_chat.append(("ai", f"{phase['name']} updated. Please review the revised output above."))
                    st.session_state[f"show_revision_{idx}"] = False
                    st.rerun()

    # Already approved
    elif s == "done":
        st.success("✓ **Approved by SC** — output saved to Lark Docs")

else:
    # Run button
    if st.button(f"▶ {phase['btn']}", type="primary", use_container_width=True, key=f"run_{idx}"):
        # Animate chat messages
        for role, text in phase["chat"]:
            st.session_state.pitch_chat.append((role, text))
        # Mark output visible
        st.session_state.pitch_outputs[idx]  = True
        st.session_state.pitch_approval[idx] = True
        st.rerun()
