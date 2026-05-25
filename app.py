import os
from textwrap import dedent

import streamlit as st
from openai import OpenAI


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


def run_diagnosis(problem: str, industry: str, urgency: str, team_context: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    client = OpenAI(api_key=api_key)
    prompt = build_prompt(problem, industry, urgency, team_context)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a clear, practical operations diagnosis assistant.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.3,
    )

    content = response.choices[0].message.content or ""
    return content.strip()


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
                diagnosis = run_diagnosis(problem, industry, urgency, team_context)
            except Exception as error:  # noqa: BLE001
                st.error(f"Unable to run diagnosis: {error}")
                return

        st.success("Diagnosis complete")
        st.markdown(diagnosis)


if __name__ == "__main__":
    main()
