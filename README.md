# AI Operations Diagnosis Agent

A browser-based AI agent that helps operations leaders turn messy business problems into structured root-cause analysis.

This project uses **Python**, **Streamlit**, and the **OpenAI Agents SDK** to analyze operational issues through a layered diagnosis framework focused on visibility, root causes, system design, and action planning.

---

## Project Purpose

Many operational problems show up as missed SLAs, backlog growth, customer escalations, unclear ownership, or repeated handoff failures.

The purpose of this app is to demonstrate how AI can support operations leaders by creating structure around those problems instead of producing generic advice.

The agent helps translate an operational issue into:

- visible symptoms
- likely root causes
- structural/system issues
- recommended fixes
- a 7-day action plan
- KPIs or signals to monitor
- an executive summary

---

## What the App Does

The user enters:

- an operational problem statement
- industry or business context
- urgency level
- team size or volume context

The app then runs a two-step AI workflow:

1. **Issue Classification Tool**  
   A function/tool classifies the operational issue before diagnosis.

2. **Operations Diagnosis Agent**  
   An OpenAI Agents SDK workflow generates a structured diagnosis using the Layered Thinking framework.

---

## Diagnosis Framework

The output is organized into:

### Layer 1: Visible Symptoms
What is showing up on the surface, such as missed SLAs, delays, complaints, rework, or backlog growth.

### Layer 2: Likely Root Causes
What may be driving the issue, such as unclear ownership, weak handoffs, poor prioritization, missing feedback loops, or inconsistent processes.

### Layer 3: Structural/System Issues
What in the operating system allows the issue to continue, such as undocumented workflows, limited reporting, reactive governance, or lack of escalation rules.

The app then provides:

- Recommended fixes
- 7-day action plan
- KPIs or signals to monitor
- Executive summary

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

### 1. Clone the repository

```bash
git clone https://github.com/KingAdamas/ai-operations-diagnosis-agent.git
cd ai-operations-diagnosis-agent
