# Multi-Model SDR Outreach Agent

A focused agentic AI mini project that explores how multiple LLMs can work together inside an automated sales outreach workflow.

## Why I Built This

ChatGPT or Gemini can already write a sales email from a prompt. The point of this project was not just email generation, but to explore what happens around the generation itself:

- multiple AI agents creating different outreach approaches
- Gemini and Groq working in the same application
- a manager agent comparing the drafts
- human review before the final action
- sending the selected email through Gmail

The goal was to understand how LLMs can become part of a structured software workflow instead of being used only as standalone chatbots.

## Why Not Just Use ChatGPT?

If I only wanted one email, using ChatGPT directly would be simpler. This project explores orchestration:

```text
Prospect brief
      ↓
Multiple SDR agents
      ↓
Manager agent evaluates drafts
      ↓
Best draft selected
      ↓
Human review
      ↓
Email delivery
```

The interesting part is that the software handles the workflow instead of the user manually generating, comparing, copying, and sending everything.

## Tech Stack

- Python
- OpenAI Agents SDK
- Gemini 3.5 Flash-Lite
- Groq / GPT-OSS
- Gradio
- Gmail SMTP
- pytest
- uv

## Run

```bash
uv sync
uv run pytest
uv run python app.py
```

Create a `.env` file from `.env.example` before using live models or email delivery.

## Future Scope

This can later be expanded with bulk prospect imports, CRM integration, approval queues, follow-up agents, campaign tracking, and analytics.
