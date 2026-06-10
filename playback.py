"""
Guided playback view for The Diagnosis Engine.

Drop-in module. No changes to schemas.py, prompts.py, or agents.py required.

Integration in app.py, in the results section after a diagnosis succeeds:

    from playback import render_playback, reset_playback

    # Call once, right after a NEW diagnosis result is produced:
    reset_playback()

    # Then render. mode is "operations" or "project":
    render_playback(result, mode)

To offer both views, wrap with a toggle:

    view = st.radio(
        "View", ["Guided playback", "Full report"],
        horizontal=True, label_visibility="collapsed",
    )
    if view == "Guided playback":
        render_playback(result, mode)
    else:
        render_full_report(result, mode)  # your existing renderer

The playback walks the viewer through the Layered Thinking Framework one
layer at a time: the case, Layer 1, a prediction pause, Layer 2 with
linkage back to the Layer 1 items each cause explains, Layer 3 with the
viewer's prediction shown beside the structural findings, recommendations
tagged with what they address, the phased plan with KPIs and assumptions,
and the executive summary with an optional look at the agent's working
notes.
"""

import difflib

import streamlit as st

# ----------------------------------------------------------------------------
# Mode-aware field map. Ops and project schemas share a shape but use
# different field names for the first two layers.
# ----------------------------------------------------------------------------
FIELDS = {
    "operations": {
        "layer1_key": "layer_1_symptoms",
        "layer1_title": "Layer 1: Visible symptoms",
        "layer1_lead": "What the surface shows. Most conversations stop here.",
        "tag_prefix": "S",
        "layer2_key": "layer_2_root_causes",
        "layer2_title": "Layer 2: Root causes",
        "layer2_lead": "Each cause is accountable to the symptoms it explains.",
        "layer2_item_key": "cause",
        "layer2_links_key": "explains_symptoms",
        "links_label": "Explains",
    },
    "project": {
        "layer1_key": "layer_1_visible_risks",
        "layer1_title": "Layer 1: Visible risks",
        "layer1_lead": "What the surface shows. Most conversations stop here.",
        "tag_prefix": "R",
        "layer2_key": "layer_2_risk_drivers",
        "layer2_title": "Layer 2: Risk drivers",
        "layer2_lead": "Each driver is accountable to the risks it explains.",
        "layer2_item_key": "driver",
        "layer2_links_key": "explains_risks",
        "links_label": "Explains",
    },
}

STEP_TITLES = [
    "The case",
    "Layer 1",
    "Your read",
    "Layer 2",
    "Layer 3",
    "Recommended actions",
    "Plan and proof",
    "Executive summary",
]

_DIRECTION_GLYPHS = {"increase": "▲", "decrease": "▼", "hold": "■"}

_CSS = """
<style>
.pb-card {
    border: 1px solid #D8DEE9;
    border-left: 4px solid #1F3A5F;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 10px;
    background: #FFFFFF;
}
.pb-card-structural { border-left-color: #8C2F39; }
.pb-card-action { border-left-color: #2F6B4F; }
.pb-tag {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #5A6B8C;
    margin-bottom: 4px;
}
.pb-chip {
    display: inline-block;
    padding: 3px 12px;
    margin: 3px 6px 3px 0;
    border-radius: 14px;
    font-size: 0.82rem;
    background: #EEF1F6;
    color: #33415C;
    border: 1px solid #D8DEE9;
}
.pb-chip-hot {
    background: #1F3A5F;
    color: #FFFFFF;
    border-color: #1F3A5F;
}
.pb-addresses {
    font-size: 0.82rem;
    color: #5A6B8C;
    margin-top: 6px;
}
.pb-quote {
    border-left: 3px solid #B9C2D4;
    padding: 8px 14px;
    color: #4A5670;
    font-style: italic;
    background: #F6F8FB;
    border-radius: 0 8px 8px 0;
    margin-bottom: 12px;
}
</style>
"""


# ----------------------------------------------------------------------------
# State helpers
# ----------------------------------------------------------------------------
def reset_playback():
    """Call once whenever a NEW diagnosis result is produced."""
    st.session_state["pb_step"] = 0
    st.session_state["pb_prediction"] = ""
    st.session_state.pop("pb_prediction_input", None)


def _capture_prediction():
    text = st.session_state.get("pb_prediction_input")
    if text is not None:
        st.session_state["pb_prediction"] = text.strip()


def _go(delta):
    _capture_prediction()
    step = st.session_state.get("pb_step", 0) + delta
    st.session_state["pb_step"] = max(0, min(step, len(STEP_TITLES) - 1))


def _jump_to_end():
    _capture_prediction()
    st.session_state["pb_step"] = len(STEP_TITLES) - 1


# ----------------------------------------------------------------------------
# Linkage matching. explains_symptoms / explains_risks entries are free
# strings written by the model; they usually echo a Layer 1 item but are not
# guaranteed to match it verbatim. Fuzzy-match each link to its closest
# Layer 1 item so we can light up the right chip.
# ----------------------------------------------------------------------------
def _match_layer1(link_text, layer1_items, threshold=0.45):
    """Return the index of the Layer 1 item this link refers to, or None."""
    if not layer1_items or not link_text:
        return None
    if link_text in layer1_items:
        return layer1_items.index(link_text)
    link_low = link_text.lower().strip()
    best_idx, best_score = None, 0.0
    for i, item in enumerate(layer1_items):
        item_low = item.lower().strip()
        if link_low in item_low or item_low in link_low:
            return i
        score = difflib.SequenceMatcher(None, link_low, item_low).ratio()
        if score > best_score:
            best_idx, best_score = i, score
    return best_idx if best_score >= threshold else None


def _esc(text):
    """Minimal HTML escaping for content rendered inside styled divs."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


# ----------------------------------------------------------------------------
# Step renderers
# ----------------------------------------------------------------------------
def _step_case(result, fmap):
    st.markdown(
        "This is a guided playback. Instead of reading a finished report, "
        "you will watch the Layered Thinking Framework move from what is "
        "visible to what is structural, one layer at a time."
    )
    classification = result.get("classification", "")
    st.markdown(
        f'<div class="pb-card"><span class="pb-tag">Classification</span>'
        f"<div>{_esc(classification)}</div></div>",
        unsafe_allow_html=True,
    )


def _step_layer1(result, fmap):
    st.subheader(fmap["layer1_title"])
    st.caption(fmap["layer1_lead"])
    items = result.get(fmap["layer1_key"], []) or []
    for i, item in enumerate(items):
        st.markdown(
            f'<div class="pb-card"><span class="pb-tag">'
            f'{fmap["tag_prefix"]}{i + 1}</span>'
            f"<div>{_esc(item)}</div></div>",
            unsafe_allow_html=True,
        )


def _step_predict(result, fmap):
    st.subheader("Pause: what is your read?")
    st.markdown(
        "Before the next layer opens, name what you think is actually "
        "driving these. One or two sentences. Most first reads land on a "
        "surface cause. The next two layers test that instinct."
    )
    st.text_area(
        "Your read",
        key="pb_prediction_input",
        value=st.session_state.get("pb_prediction", ""),
        placeholder="What do you think is underneath this?",
        label_visibility="collapsed",
        height=100,
    )
    st.caption("Optional. You can continue without writing anything.")


def _step_layer2(result, fmap):
    st.subheader(fmap["layer2_title"])
    st.caption(fmap["layer2_lead"])
    layer1_items = result.get(fmap["layer1_key"], []) or []
    causes = result.get(fmap["layer2_key"], []) or []
    prefix = fmap["tag_prefix"]
    for i, entry in enumerate(causes):
        if not isinstance(entry, dict):
            entry = {fmap["layer2_item_key"]: str(entry)}
        cause = entry.get(fmap["layer2_item_key"], "")
        links = entry.get(fmap["layer2_links_key"], []) or []
        chips = []
        for link in links:
            idx = _match_layer1(link, layer1_items)
            if idx is not None:
                chips.append(
                    f'<span class="pb-chip pb-chip-hot">'
                    f"{prefix}{idx + 1}</span>"
                )
            else:
                chips.append(f'<span class="pb-chip">{_esc(link)}</span>')
        chips_html = "".join(chips)
        st.markdown(
            f'<div class="pb-card"><span class="pb-tag">Cause {i + 1}</span>'
            f"<div>{_esc(cause)}</div>"
            f'<div class="pb-addresses">{fmap["links_label"]}: '
            f"{chips_html}</div></div>",
            unsafe_allow_html=True,
        )
    st.caption(
        f"Numbered chips point back to the Layer 1 items above. A cause "
        f"that explains nothing is not a cause."
    )


def _step_layer3(result, fmap):
    st.subheader("Layer 3: Structural conditions")
    st.caption(
        "The conditions that let the causes keep emerging. This is where "
        "the diagnosis actually lives."
    )
    items = result.get("layer_3_structural", []) or []
    for i, item in enumerate(items):
        st.markdown(
            f'<div class="pb-card pb-card-structural">'
            f'<span class="pb-tag">Structural {i + 1}</span>'
            f"<div>{_esc(item)}</div></div>",
            unsafe_allow_html=True,
        )
    prediction = st.session_state.get("pb_prediction", "")
    if prediction:
        st.markdown("**Your early read**")
        st.markdown(
            f'<div class="pb-quote">{_esc(prediction)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            "Compare your read against the layers above. Did it land on a "
            "Layer 2 cause, or did it reach the structure?"
        )


def _step_actions(result, fmap):
    st.subheader("Recommended actions")
    st.caption("Every action names what it addresses. Nothing free-floating.")
    actions = result.get("recommended_actions", []) or []
    for i, entry in enumerate(actions):
        if not isinstance(entry, dict):
            entry = {"action": str(entry), "addresses": ""}
        action = entry.get("action", "")
        addresses = entry.get("addresses", "")
        addresses_html = (
            f'<div class="pb-addresses">Addresses: {_esc(addresses)}</div>'
            if addresses
            else ""
        )
        st.markdown(
            f'<div class="pb-card pb-card-action">'
            f'<span class="pb-tag">Action {i + 1}</span>'
            f"<div>{_esc(action)}</div>{addresses_html}</div>",
            unsafe_allow_html=True,
        )


def _step_plan_proof(result, fmap):
    st.subheader("The plan, and how you will know it is working")
    phases = result.get("action_plan", []) or []
    for entry in phases:
        if not isinstance(entry, dict):
            continue
        phase = entry.get("phase", "")
        focus = entry.get("focus", "")
        with st.expander(f"{phase}: {focus}", expanded=(phase == "Discovery")):
            for action in entry.get("actions", []) or []:
                st.markdown(f"- {action}")

    kpis = result.get("kpis", []) or []
    if kpis:
        st.markdown("**KPIs that validate the diagnosis**")
        rows = ["| KPI | Direction | Type | Target |", "| --- | --- | --- | --- |"]
        for entry in kpis:
            if not isinstance(entry, dict):
                continue
            glyph = _DIRECTION_GLYPHS.get(entry.get("direction", ""), "")
            rows.append(
                f"| {entry.get('kpi', '')} "
                f"| {glyph} {entry.get('direction', '')} "
                f"| {entry.get('type', '')} "
                f"| {entry.get('target_or_threshold', '')} |"
            )
        st.markdown("\n".join(rows))

    assumptions = result.get("assumptions_to_test", []) or []
    if assumptions:
        st.markdown("**Assumptions to test before acting**")
        for item in assumptions:
            st.markdown(f"- {item}")


def _step_summary(result, fmap):
    st.subheader("Executive summary")
    summary = result.get("executive_summary", "")
    st.markdown(
        f'<div class="pb-card"><div>{_esc(summary)}</div></div>',
        unsafe_allow_html=True,
    )
    scratchpad = result.get("scratchpad_reasoning", "")
    if scratchpad:
        st.markdown('<div style="height: 8px;"></div>', unsafe_allow_html=True)
        with st.expander("Show the agent's working notes"):
            st.caption(
                "The private reasoning the agent worked through before "
                "committing to the structured diagnosis."
            )
            st.markdown(scratchpad)
    st.markdown('<div style="height: 16px;"></div>', unsafe_allow_html=True)


_STEP_RENDERERS = [
    _step_case,
    _step_layer1,
    _step_predict,
    _step_layer2,
    _step_layer3,
    _step_actions,
    _step_plan_proof,
    _step_summary,
]


# ----------------------------------------------------------------------------
# Public entry point
# ----------------------------------------------------------------------------
def render_playback(result, mode="operations"):
    """Render the guided playback for a diagnosis result dict.

    result: the parsed JSON dict returned by run_ops_diagnosis or
            run_project_diagnosis.
    mode:   "operations" or "project".
    """
    fmap = FIELDS.get(mode, FIELDS["operations"])
    st.markdown(_CSS, unsafe_allow_html=True)

    step = st.session_state.setdefault("pb_step", 0)
    total = len(STEP_TITLES)

    st.progress((step + 1) / total)
    st.caption(f"Step {step + 1} of {total}: {STEP_TITLES[step]}")

    _STEP_RENDERERS[step](result, fmap)

    st.markdown('<div style="height: 8px;"></div>', unsafe_allow_html=True)
    st.divider()
    col_back, col_mid, col_next = st.columns([1, 2, 1])
    with col_back:
        st.button(
            "Back",
            key="pb_back",
            on_click=_go,
            args=(-1,),
            disabled=(step == 0),
            use_container_width=True,
        )
    with col_mid:
        if step < total - 1:
            st.button(
                "Skip to summary",
                key="pb_skip",
                on_click=_jump_to_end,
                use_container_width=True,
            )
        else:
            st.button(
                "Restart playback",
                key="pb_restart",
                on_click=reset_playback,
                use_container_width=True,
            )
    with col_next:
        st.button(
            "Next",
            key="pb_next",
            on_click=_go,
            args=(1,),
            disabled=(step == total - 1),
            type="primary",
            use_container_width=True,
        )
