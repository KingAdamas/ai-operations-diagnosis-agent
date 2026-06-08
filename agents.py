"""
OpenAI API calls for the diagnostic agents and the routing classifier.

Three callables:
- classify_issue(issue): routes "operations" or "project" when the user lets
  the tool decide.
- run_ops_diagnosis(inputs): runs the Operations Diagnosis Agent.
- run_project_diagnosis(inputs): runs the Project Recovery Agent.

Each returns either a parsed dict or raises with a clean error message.
"""

import json

from openai import OpenAI

from prompts import (
    CLASSIFIER_SYSTEM_PROMPT,
    OPS_SYSTEM_PROMPT,
    PROJECT_SYSTEM_PROMPT,
)
from schemas import (
    CLASSIFIER_SCHEMA,
    OPS_DIAGNOSIS_SCHEMA,
    PROJECT_DIAGNOSIS_SCHEMA,
)


MODEL = "gpt-5-mini"


def _format_user_message(inputs):
    """Convert the input dict into the user message the model sees."""
    return (
        f"Operational Issue: {inputs['issue']}\n"
        f"Industry / Context: {inputs['context']}\n"
        f"Urgency Level: {inputs['urgency']}\n"
        f"Team Size / Volume Context: {inputs.get('team_size') or 'Not specified'}\n"
        f"Stated Outcome: {inputs.get('stated_outcome') or 'Not specified'}\n"
        f"Operating Culture: {inputs.get('operating_culture') or 'Not specified'}\n"
        f"Relationship to System: {inputs.get('relationship') or 'Not specified'}"
    )


def _call_structured(system_prompt, user_message, schema, schema_name):
    """Run a structured-output call with strict JSON schema enforcement."""
    client = OpenAI()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": schema_name,
                "strict": True,
                "schema": schema,
            },
        },
    )

    message = response.choices[0].message

    if getattr(message, "refusal", None):
        return None, message.refusal

    return json.loads(message.content), None


def classify_issue(issue):
    """
    Decide whether an issue should be routed to operations or project recovery.

    Returns a dict with keys: mode, confidence, reason.
    Used only when the user picks "Let the tool decide" on the form.
    """
    data, refusal = _call_structured(
        system_prompt=CLASSIFIER_SYSTEM_PROMPT,
        user_message=f"Issue: {issue}",
        schema=CLASSIFIER_SCHEMA,
        schema_name="route_classifier",
    )
    if refusal:
        raise RuntimeError(f"Classifier refused: {refusal}")
    return data


def run_ops_diagnosis(inputs):
    """Run the Operations Diagnosis Agent and return parsed output."""
    data, refusal = _call_structured(
        system_prompt=OPS_SYSTEM_PROMPT,
        user_message=_format_user_message(inputs),
        schema=OPS_DIAGNOSIS_SCHEMA,
        schema_name="operations_diagnosis",
    )
    return data, refusal


def run_project_diagnosis(inputs):
    """Run the Project Recovery Agent and return parsed output."""
    data, refusal = _call_structured(
        system_prompt=PROJECT_SYSTEM_PROMPT,
        user_message=_format_user_message(inputs),
        schema=PROJECT_DIAGNOSIS_SCHEMA,
        schema_name="project_diagnosis",
    )
    return data, refusal
