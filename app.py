"""
AI Operations Diagnosis Agent + Project Recovery Agent.

Single Streamlit app, two diagnostic modes, one Layered Thinking framework.
"""

import json
import streamlit as st
from agents import classify_issue, run_ops_diagnosis, run_project_diagnosis
from playback import render_playback, reset_playback

st.set_page_config(
    page_title="The Diagnosis Engine",
    page_icon="🔍",
    layout="wide",
)

# ----------------------------------------------------------------------------
# CSS — Google Fonts + full Streamlit component overrides + custom classes
# ----------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Base ── */
html, body, [class*="css"], * {
    font-family: 'Inter', 'Source Sans', -apple-system, sans-serif !important;
}

/* ── Page background ── */
[data-testid="stAppViewContainer"] {
    background-color: #F1F5F9 !important;
}
[data-testid="stMain"] {
    background-color: transparent !important;
}
[data-testid="stHeader"] {
    background-color: transparent !important;
    border-bottom: none !important;
}

/* ── Main container ── */
.block-container {
    max-width: 1280px !important;
    padding-top: 1.5rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
    padding-bottom: 4rem !important;
}

/* ── Widget labels ── */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] {
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.09em !important;
    text-transform: uppercase !important;
    color: #475569 !important;
    margin-bottom: 4px !important;
}

/* ── Text input ── */
.stTextInput input {
    background: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 8px !important;
    font-size: 13.5px !important;
    color: #0F172A !important;
    padding: 10px 14px !important;
    height: 42px !important;
    transition: border-color 0.15s !important;
}
.stTextInput input:focus {
    border-color: #0F2044 !important;
    box-shadow: 0 0 0 3px rgba(15,32,68,0.10) !important;
    outline: none !important;
}
.stTextInput input::placeholder { color: #94A3B8 !important; }

/* ── Textarea ── */
.stTextArea textarea {
    background: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 8px !important;
    font-size: 13.5px !important;
    color: #0F172A !important;
    line-height: 1.65 !important;
    padding: 12px 14px !important;
    transition: border-color 0.15s !important;
}
.stTextArea textarea:focus {
    border-color: #0F2044 !important;
    box-shadow: 0 0 0 3px rgba(15,32,68,0.10) !important;
    outline: none !important;
}
.stTextArea textarea::placeholder { color: #94A3B8 !important; }

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 8px !important;
    font-size: 13.5px !important;
    color: #0F172A !important;
    min-height: 42px !important;
}
[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: #0F2044 !important;
    box-shadow: 0 0 0 3px rgba(15,32,68,0.10) !important;
}
[data-testid="stSelectbox"] svg { color: #64748B !important; }

/* ── Secondary buttons (compact default: view toggle, playback nav) ── */
[data-testid="stBaseButton-secondary"] button {
    background: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 8px !important;
    color: #0F2044 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    height: 40px !important;
    width: 100% !important;
    transition: border-color 0.15s, background 0.15s !important;
}
[data-testid="stBaseButton-secondary"] button:hover {
    background: #F8FAFC !important;
    border-color: #0F2044 !important;
}
[data-testid="stBaseButton-secondary"] button:focus:not(:active) {
    box-shadow: none !important;
    outline: none !important;
}

/* ── Mode picker cards (scoped to the three mode buttons by key) ── */
.st-key-btn_ops button,
.st-key-btn_proj button,
.st-key-btn_infer button {
    height: 80px !important;
    background: #FFFFFF !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 10px !important;
    color: #334155 !important;
    font-size: 13.5px !important;
    font-weight: 500 !important;
    text-align: left !important;
    white-space: normal !important;
    line-height: 1.55 !important;
    padding: 14px 18px !important;
}
.st-key-btn_ops button:hover,
.st-key-btn_proj button:hover,
.st-key-btn_infer button:hover {
    background: #F8FAFC !important;
    border-color: #94A3B8 !important;
}

/* ── Run Diagnosis button (primary) ── */
[data-testid="stBaseButton-primary"] button {
    background-color: #E63000 !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    letter-spacing: 0.03em !important;
    padding: 0 28px !important;
    border-radius: 8px !important;
    border: none !important;
    width: 100% !important;
    height: 48px !important;
}
[data-testid="stBaseButton-primary"] button:hover {
    background-color: #C42800 !important;
}
[data-testid="stBaseButton-primary"] button:active {
    background-color: #A82200 !important;
    transform: scale(0.99) !important;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] button {
    background: #FFFFFF !important;
    color: #0F2044 !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    width: auto !important;
    padding: 0 20px !important;
    height: 40px !important;
}
[data-testid="stDownloadButton"] button:hover {
    border-color: #0F2044 !important;
    background: #F8FAFC !important;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid #E2E8F0 !important;
    margin: 2rem 0 !important;
}

/* ── Info box (inference note) ── */
[data-testid="stAlertContainer"] {
    background: #EFF6FF !important;
    border: 1px solid #BFDBFE !important;
    border-radius: 8px !important;
    color: #1E3A8A !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] p {
    font-size: 13px !important;
    color: #64748B !important;
}

/* ─────────────────────────────────────────────
   APP HEADER (navy masthead)
───────────────────────────────────────────── */
.app-header {
    background: #0F2044;
    border-radius: 12px;
    padding: 28px 36px 26px;
    margin-bottom: 28px;
}
.app-header-eyebrow {
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #60A5FA;
    margin-bottom: 8px;
}
.app-header-title {
    font-size: 26px;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: -0.01em;
    margin-bottom: 5px;
    line-height: 1.2;
}
.app-header-sub {
    font-size: 13.5px;
    color: #94A3B8;
    font-weight: 400;
    line-height: 1.65;
}

/* ─────────────────────────────────────────────
   FORM SECTION LABEL
───────────────────────────────────────────── */
.form-section-label {
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #64748B;
    margin-bottom: 10px;
    margin-top: 4px;
}

/* ─────────────────────────────────────────────
   DIAGNOSIS OUTPUT
───────────────────────────────────────────── */
.diag-mode-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    margin-right: 8px;
}
.diag-mode-ops {
    background: #EFF6FF;
    color: #1E40AF;
    border: 1px solid #BFDBFE;
}
.diag-mode-project {
    background: #F0F9FF;
    color: #0369A1;
    border: 1px solid #BAE6FD;
}
.diag-done-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    background: #F0FDF4;
    color: #166534;
    border: 1px solid #BBF7D0;
}
.diag-classification {
    background: #EFF6FF;
    border-left: 4px solid #1D4ED8;
    border-radius: 0 10px 10px 0;
    padding: 13px 18px;
    font-size: 13.5px;
    color: #1E3A8A;
    font-weight: 600;
    margin-bottom: 24px;
    line-height: 1.5;
}
.diag-col-title {
    font-size: 15px;
    font-weight: 700;
    color: #0F2044;
    margin-bottom: 4px;
    padding-bottom: 10px;
    border-bottom: 2px solid #E2E8F0;
    letter-spacing: -0.01em;
}
.diag-layer-label {
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    margin: 20px 0 10px;
    display: flex;
    align-items: center;
    gap: 7px;
}
.diag-layer-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    flex-shrink: 0;
}
.l1-dot { background: #D97706; }
.l2-dot { background: #DC2626; }
.l3-dot { background: #7C3AED; }
.l1-text { color: #92400E; }
.l2-text { color: #991B1B; }
.l3-text { color: #5B21B6; }
.diag-item {
    font-size: 13px;
    color: #334155;
    padding: 7px 0 7px 14px;
    border-left: 2px solid #E2E8F0;
    margin-bottom: 5px;
    line-height: 1.55;
}
.diag-item-link {
    font-size: 11px;
    color: #94A3B8;
    margin-top: 3px;
    font-style: italic;
}
.diag-section-label {
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: #64748B;
    margin: 24px 0 10px;
    padding-bottom: 6px;
    border-bottom: 1px solid #F1F5F9;
}
.diag-action-item {
    font-size: 13px;
    color: #334155;
    padding: 8px 0 8px 14px;
    border-left: 3px solid #0F2044;
    margin-bottom: 8px;
    line-height: 1.55;
}
.diag-action-addr {
    font-size: 11px;
    color: #94A3B8;
    margin-top: 3px;
    font-style: italic;
}
.diag-phase-block {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-left: 4px solid #0F2044;
    border-radius: 0 10px 10px 0;
    padding: 14px 16px;
    margin-bottom: 10px;
}
.diag-phase-name {
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #0F2044;
    margin-bottom: 3px;
}
.diag-phase-focus {
    font-size: 12px;
    color: #64748B;
    font-style: italic;
    margin-bottom: 10px;
    line-height: 1.4;
}
.diag-phase-action {
    font-size: 12.5px;
    color: #334155;
    padding: 3px 0;
    line-height: 1.5;
    display: flex;
    gap: 7px;
}
.diag-phase-bullet {
    color: #0F2044;
    font-weight: 700;
    flex-shrink: 0;
    margin-top: 1px;
}
.diag-kpi-row {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    padding: 10px 0;
    border-bottom: 1px solid #F1F5F9;
    flex-wrap: wrap;
}
.diag-kpi-name {
    font-size: 12.5px;
    font-weight: 500;
    color: #0F172A;
    flex: 1;
    min-width: 160px;
    line-height: 1.4;
}
.diag-kpi-target {
    font-size: 11px;
    color: #94A3B8;
    margin-top: 3px;
    font-style: italic;
}
.pill {
    font-size: 10px;
    font-weight: 700;
    padding: 3px 9px;
    border-radius: 12px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    white-space: nowrap;
    flex-shrink: 0;
}
.pill-leading { background: #F0FDF4; color: #166534; border: 1px solid #BBF7D0; }
.pill-lagging { background: #FFFBEB; color: #92400E; border: 1px solid #FDE68A; }
.pill-inc { background: #F0FDF4; color: #166534; border: 1px solid #BBF7D0; }
.pill-dec { background: #FFF1F2; color: #9F1239; border: 1px solid #FECDD3; }
.pill-hold { background: #F8FAFC; color: #475569; border: 1px solid #E2E8F0; }
.diag-assume-item {
    background: #FFFBEB;
    border-left: 3px solid #F59E0B;
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    margin-bottom: 8px;
    font-size: 12.5px;
    color: #78350F;
    line-height: 1.5;
}
.diag-exec-box {
    background: #EFF6FF;
    border-left: 4px solid #2563EB;
    border-radius: 0 10px 10px 0;
    padding: 16px 18px;
    font-size: 13.5px;
    color: #1E3A8A;
    line-height: 1.7;
    margin-top: 4px;
}
.diag-download-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding-top: 8px;
}
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# Rendering helpers
# ----------------------------------------------------------------------------
def render_linked_items(items, primary_key, detail_key, detail_label):
    for item in items:
        detail = item[detail_key]
        detail_str = ", ".join(detail) if isinstance(detail, list) else detail
        st.markdown(
            f'<div class="diag-action-item">{item[primary_key]}'
            f'<div class="diag-action-addr">{detail_label}: {detail_str}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


def render_kpis(kpis):
    for kpi in kpis:
        direction = kpi["direction"]
        kpi_type = kpi["type"]
        arrow = "↑" if direction == "increase" else "↓" if direction == "decrease" else "→"
        dir_class = (
            "pill-inc" if direction == "increase"
            else "pill-dec" if direction == "decrease"
            else "pill-hold"
        )
        type_class = "pill-leading" if kpi_type == "leading" else "pill-lagging"
        st.markdown(
            f'<div class="diag-kpi-row">'
            f'<div class="diag-kpi-name">{kpi["kpi"]}'
            f'<div class="diag-kpi-target">Target: {kpi["target_or_threshold"]}</div>'
            f'</div>'
            f'<span class="pill {dir_class}">{arrow} {direction}</span>'
            f'<span class="pill {type_class}">{kpi_type}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )


def render_diagnosis(data, mode):
    is_project = mode == "project"

    mode_badge_class = "diag-mode-project" if is_project else "diag-mode-ops"
    mode_badge_text = "Project Recovery" if is_project else "Operations Diagnosis"

    layer_1_key = "layer_1_visible_risks" if is_project else "layer_1_symptoms"
    layer_2_key = "layer_2_risk_drivers" if is_project else "layer_2_root_causes"
    layer_2_item_key = "driver" if is_project else "cause"
    layer_2_link_key = "explains_risks" if is_project else "explains_symptoms"
    layer_1_label = "Layer 1: Visible delivery risks" if is_project else "Layer 1: Visible symptoms"
    layer_2_label = "Layer 2: Risk drivers" if is_project else "Layer 2: Root causes"

    st.markdown(
        f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:20px;">'
        f'<span class="diag-mode-badge {mode_badge_class}">{mode_badge_text}</span>'
        f'<span class="diag-done-badge">&#10003; Diagnosis complete</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div style="font-size:10.5px;font-weight:700;letter-spacing:0.09em;'
        f'text-transform:uppercase;color:#64748B;margin-bottom:8px;">Issue classification</div>'
        f'<div class="diag-classification">{data["classification"]}</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="diag-col-title">Layered diagnosis</div>', unsafe_allow_html=True)

        st.markdown(
            f'<div class="diag-layer-label {" ".join(["l1-text"])}">'
            f'<span class="diag-layer-dot l1-dot"></span>{layer_1_label}</div>',
            unsafe_allow_html=True,
        )
        for item in data[layer_1_key]:
            st.markdown(f'<div class="diag-item">{item}</div>', unsafe_allow_html=True)

        st.markdown(
            f'<div class="diag-layer-label l2-text">'
            f'<span class="diag-layer-dot l2-dot"></span>{layer_2_label}</div>',
            unsafe_allow_html=True,
        )
        for item in data[layer_2_key]:
            detail = item[layer_2_link_key]
            detail_str = ", ".join(detail) if isinstance(detail, list) else detail
            st.markdown(
                f'<div class="diag-item">{item[layer_2_item_key]}'
                f'<div class="diag-item-link">Explains: {detail_str}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            f'<div class="diag-layer-label l3-text">'
            f'<span class="diag-layer-dot l3-dot"></span>Layer 3: Structural conditions</div>',
            unsafe_allow_html=True,
        )
        for item in data["layer_3_structural"]:
            st.markdown(f'<div class="diag-item">{item}</div>', unsafe_allow_html=True)

        st.markdown(
            '<div class="diag-section-label">Recommended actions</div>',
            unsafe_allow_html=True,
        )
        render_linked_items(
            data["recommended_actions"],
            primary_key="action",
            detail_key="addresses",
            detail_label="Addresses",
        )

    with col2:
        st.markdown('<div class="diag-col-title">Phased action plan</div>', unsafe_allow_html=True)
        for phase in data["action_plan"]:
            actions_html = "".join(
                f'<div class="diag-phase-action">'
                f'<span class="diag-phase-bullet">&#8226;</span>{a}'
                f'</div>'
                for a in phase["actions"]
            )
            st.markdown(
                f'<div class="diag-phase-block">'
                f'<div class="diag-phase-name">{phase["phase"]}</div>'
                f'<div class="diag-phase-focus">{phase["focus"]}</div>'
                f'{actions_html}'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            '<div class="diag-section-label">KPIs to monitor</div>',
            unsafe_allow_html=True,
        )
        render_kpis(data["kpis"])

        st.markdown(
            '<div class="diag-section-label">Assumptions to test</div>',
            unsafe_allow_html=True,
        )
        for item in data["assumptions_to_test"]:
            st.markdown(
                f'<div class="diag-assume-item">{item}</div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            '<div class="diag-section-label">Executive summary</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="diag-exec-box">{data["executive_summary"]}</div>',
            unsafe_allow_html=True,
        )

    st.divider()
    st.download_button(
        "Download diagnosis (JSON)",
        data=json.dumps(data, indent=2),
        file_name=f"{mode}_diagnosis.json",
        mime="application/json",
    )


# ----------------------------------------------------------------------------
# App layout
# ----------------------------------------------------------------------------
st.markdown("""
<div class="app-header">
    <div class="app-header-eyebrow">Layered Thinking Framework</div>
    <div class="app-header-title">The Diagnosis Engine</div>
    <div class="app-header-sub">
        From symptom to structure.<br>
        One framework, two modes. Operations Diagnosis and Project Recovery.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Mode picker state ──
if "mode" not in st.session_state:
    st.session_state.mode = "operations"


def _set_mode(value):
    st.session_state.mode = value


MODE_CARDS = [
    (
        "operations",
        "btn_ops",
        "Operating System",
        "Ongoing performance, team, queue, workflow",
    ),
    (
        "project",
        "btn_proj",
        "Project Recovery",
        "Delivery, sprints, milestones, scope, stakeholder alignment",
    ),
    (
        "infer",
        "btn_infer",
        "Let the tool decide",
        "Infer mode from your description",
    ),
]

# Persistent highlight for the selected card. Keyed elements carry a stable
# .st-key-{key} class, so we target the selected button directly instead of
# walking the DOM. The focus variants are included so the highlight holds
# through Streamlit's focus styling, and this rule is injected after the
# global CSS block so it wins on source order.
_selected_key = {m: k for m, k, _, _ in MODE_CARDS}[st.session_state.mode]
st.markdown(f"""
<style>
.st-key-{_selected_key} button,
.st-key-{_selected_key} button:focus,
.st-key-{_selected_key} button:focus:not(:active) {{
    background: #EFF6FF !important;
    border: 2px solid #0F2044 !important;
    color: #0F2044 !important;
    font-weight: 700 !important;
}}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="form-section-label">What are you diagnosing?</div>',
    unsafe_allow_html=True,
)

mc_cols = st.columns(3, gap="small")
for _col, (_value, _key, _title, _subtitle) in zip(mc_cols, MODE_CARDS):
    with _col:
        st.button(
            f"{_title}\n\n{_subtitle}",
            key=_key,
            type="secondary",
            use_container_width=True,
            on_click=_set_mode,
            args=(_value,),
        )

st.markdown('<div style="height: 4px;"></div>', unsafe_allow_html=True)

issue = st.text_area(
    "Describe the issue",
    placeholder="e.g. Resolution team is hitting cases per hour but missing CSAT. Repeat cases are climbing.",
    height=110,
)

stated_outcome = st.text_input(
    "Stated outcome or promise — optional but recommended",
    placeholder="e.g. Increase CSAT to 92 percent without losing case throughput.",
)

col1, col2, col3 = st.columns(3, gap="medium")
with col1:
    context = st.selectbox("Industry / context", [
        "Contact Center Operations", "Supply Chain / Logistics",
        "Field Operations", "IT Service Delivery", "HR / People Operations",
        "Project / Program Management", "Retail Operations",
        "Healthcare Operations", "Financial Services Operations", "Other",
    ])
with col2:
    urgency = st.selectbox("Urgency level", ["High", "Medium", "Low"])
with col3:
    operating_culture = st.selectbox("Operating culture", [
        "Outcome-focused (flexible on method)",
        "Method-focused (must use existing processes)",
        "Mixed or unsure",
    ])

col4, col5 = st.columns([1, 1], gap="medium")
with col4:
    relationship = st.selectbox("Your relationship to this system", [
        "Current owner (I run this today)",
        "Prospective owner (I would inherit or take this over)",
        "External diagnostician (consultant, peer team, advisor)",
        "Other or not sure",
    ])
with col5:
    team_size = st.text_input(
        "Team size or volume context",
        placeholder="e.g. 25 associates, 4 supervisors, 1 manager",
    )

st.markdown('<div style="height: 4px;"></div>', unsafe_allow_html=True)
run = st.button("Run Diagnosis", key="run_btn", type="primary", use_container_width=True)


# ----------------------------------------------------------------------------
# Execution — the result is stored in session state so it survives the
# reruns triggered by playback navigation, the view toggle, and downloads.
# ----------------------------------------------------------------------------
if run:
    if not issue.strip():
        st.warning("Please describe the issue before running the diagnosis.")
    else:
        inputs = {
            "issue": issue,
            "context": context,
            "urgency": urgency,
            "team_size": team_size,
            "stated_outcome": stated_outcome,
            "operating_culture": operating_culture,
            "relationship": relationship,
        }

        _selected = st.session_state.get("mode", "operations")
        if _selected == "operations":
            mode = "operations"
            inferred_note = None
        elif _selected == "project":
            mode = "project"
            inferred_note = None
        else:
            with st.spinner("Routing your issue..."):
                try:
                    routing = classify_issue(issue)
                    mode = routing["mode"]
                    inferred_note = (
                        f"Routed this as a **{mode}** issue "
                        f"(confidence: {routing['confidence']}). "
                        f"{routing['reason']} "
                        f"Switch the mode above if that read is wrong."
                    )
                except Exception as e:
                    st.error(f"Routing failed: {str(e)}")
                    st.stop()

        with st.spinner("Running diagnosis..."):
            try:
                if mode == "operations":
                    data, refusal = run_ops_diagnosis(inputs)
                else:
                    data, refusal = run_project_diagnosis(inputs)

                if refusal:
                    st.error("The model declined to diagnose this input.")
                    st.info(refusal)
                else:
                    st.session_state.diagnosis = {
                        "data": data,
                        "mode": mode,
                        "note": inferred_note,
                    }
                    reset_playback()

            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")
                st.info(
                    "Make sure your OPENAI_API_KEY is set in your Streamlit secrets "
                    "or environment variables. If you see a model-not-found error, "
                    "change MODEL in agents.py to gpt-4o as a fallback."
                )


# ----------------------------------------------------------------------------
# Results — rendered from session state on every run so the diagnosis
# persists across interactions. Two views: guided playback and full report.
# ----------------------------------------------------------------------------
if "diagnosis" in st.session_state:
    saved = st.session_state.diagnosis

    st.divider()

    if saved.get("note"):
        st.info(saved["note"])

    # ── View toggle ──
    if "view" not in st.session_state:
        st.session_state.view = "playback"

    def _set_view(value):
        st.session_state.view = value

    VIEW_TABS = [
        ("playback", "view_playback", "Guided playback"),
        ("report", "view_report", "Full report"),
    ]

    _view_key = {v: k for v, k, _ in VIEW_TABS}[st.session_state.view]
    st.markdown(f"""
<style>
.st-key-{_view_key} button,
.st-key-{_view_key} button:focus,
.st-key-{_view_key} button:focus:not(:active) {{
    background: #0F2044 !important;
    border: 1.5px solid #0F2044 !important;
    color: #FFFFFF !important;
}}
</style>
""", unsafe_allow_html=True)

    vc1, vc2, _spacer = st.columns([1, 1, 3], gap="small")
    with vc1:
        st.button(
            "Guided playback",
            key="view_playback",
            type="secondary",
            use_container_width=True,
            on_click=_set_view,
            args=("playback",),
        )
    with vc2:
        st.button(
            "Full report",
            key="view_report",
            type="secondary",
            use_container_width=True,
            on_click=_set_view,
            args=("report",),
        )

    if st.session_state.view == "playback":
        render_playback(saved["data"], saved["mode"])
    else:
        render_diagnosis(saved["data"], saved["mode"])
