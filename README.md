# AI Operations Diagnosis Agent

A browser-based AI agent that helps operations leaders turn messy business problems into structured root-cause analysis.

This project uses **Python**, **Streamlit**, and the **OpenAI Agents SDK** to analyze operational issues through a layered diagnosis framework focused on visibility, root causes, system design, and action planning.

---

## Project Purpose

Many operational problems show up as missed SLAs, backlog growth, customer escalations, unclear ownership, or repeated handoff failures.

The purpose of this app is to demonstrate how AI can support operations leaders by creating structure around those problems instead of producing generic advice.

The agent helps translate an operational issue into:

- Visible symptoms
- Likely root causes
- Structural or system issues
- Recommended fixes
- A 7-day action plan
- KPIs or signals to monitor
- An executive summary

---

## App Screenshots

### Input Screen

![AI Operations Diagnosis Agent input screen](screenshots/app-input.png)

### Diagnosis Output

![AI Operations Diagnosis Agent diagnosis output](screenshots/app-output.png)

---

## What the App Does

The user enters:

- An operational problem statement
- Industry or business context
- Urgency level
- Team size or volume context

The app then runs a two-step AI workflow:

1. **Issue Classification Tool**  
	A function/tool classifies the operational issue before diagnosis.

2. **Operations Diagnosis Agent**  
	An OpenAI Agents SDK workflow generates a structured diagnosis using the Layered Thinking framework.

---

## Diagnosis Framework

The output is organized into the following sections:

### Layer 1: Visible Symptoms

What is showing up on the surface, such as missed SLAs, delays, complaints, rework, or backlog growth.

### Layer 2: Likely Root Causes

What may be driving the issue, such as unclear ownership, weak handoffs, poor prioritization, missing feedback loops, or inconsistent processes.

### Layer 3: Structural/System Issues

What in the operating system allows the issue to continue, such as undocumented workflows, limited reporting, reactive governance, or lack of escalation rules.

The app also provides:

- Recommended fixes
- A 7-day action plan
- KPIs or signals to monitor
- An executive summary

---

## Tools and Technologies

- Python
- Streamlit
- OpenAI Agents SDK
- python-dotenv
- GitHub Codespaces
- Environment-variable-based secret management

---

## Skills Demonstrated

This project demonstrates:

- AI-assisted operations diagnosis
- Agent workflow design
- Tool/function design for issue classification
- Prompt design for structured business outputs
- Workflow optimization thinking
- Root-cause analysis
- Process improvement
- Streamlit app development
- Secure API key handling with environment variables
- Portfolio-ready AI application development

---

## How to Run Locally

1. Clone the repository

```bash
git clone https://github.com/KingAdamas/ai-operations-diagnosis-agent.git
cd ai-operations-diagnosis-agent
```

2. Create and activate a Python virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Set your OpenAI API key (environment variable)

```bash
export OPENAI_API_KEY="sk-..."   # macOS/Linux
setx OPENAI_API_KEY "sk-..."     # Windows (restart shell)
```

5. Run the Streamlit app

```bash
streamlit run app.py
```

6. Open the URL shown by Streamlit (usually http://localhost:8501) and interact with the app.

---

If you need to customize agent behavior or tools, inspect the code in the repository for the Issue Classification tool and the Agents SDK workflow.

