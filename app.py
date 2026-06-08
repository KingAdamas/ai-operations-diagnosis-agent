"""
AI Operations Diagnosis Agent + Project Recovery Agent.

Single Streamlit app, two diagnostic modes, one Layered Thinking framework.
"""

import json

import streamlit as st

from agents import classify_issue, run_ops_diagnosis, run_project_diagnosis


# ----------------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Operations Diagnosis Agent",
    page_icon="🔍",
    layout="wide",
)


# ----------------------------------------------------------------------------
# Styling
# ----------------------------------------------------------------------------
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 0.25rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #555;
        margin-bottom: 1.5rem;
    }
    .mode-badge {
        display: inline-block;
        background: #fef3c7;
        color: #92400e;
        padding: 0.25rem 0.85rem;
        border-radius: 16px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1.25rem;
    }
    .mode-badge-project {
        background: #dbeafe;
        color: #1e40af;
    }
    .layer-header {
        font-size: 1.3rem;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .layer-1 { color: #d97706; }
    .layer-2 { color: #dc2626; }
    .layer-3 { color: #7c3aed; }
    .section-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .exec-summary {
        background: #f0f9ff;
        border-left: 4px solid #0284c7;
        padding: 1rem 1.25rem;
        border-radius: 0 8px 8px 0;
        margin-top: 0.5rem;
    }
    .classification-box {
        background: #f0fdf4;
        border-left: 4px solid #16a34a;
        padding: 0.75rem 1rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 1.5rem;
        font-size: 0.95rem;
        color: #15803d;
        font-weight: 500;
    }
    .phase-block {
        background: #fafafa;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.75rem;
    }
    .phase-label {
        font-weight: 600;
        color: #1a1a1a;
        font-size: 1.05rem;
    }
    .phase-focus {
        font-size: 0.9rem;
        color: #555;
        margin-bottom: 0.5rem;
        font-style: italic;
    }
    .linked-item {
        margin-bottom: 0.6rem;
    }
    .linked-detail {
        font-size: 0.85rem;
        color: #6b7280;
        margin-left: 1.25rem;
        margin-top: 0.15rem;
    }
    .kpi-row {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 0.5rem;
        flex-wrap: wrap;
    }
    .kpi-name { font-weight: 500; }
    .kpi-tag {
        font-size: 0.75rem;
        padding: 2px 8px;
        border-radius: 10px;
        font-weight: 500;
    }
    .kpi-tag-leading { background: #ecfdf5; color: #065f46; }
    .kpi-tag-lagging { background: #fef3c7; color: #92400e; }
    .kpi-tag-direction { background: #f3f4f6; color: #374151; }
    .assumption-item {
        background: #fffbeb;
        border-left: 3px solid #f59e0b;
        padding: 0.6rem 0.85rem;
        border-radius: 0 6px 6px 0;
        margin-bottom: 0.5rem;
        font-size: 0.92rem;
    }
    .stButton > button {
        background-color: #e63000;
        color: white;
        font-weight: 600;
        padding: 0.6rem 2rem;
        border-radius: 6px;
        border: none;
        font-size: 1rem;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #c42800;
        color: white;
    }
    .complete-badge {
        background: #dcfce7;
        color: #15803d;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
    }
</style>
""",
    unsafe_allow_html=True,
)


# ----------------------------------------------------------------------------
# Rendering helpers
# ----------------------------------------------------------------------------
def render_linked_items(items, primary_key, detail_key, detail_label):
    for item in items:
        detail = item[detail_key]
        detail_str = ", ".join(detail) if isinstance(detail, list) else detail
        st.markdown(
            f'<div class="linked-item">• <b>{item[primary_key]}</b>'
            f'<div class="linked-detail">{detail_label}: {detail_str}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


def render_kpis(kpis):
    for kpi in kpis:
        direction = kpi["direction"]
        kpi_type = kpi["type"]
        arrow = (
            "↑" if direction == "increase"
            else "↓" if direction == "decrease"
            else "→"
        )
        tag_class = (
            "kpi-tag-leading" if kpi_type == "leading" else "kpi-tag-lagging"
        )
        st.markdown(
            f'<div class="kpi-row">'
            f'<span class="kpi-name">{kpi["kpi"]}</span>'
            f'<span class="kpi-tag kpi-tag-direction">{arrow} {direction}</span>'
            f'<span class="kpi-tag {tag_class}">{kpi_type}</span>'
            f'</div>'
            f'<div class="linked-detail" style="margin-bottom: 0.7rem; margin-left: 0;">'
            f'Target: {kpi["target_or_threshold"]}</div>',
            unsafe_allow_html=True,
        )


def render_diagnosis(data, mode):
    is_project = mode == "project"

    badge_class = "mode-badge mode-badge-project" if is_project else "mode-badge"
    badge_text = (
        "Project Recovery Mode" if is_project else "Operations Diagnosis Mode"
    )

    layer_1_key = "layer_1_visible_risks" if is_project else "layer_1_symptoms"
    layer_2_key = "layer_2_risk_drivers" if is_project else "layer_2_root_causes"
    layer_2_item_key = "driver" if is_project else "cause"
    layer_2_link_key = "explains_risks" if is_project else "explains_symptoms"
    layer_1_label = (
        "Layer 1: Visible delivery risks" if is_project
        else "Layer 1: Visible symptoms"
    )
    layer_2_label = (
        "Layer 2: Risk drivers" if is_project else "Layer 2: Root causes"
    )

    st.markdown(f'<div class="{badge_class}">{badge_text}</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="complete-badge">✓ Diagnosis complete</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### Issue classification")
    st.markdown(
        f'<div class="classification-box">{data["classification"]}</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("## Layered diagnosis")

        st.markdown(
            f'<p class="layer-header layer-1">{layer_1_label}</p>',
            unsafe_allow_html=True,
        )
        for item in data[layer_1_key]:
            st.markdown(f"- {item}")

        st.markdown(
            f'<p class="layer-header layer-2">{layer_2_label}</p>',
            unsafe_allow_html=True,
        )
        render_linked_items(
            data[layer_2_key],
            primary_key=layer_2_item_key,
            detail_key=layer_2_link_key,
            detail_label="Explains",
        )

        st.markdown(
            '<p class="layer-header layer-3">Layer 3: Structural conditions</p>',
            unsafe_allow_html=True,
        )
        for item in data["layer_3_structural"]:
            st.markdown(f"- {item}")

        st.markdown(
            '<p class="section-header">Recommended actions</p>',
            unsafe_allow_html=True,
        )
        render_linked_items(
            data["recommended_actions"],
            primary_key="action",
            detail_key="addresses",
            detail_label="Addresses",
        )

    with col2:
        st.markdown("## Phased action plan")
        for phase in data["action_plan"]:
            actions_html = "".join(
                f"<div>• {a}</div>" for a in phase["actions"]
            )
            st.markdown(
                f'<div class="phase-block">'
                f'<div class="phase-label">{phase["phase"]}</div>'
                f'<div class="phase-focus">{phase["focus"]}</div>'
                f"{actions_html}</div>",
                unsafe_allow_html=True,
            )

        st.markdown(
            '<p class="section-header">KPIs to monitor</p>',
            unsafe_allow_html=True,
        )
        render_kpis(data["kpis"])

        st.markdown(
            '<p class="section-header">Assumptions to test</p>',
            unsafe_allow_html=True,
        )
        for item in data["assumptions_to_test"]:
            st.markdown(
                f'<div class="assumption-item">{item}</div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            '<p class="section-header">Executive summary</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="exec-summary">{data["executive_summary"]}</div>',
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
st.markdown(
    '<p class="main-header">AI Operations Diagnosis Agent</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="sub-header">Layered Thinking, applied. Diagnose an operating '
    "system or recover a project that is off track.</p>",
    unsafe_allow_html=True,
)

mode_choice = st.radio(
    "What are you diagnosing?",
    options=[
        "Operating system (ongoing performance, team, queue, workflow)",
        "Project that is off track (delivery, milestones, scope, risk)",
        "Not sure, let the tool decide",
    ],
    index=0,
    horizontal=False,
)

issue = st.text_area(
    "Describe the issue",
    placeholder=(
        "e.g. Resolution team is hitting cases per hour but missing CSAT. "
        "Repeat cases are climbing."
    ),
    height=120,
)

stated_outcome = st.text_input(
    "Stated outcome or promise (optional but recommended)",
    placeholder=(
        "e.g. Increase CSAT to 92 percent without losing case throughput."
    ),
)

col1, col2, col3 = st.columns(3)

with col1:
    context_options = [
        "Contact Center Operations",
        "Supply Chain / Logistics",
        "Field Operations",
        "IT Service Delivery",
        "HR / People Operations",
        "Project / Program Management",
        "Retail Operations",
        "Healthcare Operations",
        "Financial Services Operations",
        "Other",
    ]
    context = st.selectbox("Industry / context", context_options)

with col2:
    urgency = st.selectbox("Urgency level", ["High", "Medium", "Low"])

with col3:
    operating_culture = st.selectbox(
        "Operating culture",
        [
            "Outcome-focused (flexible on method)",
            "Method-focused (must use existing processes)",
            "Mixed or unsure",
        ],
    )

relationship = st.selectbox(
    "Your relationship to this system",
    [
        "Current owner (I run this today)",
        "Prospective owner (I would inherit or take this over)",
        "External diagnostician (consultant, peer team, advisor)",
        "Other or not sure",
    ],
)

team_size = st.text_input(
    "Team size or volume context",
    placeholder="e.g. 25 associates, 4 supervisors, 1 manager",
)

run = st.button("Run Diagnosis")


# ----------------------------------------------------------------------------
# Execution
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

        if mode_choice.startswith("Operating system"):
            mode = "operations"
            inferred_note = None
        elif mode_choice.startswith("Project"):
            mode = "project"
            inferred_note = None
        else:
            with st.spinner("Routing..."):
                try:
                    routing = classify_issue(issue)
                    mode = routing["mode"]
                    inferred_note = (
                        f"Routed this as a **{mode}** issue "
                        f"(confidence: {routing['confidence']}). "
                        f"{routing['reason']} "
                        f"Switch the radio above if that read is wrong."
                    )
                except Exception as e:
                    st.error(f"Routing failed: {str(e)}")
                    st.stop()

        if inferred_note:
            st.info(inferred_note)

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
                    st.divider()
                    render_diagnosis(data, mode)

            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")
                st.info(
                    "Make sure your OPENAI_API_KEY is set in your Streamlit "
                    "secrets or environment variables. If you get a "
                    "model-not-found error, your account may not have access "
                    "to gpt-5-mini yet. Change MODEL in agents.py to gpt-4o "
                    "as a fallback."
                )
