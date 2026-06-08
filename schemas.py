"""
Strict JSON schemas for the AI Operations Diagnosis Agent.

Two diagnostic schemas (ops, project) plus a small classifier schema for routing
when the user lets the tool decide which mode to use.

Linkage fields are deliberate: every Layer 2 root cause names which Layer 1
symptoms it explains, every recommendation names which cause or structural
issue it addresses, and every KPI carries a direction and a leading/lagging
designation. This is what turns parallel lists into a connected diagnosis.
"""


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
        "layer_2_root_causes",
        "layer_3_structural",
        "recommended_actions",
        "action_plan",
        "kpis",
        "assumptions_to_test",
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
        "layer_3_structural": {
            "type": "array",
            "description": (
                "3 to 5 structural or system conditions that allow the root causes "
                "to keep emerging. Include scorecard design, governance gaps, "
                "absence of measurement, or absence of function where relevant."
            ),
            "items": {"type": "string"},
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
                "user should verify these before acting. This is the bias check."
            ),
            "items": {"type": "string"},
        },
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
# Same shape as ops, with field names that map to project work and risk-spine
# framing in the layers.
PROJECT_DIAGNOSIS_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "scratchpad_reasoning",
        "classification",
        "layer_1_visible_risks",
        "layer_2_risk_drivers",
        "layer_3_structural",
        "recommended_actions",
        "action_plan",
        "kpis",
        "assumptions_to_test",
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
                "milestones, scope drift, stakeholder concerns, confidence drops."
            ),
            "items": {"type": "string"},
        },
        "layer_2_risk_drivers": {
            "type": "array",
            "description": (
                "3 to 5 proximate drivers. Each names which Layer 1 risks it "
                "explains. Look at dependencies, decision cadence, ownership, "
                "handoffs, and requirements churn."
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
        "layer_3_structural": {
            "type": "array",
            "description": (
                "3 to 5 structural conditions enabling risk to persist on this "
                "project. Charter ambiguity, sponsor disengagement, governance "
                "cadence mismatch, escalation paths that do not work, missing "
                "decision authority."
            ),
            "items": {"type": "string"},
        },
        "recommended_actions": {
            "type": "array",
            "description": (
                "5 to 6 specific recovery actions. Each names a project rhythm or "
                "artifact: standup, status report, steering committee, RAID log, "
                "milestone gate, decision authority. Each names which driver or "
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
