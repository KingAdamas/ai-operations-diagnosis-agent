import os
from textwrap import dedent

import streamlit as st
from agents import Agent, Runner, function_tool
from dotenv import load_dotenv


INDUSTRY_OPTIONS = [
    "Contact Center Operations",
    "Customer Service",
    "Claims Operations",
    "Logistics / Delivery",
    "Vendor Management",
    "Healthcare Operations",
    "Fintech / Risk Operations",
    "General Business Operations",
]

URGENCY_OPTIONS = ["Low", "Medium", "High"]


load_dotenv()


@function_tool
def classify_operational_issue(problem_statement: str) -> str:
    """Classify an operations issue into a simple category for diagnosis context."""
    text = problem_statement.lower()

    if any(word in text for word in ["delay", "backlog", "sla", "queue", "throughput"]):
        return "Classification: Capacity and process flow issue"
    if any(word in text for word in ["error", "rework", "defect", "quality", "accuracy"]):
        return "Classification: Quality control issue"
    if any(word in text for word in ["churn", "escalation", "complaint", "csat", "nps"]):
        return "Classification: Customer experience issue"
    if any(word in text for word in ["fraud", "compliance", "risk", "audit", "regulatory"]):
        return "Classification: Risk and compliance issue"

    return "Classification: General operations issue"


def build_prompt(problem: str, industry: str, urgency: str, team_context: str) -> str:
    return dedent(
        f"""
        You are an operations strategy advisor.

        Diagnose the following operations problem using a layered thinking framework.

        Context:
        - Industry/Function: {industry}
        - Urgency: {urgency}
        - Team size or volume context: {team_context}
        - Problem statement: {problem}

        Return your answer in markdown with exactly these sections and short bullet points:
        ## Layer 1: Visible symptoms
        ## Layer 2: Likely root causes
        ## Layer 3: Structural/system issues
        ## Recommended fixes
        ## 7-day action plan
        ## KPIs or signals to monitor
        ## Executive summary

        Keep the response practical, specific, and beginner-friendly for an operations leader.
        """
    ).strip()


def run_diagnosis(
    problem: str, industry: str, urgency: str, team_context: str
) -> tuple[str, str]:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set.")

    classifier_agent = Agent(
        name="Operations Issue Classifier",
        instructions=(
            "Use the classify_operational_issue tool to classify the problem statement. "
            "Return only the classification result from the tool."
        ),
        model="gpt-4.1-mini",
        tools=[classify_operational_issue],
    )
    classification_result = Runner.run_sync(classifier_agent, problem)

    diagnosis_agent = Agent(
        name="AI Operations Diagnosis Agent",
        instructions=(
            "You are a clear, practical operations diagnosis assistant. "
            "Use the provided issue classification and context to produce an actionable diagnosis."
        ),
        model="gpt-4.1-mini",
    )
    diagnosis_prompt = build_prompt(problem, industry, urgency, team_context)
    diagnosis_input = (
        f"Issue pre-classification:\n{classification_result.final_output}\n\n"
        f"{diagnosis_prompt}"
    )
    diagnosis_result = Runner.run_sync(diagnosis_agent, diagnosis_input)

    classification_text = str(classification_result.final_output or "").strip()
    diagnosis_text = str(diagnosis_result.final_output or "").strip()
    return classification_text, diagnosis_text


def main() -> None:
    st.set_page_config(page_title="AI Operations Diagnosis Agent", page_icon="🛠️")

    st.title("AI Operations Diagnosis Agent")
    st.write(
        "Describe an operations problem and get a structured diagnosis using layered thinking."
    )

    problem = st.text_area(
        "Describe the operational issue",
        placeholder="Example: SLA misses increased by 22% in the last month after a new workflow launch...",
        height=180,
    )

    industry = st.selectbox("Industry / context", INDUSTRY_OPTIONS)
    urgency = st.selectbox("Urgency level", URGENCY_OPTIONS)
    team_context = st.text_input(
        "Team size or volume context",
        placeholder="Example: 35 agents, 4,000 weekly tickets",
    )

    if st.button("Run Diagnosis", type="primary"):
        if not problem.strip():
            st.warning("Please describe the operational issue before running diagnosis.")
            return

        with st.spinner("Running diagnosis..."):
            try:
                classification, diagnosis = run_diagnosis(
                    problem, industry, urgency, team_context
                )
            except Exception as error:  # noqa: BLE001
                st.error(f"Unable to run diagnosis: {error}")
                return

        st.success("Diagnosis complete")
        st.subheader("Issue classification")
        st.write(classification)
        st.subheader("Layered diagnosis")
        st.markdown(diagnosis)


if __name__ == "__main__":
    main()
