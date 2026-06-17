"""
Strict JSON schemas for the AI Operations Diagnosis Agent.

Two diagnostic schemas (ops, project) plus a small classifier schema for routing
when the user lets the tool decide which mode to use.

Linkage fields are deliberate: every Layer 2 root cause names which Layer 1
symptoms it explains, every recommendation names which cause or structural
issue it addresses, and every KPI carries a direction and a leading/lagging
designation. This is what turns parallel lists into a connected diagnosis.

Updated to reflect the improved Layered Thinking Framework:
- layer_1_threshold_gate: the question that must be answered before descending to Layer 2
- layer_2_threshold_gate: the question that must be answered before descending to Layer 3
- layer_3_bias_check: the structural condition the analyst least wants to find, tested first
- verification: defines what Layer 1 would show if Layer 3 changed, set before intervening
"""


# ----------------------------------------------------------------------------
# Shared verification schema (used in both ops and project)
# ----------------------------------------------------------------------------
VERIFICATION_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["metric", "direction", "threshold", "counter_signal"],
    "properties": {
        "metric": {
            "type": "string",
            "description": (
                "The single Layer 1 metric that should move if the Layer 3 "
                "structural condition actually changes. Name it specifically."
            ),
        },
        "direction": {
            "type": "string",
            "enum": ["increase", "decrease", "hold"],
            "description": "The direction the metric should move.",
        },
        "threshold": {
            "type": "string",
            "description": (
                "By how much, over what window. Specific enough that a flat "
                "result cannot be rationalized as success."
            ),
        },
        "counter_signal": {
            "type": "string",
            "description": (
                "What Layer 1 would show if the structural diagnosis was wrong "
                "and a different structural condition is the real cause. "
                "This is the signal that tells you to re-diagnose."
            ),
        },
    },
}


# ----------------------------------------------------------------------------
# Operations Diagnosis Agent
# ----------------------------------------------------------------------------
OPS_DIAGNOSIS_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "scratchpad_reasoning",
        "classification",
        "layer_1_symptoms",
        "layer_1_threshold_gate",
        "layer_2_root_causes",
        "layer_2_threshold_gate",
        "layer_3_structural",
        "layer_3_bias_check",
        "recommended_actions",
        "action_plan",
        "kpis",
        "assumptions_to_test",
        "verification",
        "executive_summary",
    ],
    "properties": {
        "scratchpad_reasoning": {
            "type": "string",
            "description": (
                "Private reasoning space. Work through the diagnosis here before "
                "filling in the structured fields. This field is not shown to the "
                "user. Use it to think in layers, name the handoffs, surface the "
                "hidden value, and test the diagnosis against the stated outcome."
            ),
        },
        "classification": {
            "type": "string",
            "description": (
                "One sentence that names what kind of operational issue this is. "
                "Specific enough to anchor the diagnosis. Not just a category label."
            ),
        },
        "layer_1_symptoms": {
            "type": "array",
            "description": "3 to 5 observable surface-level symptoms.",
            "items": {"type": "string"},
        },
        "layer_1_threshold_gate": {
            "type": "string",
            "description": (
                "The gate question answered before descending to Layer 2. "
                "Confirm: are there multiple instances of this symptom, and "
                "do they share a common characteristic? State what that "
                "characteristic is. If the answer is no, the descent stops here."
            ),
        },
        "layer_2_root_causes": {
            "type": "array",
            "description": (
                "3 to 5 proximate causes. Each names which Layer 1 symptoms it "
                "explains. A root cause that explains nothing is not a root cause."
            ),
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["cause", "explains_symptoms"],
                "properties": {
                    "cause": {"type": "string"},
                    "explains_symptoms": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
            },
        },
        "layer_2_threshold_gate": {
            "type": "string",
            "description": (
                "The gate question answered before descending to Layer 3. "
                "Confirm: does the identified cause explain the full pattern "
                "or only part of it? If only part, name what is still unexplained "
                "and what additional structural condition might account for it."
            ),
        },
        "layer_3_structural": {
            "type": "array",
            "description": (
                "3 to 5 structural or system conditions that allow the root causes "
                "to keep emerging. Include scorecard design, governance gaps, "
                "absence of measurement, or absence of function where relevant."
            ),
            "items": {"type": "string"},
        },
        "layer_3_bias_check": {
            "type": "string",
            "description": (
                "The structural condition the analyst would least want to find. "
                "State it explicitly and describe what evidence was checked for "
                "or against it before committing to the Layer 3 findings above. "
                "This is the bias check. It must be answered before the structural "
                "conditions are finalized."
            ),
        },
        "recommended_actions": {
            "type": "array",
            "description": (
                "5 to 6 specific actions. Each names a meeting, metric, role, "
                "artifact, or rhythm. Each names which root cause or structural "
                "condition it addresses. Vague advice is not allowed."
            ),
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["action", "addresses"],
                "properties": {
                    "action": {"type": "string"},
                    "addresses": {"type": "string"},
                },
            },
        },
        "action_plan": {
            "type": "array",
            "description": (
                "Three phases: Discovery, Structuring, Execution. Each phase has "
                "a clear focus and 2 to 4 specific actions."
            ),
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["phase", "focus", "actions"],
                "properties": {
                    "phase": {
                        "type": "string",
                        "enum": ["Discovery", "Structuring", "Execution"],
                    },
                    "focus": {"type": "string"},
                    "actions": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
            },
        },
        "kpis": {
            "type": "array",
            "description": (
                "5 to 6 metrics. Each carries a direction and a leading/lagging "
                "designation. KPIs should validate whether the diagnosis is "
                "correct, not just measure activity."
            ),
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["kpi", "direction", "type", "target_or_threshold"],
                "properties": {
                    "kpi": {"type": "string"},
                    "direction": {
                        "type": "string",
                        "enum": ["increase", "decrease", "hold"],
                    },
                    "type": {
                        "type": "string",
                        "enum": ["leading", "lagging"],
                    },
                    "target_or_threshold": {"type": "string"},
                },
            },
        },
        "assumptions_to_test": {
            "type": "array",
            "description": (
                "3 to 5 assumptions the diagnosis is taking for granted. The "
                "user should verify these before acting."
            ),
            "items": {"type": "string"},
        },
        "verification": VERIFICATION_SCHEMA,
        "executive_summary": {
            "type": "string",
            "description": (
                "2 to 4 sentences. Names the diagnosis, the root pattern, the "
                "recommended path, and the expected outcome. Operational voice."
            ),
        },
    },
}


# ----------------------------------------------------------------------------
# Project Recovery Agent
# ----------------------------------------------------------------------------
PROJECT_DIAGNOSIS_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "scratchpad_reasoning",
        "classification",
        "layer_1_visible_risks",
        "layer_1_threshold_gate",
        "layer_2_risk_drivers",
        "layer_2_threshold_gate",
        "layer_3_structural",
        "layer_3_bias_check",
        "recommended_actions",
        "action_plan",
        "kpis",
        "assumptions_to_test",
        "verification",
        "executive_summary",
    ],
    "properties": {
        "scratchpad_reasoning": {
            "type": "string",
            "description": (
                "Private reasoning space. Work through the diagnosis here before "
                "filling in the structured fields. Not shown to the user. Reason "
                "in layers. Surface the decision cadence, the handoffs, and the "
                "structural conditions that put the project where it is."
            ),
        },
        "classification": {
            "type": "string",
            "description": (
                "One sentence that names what kind of project risk pattern this is."
            ),
        },
        "layer_1_visible_risks": {
            "type": "array",
            "description": (
                "3 to 5 observable signs the project is off track. Slipped "
                "milestones, scope drift, stakeholder concerns, confidence "
                "drops, sprint commitments missed, velocity declining, "
                "backlog growing faster than it clears."
            ),
            "items": {"type": "string"},
        },
        "layer_1_threshold_gate": {
            "type": "string",
            "description": (
                "The gate question answered before descending to Layer 2. "
                "Confirm: are there multiple delivery risks present, and do "
                "they share a common characteristic that suggests a pattern "
                "rather than isolated incidents? State what that pattern is."
            ),
        },
        "layer_2_risk_drivers": {
            "type": "array",
            "description": (
                "3 to 5 proximate drivers. Each names which Layer 1 risks it "
                "explains. Look at dependencies, decision cadence, ownership, "
                "handoffs, requirements churn, sprint planning quality, "
                "standup effectiveness, definition of done gaps, and product "
                "owner availability."
            ),
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["driver", "explains_risks"],
                "properties": {
                    "driver": {"type": "string"},
                    "explains_risks": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
            },
        },
        "layer_2_threshold_gate": {
            "type": "string",
            "description": (
                "The gate question answered before descending to Layer 3. "
                "Confirm: do the identified drivers explain the full pattern "
                "of risk or only part of it? If only part, name what remains "
                "unexplained and what structural condition might account for it."
            ),
        },
        "layer_3_structural": {
            "type": "array",
            "description": (
                "3 to 5 structural conditions enabling risk to persist on this "
                "project. Charter ambiguity, sponsor disengagement, governance "
                "cadence mismatch, escalation paths that do not work, missing "
                "decision authority, Agile maturity gaps, missing or unclear "
                "Scrum roles, ineffective ceremonies, poor estimation culture."
            ),
            "items": {"type": "string"},
        },
        "layer_3_bias_check": {
            "type": "string",
            "description": (
                "The structural condition the analyst would least want to find "
                "on this project. State it explicitly and describe what evidence "
                "was checked for or against it before committing to the Layer 3 "
                "findings above. This is the bias check."
            ),
        },
        "recommended_actions": {
            "type": "array",
            "description": (
                "5 to 6 specific recovery actions. Each names a project rhythm or "
                "artifact: standup, sprint review, retrospective, backlog grooming, "
                "status report, steering committee, RAID log, milestone gate, "
                "definition of done, decision authority. Each names which driver or "
                "structural condition it addresses."
            ),
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["action", "addresses"],
                "properties": {
                    "action": {"type": "string"},
                    "addresses": {"type": "string"},
                },
            },
        },
        "action_plan": {
            "type": "array",
            "description": (
                "Three phases tied to remaining project timeline: Discovery, "
                "Structuring, Execution. Each phase has a focus and 2 to 4 actions."
            ),
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["phase", "focus", "actions"],
                "properties": {
                    "phase": {
                        "type": "string",
                        "enum": ["Discovery", "Structuring", "Execution"],
                    },
                    "focus": {"type": "string"},
                    "actions": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
            },
        },
        "kpis": {
            "type": "array",
            "description": (
                "5 to 6 project health indicators. Schedule variance, defect "
                "closure rate, time from decision request to decision, "
                "stakeholder confidence, dependency resolution rate."
            ),
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["kpi", "direction", "type", "target_or_threshold"],
                "properties": {
                    "kpi": {"type": "string"},
                    "direction": {
                        "type": "string",
                        "enum": ["increase", "decrease", "hold"],
                    },
                    "type": {
                        "type": "string",
                        "enum": ["leading", "lagging"],
                    },
                    "target_or_threshold": {"type": "string"},
                },
            },
        },
        "assumptions_to_test": {
            "type": "array",
            "description": (
                "3 to 5 assumptions the diagnosis is taking for granted. Verify "
                "before acting."
            ),
            "items": {"type": "string"},
        },
        "verification": VERIFICATION_SCHEMA,
        "executive_summary": {
            "type": "string",
            "description": (
                "2 to 4 sentences. Names the diagnosis, the structural pattern "
                "putting the project at risk, the recovery path, and the "
                "expected outcome. Operational voice."
            ),
        },
    },
}


# ----------------------------------------------------------------------------
# Classifier (only used when the user picks "Let the tool decide")
# ----------------------------------------------------------------------------
CLASSIFIER_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["mode", "confidence", "reason"],
    "properties": {
        "mode": {
            "type": "string",
            "enum": ["operations", "project"],
        },
        "confidence": {
            "type": "string",
            "enum": ["high", "medium", "low"],
        },
        "reason": {
            "type": "string",
            "description": "One sentence explaining the routing decision.",
        },
    },
}
