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

## Demo mode and live mode

This is a **multi-model text workflow**, not a multimodal image/audio application.

| Mode | Behavior |
| --- | --- |
| Demo (default) | Builds three predefined email templates without API requests and always selects the consultative draft. |
| Live | Runs three writing agents concurrently: Professional and Creative use Gemini; Consultative uses Groq. A Groq manager selects a candidate. |
| Delivery (disabled by default) | A separate UI action sends the edited draft through SMTP only when sending is enabled and credentials are configured. |

The implementation is in [src/pipeline.py](src/pipeline.py), configuration in [src/settings.py](src/settings.py), and delivery in [src/email_sender.py](src/email_sender.py). If the manager's selection is not recognized, the pipeline falls back to the first draft; selection is not a measured quality guarantee.

### Configuration and verification

Copy `.env.example` to `.env`. Keep `DEMO_MODE=true` and `ALLOW_EMAIL_SEND=false` for the initial walkthrough. Enter a fictional prospect, generate drafts, inspect their Demo labels and edit the selected draft.

For live generation, set `DEMO_MODE=false` and configure both `GEMINI_API_KEY` and `GROQ_API_KEY`. Model names are configurable through `GEMINI_MODEL` and `GROQ_MODEL`; access must be verified with the provider. Keep sending disabled while checking generation.

Delivery requires `ALLOW_EMAIL_SEND=true`, `SMTP_USER` and `SMTP_PASSWORD`; `SMTP_HOST`, `SMTP_PORT` and `SMTP_FROM` control the destination server and sender configuration. Enabling delivery can send real email. Use an address you control for an explicit delivery test.

The current tests cover demo output, dry-run behavior and missing live credentials. They do not prove successful live generation, email delivery or improved response rates. Record those results separately with the commit, configuration (without secrets), date and observed outcome.

