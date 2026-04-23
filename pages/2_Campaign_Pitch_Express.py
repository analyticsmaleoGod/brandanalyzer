import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Campaign Pitch AI Express — frndOS",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Auth guard ───────────────────────────────────────────────────
if not st.session_state.get("authenticated", False):
    st.switch_page("Home.py")

# ── Minimal CSS — only for things Streamlit can't do natively ────
st.markdown("""
<style>
/* Hide default sidebar toggle arrow — we use our own nav */
[data-testid="collapsedControl"] { display: none !important; }

/* Pipeline strip pill */
.pipe-pill {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    margin-right: 4px;
    margin-bottom: 4px;
    border: 1px solid transparent;
}
.pipe-done    { background: #e6f9f0; color: #166534; border-color: #bbf7d0; }
.pipe-active  { background: #eff6ff; color: #1d4ed8; border-color: #bfdbfe; }
.pipe-pending { background: #f9fafb; color: #9ca3af; border-color: #e5e7eb; }

/* Output block title */
.out-title { font-size: 18px; font-weight: 700; margin-bottom: 2px; }
.out-sub   { font-size: 13px; color: #6b7280; margin-bottom: 16px; }

/* Lark sync badge */
.lark-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: #f0fdf4; border: 1px solid #86efac;
    border-radius: 8px; padding: 6px 14px;
    font-size: 13px; color: #166534; font-weight: 600;
    margin-top: 12px; margin-bottom: 4px;
}

/* Chat bubble override for readability */
.chat-wrap { max-height: 340px; overflow-y: auto; padding: 4px 0; }
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
        "color": "#3B82F6", "desc": "Reads & decodes the client brief",
        "btn": "▶ Decode Brief",
        "chat": [
            ("ai", "Brief uploaded. Analyzing document structure and extracting objectives..."),
            ("ai", "Found 3 unclear points — auto-filling based on past pitches for Lumia."),
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
                ("Target Audience",    "Primary: Women 22–32, urban, skincare-aware\nSecondary: Beginners seeking entry product"),
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
        "color": "#10B981", "desc": "Market signals & competitor analysis",
        "btn": "▶ Run Research",
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
        "color": "#F59E0B", "desc": "3 campaign territories for SC to choose",
        "btn": "▶ Generate Ideas",
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
        "color": "#8B5CF6", "desc": "Content pillars, platform strategy & timeline",
        "btn": "▶ Build Rollout",
        "chat": [
            ("ai", 'Expanding "Glow Like You Mean It" into full campaign rollout...'),
            ("ai", "Content pillars, platform strategy, and 12-week timeline generated. Saved to Lark Docs."),
        ],
        "output_title": "Campaign Rollout — Glow Like You Mean It",
        "output_sub":   "12-week execution plan · Instagram + TikTok",
        "output": {
            "type": "rollout",
            "pillars":  [
                ("Education",       "40%", "Ingredient deep-dives, routine guides, expert tips"),
                ("Transformation",  "35%", "Before/after, skin journey, real results"),
                ("Community",       "25%", "UGC reposts, challenges, creator collabs"),
            ],
            "platforms":[
                ("Instagram", "Reels (hero), Carousels (edu), Stories (polls + CTAs)"),
                ("TikTok",    "Tutorials, Before/After, UGC challenge #GlowLikeYouMeanIt"),
            ],
            "timeline": [
                ("Wk 1–3",  "Teaser",  "Build intrigue, seed UGC creators, tease product"),
                ("Wk 4–8",  "Launch",  "Hero content push, paid amplification, creator activations"),
                ("Wk 9–12", "Sustain", "Community UGC, engagement nurture, retargeting"),
            ],
        },
    },
    {
        "id": "kv", "name": "KV Generator", "icon": "🟠",
        "color": "#F97316", "desc": "Visual direction & moodboard",
        "btn": "▶ Generate KV Direction",
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
        "color": "#06B6D4", "desc": "Success criteria & KPI framework",
        "btn": "▶ Generate KPI Framework",
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
        "color": "#22C55E", "desc": "Assembles & pushes to Canva deck template",
        "btn": "▶ Build Deck",
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

    st.markdown(f'<div class="out-title">{phase["output_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="out-sub">{phase["output_sub"]}</div>', unsafe_allow_html=True)

    if t == "table":
        df = pd.DataFrame(out["rows"], columns=["Field", "Value"])
        st.dataframe(df, use_container_width=True, hide_index=True)
        if out.get("flags"):
            st.warning("⚠️ **Auto-filled by AI — SC to verify:**\n" + "\n".join(f"• {f}" for f in out["flags"]))

    elif t == "signals":
        for icon, tag, text in out["items"]:
            with st.container(border=True):
                st.markdown(f"**{icon} {tag}**")
                st.write(text)

    elif t == "territories":
        for item in out["items"]:
            with st.expander(f"**Territory {item['num']} — {item['name']}**", expanded=True):
                col_l, col_r = st.columns([1, 2])
                with col_l:
                    st.markdown("**Theme**")
                    st.markdown("**Message**")
                    st.markdown("**Tone**")
                with col_r:
                    st.write(item["theme"])
                    st.markdown(f"*\"{item['message']}\"*")
                    st.write(item["tone"])
                st.info(f"💡 **Why this works:** {item['why']}")

    elif t == "rollout":
        st.markdown("**Content Pillars**")
        cols = st.columns(3)
        for i, (name, pct, desc) in enumerate(out["pillars"]):
            with cols[i]:
                st.metric(label=name, value=pct)
                st.caption(desc)

        st.markdown("**Platform Strategy**")
        for name, formats in out["platforms"]:
            with st.container(border=True):
                st.markdown(f"**{name}**")
                st.write(formats)

        st.markdown("**12-Week Timeline**")
        df_tl = pd.DataFrame(out["timeline"], columns=["Weeks", "Phase", "Description"])
        st.dataframe(df_tl, use_container_width=True, hide_index=True)

    elif t == "kv":
        df_kv = pd.DataFrame(out["specs"], columns=["Direction", "Spec"])
        st.dataframe(df_kv, use_container_width=True, hide_index=True)

    elif t == "analytics":
        st.info(f"ℹ️ {out['note']}")
        df_kpi = pd.DataFrame(out["kpis"], columns=["Objective", "Platform", "Metric", "Realistic ✅", "Breakthrough 🌟"])
        st.dataframe(df_kpi, use_container_width=True, hide_index=True)

    elif t == "deck":
        st.success("✅ **Deck pushed to Canva** — Link saved to Lark Docs · Awaiting final approval")
        col_a, col_b = st.columns(2)
        for i, slide in enumerate(out["slides"]):
            with (col_a if i % 2 == 0 else col_b):
                st.markdown(f"- {slide}")


# ─────────────────────────────────────────────
# SIDEBAR — Navigation
# ─────────────────────────────────────────────
with st.sidebar:

    if st.button("← Back to Hub", use_container_width=True):
        st.switch_page("Home.py")

    st.markdown("---")

    # Session header
    st.markdown(f"#### 🚀 Pitch Session")
    st.markdown(f"**{CLIENT}**")
    st.caption(CAMPAIGN)
    st.markdown(f"SC: **{SC}** &nbsp;·&nbsp; CE: **{CE}**")

    st.markdown("---")

    # Phase navigation
    st.markdown("**PHASES**")
    for i, p in enumerate(PHASES):
        s      = st.session_state.pitch_statuses[i]
        is_sel = st.session_state.pitch_phase == i
        icon   = "✅" if s == "done" else ("▶️" if s == "active" else "🔒")
        label  = f"{icon} {p['name']}"
        if st.button(label, key=f"nav_{i}", use_container_width=True,
                     type="primary" if is_sel else "secondary",
                     disabled=(s == "pending")):
            st.session_state.pitch_phase = i
            st.rerun()

    st.markdown("---")

    # Output links
    st.markdown("**OUTPUT**")
    any_done  = any(s == "done" for s in st.session_state.pitch_statuses)
    deck_done = st.session_state.pitch_statuses[-1] == "done"
    lark_icon  = "✅" if any_done  else "○"
    canva_icon = "✅" if deck_done else "○"
    st.markdown(f"{lark_icon} Lark Docs")
    st.markdown(f"{canva_icon} Canva Deck")

    st.markdown("---")

    # ── frndOS Assistant Chat ────────────────────
    st.markdown("#### 🟢 frndOS assistant")
    st.caption("AI · Demo mode")

    chat_box = st.container(height=260)
    with chat_box:
        for role, text in st.session_state.pitch_chat[-14:]:
            with st.chat_message("assistant" if role == "ai" else "user"):
                st.write(text)

    user_msg = st.chat_input("Ask frndOS...", key="pitch_chat_input")
    if user_msg:
        st.session_state.pitch_chat.append(("user", user_msg))
        phase_id = PHASES[st.session_state.pitch_phase]["id"]
        responses = {
            "brief":     "I can help clarify the brief. What specific point needs attention?",
            "research":  "Good question — I can pull additional signals if needed. What category are you focused on?",
            "bigidea":   "All 3 territories are grounded in the research. Need help comparing them?",
            "rollout":   "The rollout is built around the approved territory. Want to adjust the timeline split?",
            "kv":        "Visual direction is set. CE should confirm with the brand guidelines before production.",
            "analytics": "KPIs are benchmarked against skincare category norms. Want to adjust the targets?",
            "deck":      "Deck is ready for final review. All 14 slides reflect approved outputs from each phase.",
        }
        bot_reply = responses.get(phase_id, "Got it — noted for the current phase.")
        st.session_state.pitch_chat.append(("ai", bot_reply))
        st.rerun()


# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────
idx   = st.session_state.pitch_phase
phase = PHASES[idx]
s     = st.session_state.pitch_statuses[idx]

# ── Top: Pipeline progress strip ─────────────
done_ct = sum(1 for x in st.session_state.pitch_statuses if x == "done")
total   = len(PHASES)

st.markdown(f"### 🚀 Campaign Pitch AI Express &nbsp; `{done_ct}/{total} phases complete`")

strip_html = ""
for i, p in enumerate(PHASES):
    ps = st.session_state.pitch_statuses[i]
    icon = "✓ " if ps == "done" else ("▶ " if ps == "active" else "")
    css  = {"done": "pipe-done", "active": "pipe-active", "pending": "pipe-pending"}[ps]
    strip_html += f'<span class="pipe-pill {css}">{icon}{p["name"]}</span>'
st.markdown(strip_html, unsafe_allow_html=True)

st.markdown("---")

# ── Phase header ──────────────────────────────
badge_map = {
    "active":  ("Active",  "🔵"),
    "done":    ("Done ✓",  "✅"),
    "pending": ("Locked",  "🔒"),
}
badge_label, badge_icon = badge_map[s]

col_title, col_badge = st.columns([5, 1])
with col_title:
    st.markdown(f"## {phase['icon']} {phase['name']}")
    st.caption(phase["desc"])
with col_badge:
    st.markdown(f"<br>", unsafe_allow_html=True)
    if s == "active":
        st.info(badge_label)
    elif s == "done":
        st.success(badge_label)
    else:
        st.warning(badge_label)

# ── Locked ────────────────────────────────────
if s == "pending":
    st.markdown("")
    st.warning("🔒 **Phase locked.** Complete and approve the previous phase to unlock.")
    st.stop()

# ── Output ────────────────────────────────────
if st.session_state.pitch_outputs.get(idx):
    st.markdown("---")
    render_output(phase)

    # Approval panel
    if st.session_state.pitch_approval.get(idx):
        st.markdown("---")
        st.markdown("### SC Approval Checklist")

        checklist_items = CHECKLISTS.get(phase["id"], [])
        checks = st.session_state.pitch_checklist.get(idx, {})
        for j, item in enumerate(checklist_items):
            checked = st.checkbox(item, value=checks.get(j, False), key=f"chk_{idx}_{j}")
            checks[j] = checked
        st.session_state.pitch_checklist[idx] = checks
        all_checked = all(checks.get(j, False) for j in range(len(checklist_items)))

        st.markdown("")
        col_a, col_r, col_empty = st.columns([2, 2, 3])
        with col_a:
            if st.button("✅ Approve & Continue", type="primary", use_container_width=True,
                         key=f"approve_{idx}", disabled=not all_checked):
                st.session_state.pitch_statuses[idx] = "done"
                if idx + 1 < len(PHASES):
                    st.session_state.pitch_statuses[idx + 1] = "active"
                    st.session_state.pitch_phase = idx + 1
                st.session_state.pitch_approval[idx] = False
                next_name = PHASES[idx + 1]["name"] if idx + 1 < len(PHASES) else None
                st.session_state.pitch_chat.append((
                    "ai",
                    f"{phase['name']} approved ✓" + (f" Moving to {next_name}." if next_name else " All phases complete! 🎉")
                ))
                st.rerun()
        with col_r:
            if st.button("✏️ Request Revision", use_container_width=True, key=f"revise_{idx}"):
                st.session_state[f"show_revision_{idx}"] = True
                st.rerun()

        if not all_checked:
            st.caption("Complete all checklist items to enable approval.")

        if st.session_state.get(f"show_revision_{idx}"):
            st.markdown("")
            note = st.text_area("Revision notes", placeholder="Describe what needs to be revised...", key=f"rev_note_{idx}")
            if st.button("Submit Revision", key=f"submit_rev_{idx}"):
                if note.strip():
                    st.session_state.pitch_chat.append(("user", f"Revision needed: {note}"))
                    st.session_state.pitch_chat.append(("ai", f"Got it. Regenerating {phase['name']} based on your feedback..."))
                    st.session_state.pitch_chat.append(("ai", f"{phase['name']} updated. Please review the revised output."))
                    st.session_state[f"show_revision_{idx}"] = False
                    st.rerun()

    elif s == "done":
        st.markdown('<div class="lark-badge">✅ Approved by SC — Output synced to Lark Docs</div>', unsafe_allow_html=True)

else:
    # ── Run button (phase not yet executed) ───
    st.markdown("")
    st.markdown(f"**Ready to run this phase?** Click the button below to generate the output.")
    st.markdown("")
    if st.button(phase["btn"], type="primary", key=f"run_{idx}", use_container_width=False):
        for role, text in phase["chat"]:
            st.session_state.pitch_chat.append((role, text))
        st.session_state.pitch_outputs[idx]  = True
        st.session_state.pitch_approval[idx] = True
        st.rerun()
