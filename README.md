# AI Operations Diagnosis Agent

AI Operations Diagnosis Agent is a beginner-friendly Streamlit web app that helps an operations leader diagnose business/operational problems using a layered thinking framework.

## What this app does

A user enters:
- an operational problem statement,
- industry/context,
- urgency level,
- team size or volume context.

The app then generates a structured diagnosis with:
- Layer 1: Visible symptoms
- Layer 2: Likely root causes
- Layer 3: Structural/system issues
- Recommended fixes
- 7-day action plan
- KPIs or signals to monitor
- Executive summary

## How to run locally

1. **Clone the repository**
2. **Create and activate a virtual environment**
3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set your OpenAI API key in environment variables** (required)

```bash
export OPENAI_API_KEY="your_api_key_here"
```

5. **Run the Streamlit app**

```bash
streamlit run app.py
```

## Skills this portfolio project demonstrates

- AI-assisted operations diagnosis
- Prompt design for structured business outputs
- Workflow optimization and root-cause analysis mindset
- Practical Python app development with Streamlit
- Secure handling of API credentials via environment variables

## Portfolio positioning

This project is designed to showcase practical AI application for operations leadership. It demonstrates how AI can support process improvement, project management, and faster decision-making in real operational environments, rather than acting as a generic chatbot.
