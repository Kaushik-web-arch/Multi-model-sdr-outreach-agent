from __future__ import annotations

import asyncio
import re

from src.email_sender import SafeEmailSender
from src.models import EmailDraft, PipelineResult, Prospect
from src.prompts import PERSONAS, manager_prompt, prospect_context
from src.settings import Settings


class SDRPipeline:
    """Generate three outreach candidates, then let a manager select one.

    Live provider split:
    - Professional SDR -> Gemini
    - Consultative SDR -> Groq
    - Creative SDR -> Gemini
    - Sales Manager -> Groq
    """

    PROVIDER_BY_AGENT = {
        "Professional SDR": "Gemini",
        "Consultative SDR": "Groq",
        "Creative SDR": "Gemini",
    }

    def __init__(self, settings: Settings):
        self.settings = settings
        self.email_sender = SafeEmailSender(settings)

    async def generate(self, prospect: Prospect) -> PipelineResult:
        if self.settings.demo_mode:
            return self._demo_generate(prospect)
        return await self._agent_generate(prospect)

    def _demo_generate(self, p: Prospect) -> PipelineResult:
        first = EmailDraft(
            agent_name="Professional SDR",
            provider="Demo",
            subject=f"{p.company}: reducing {p.pain_point.lower()}",
            body=(
                f"Hi {p.prospect_name},\n\n"
                f"I'm reaching out because teams in roles like {p.role} often spend too much "
                f"time on {p.pain_point.lower()}. I'm working on {p.product}, focused on helping "
                f"teams {p.value_proposition.lower()} without adding unnecessary process.\n\n"
                f"If this is relevant at {p.company}, would you be open to {p.call_to_action}?\n\n"
                f"Best,\n{p.sender_name}"
            ),
        )
        second = EmailDraft(
            agent_name="Consultative SDR",
            provider="Demo",
            subject=f"Quick question about workflows at {p.company}",
            body=(
                f"Hi {p.prospect_name},\n\n"
                f"How is your team currently handling {p.pain_point.lower()}? I'm exploring this "
                f"problem through {p.product}, with the goal to {p.value_proposition.lower()}.\n\n"
                f"I thought it might be relevant to your work as {p.role}. If it's a priority for "
                f"your team, I'd be glad to learn how you handle it today and share what we're building.\n\n"
                f"Would {p.call_to_action} be useful?\n\nBest,\n{p.sender_name}"
            ),
        )
        third = EmailDraft(
            agent_name="Creative SDR",
            provider="Demo",
            subject=f"One less manual workflow for {p.company}",
            body=(
                f"Hi {p.prospect_name},\n\n"
                f"A simple question: if your team could remove one repetitive workflow this quarter, "
                f"would {p.pain_point.lower()} be on the list?\n\n"
                f"I'm building around {p.product} to help teams {p.value_proposition.lower()}. "
                f"Given your role as {p.role}, I'd value your perspective even if there's no immediate fit.\n\n"
                f"Open to {p.call_to_action}?\n\nBest,\n{p.sender_name}"
            ),
        )
        return PipelineResult(
            candidates=[first, second, third],
            winner=second,
            manager_provider="Demo",
            rationale=(
                "Demo manager selected the consultative version because it is personalized, "
                "problem-led and avoids unsupported claims."
            ),
        )

    async def _agent_generate(self, p: Prospect) -> PipelineResult:
        self.settings.validate_live_models()

        try:
            from openai import AsyncOpenAI
            from agents import (
                Agent,
                OpenAIChatCompletionsModel,
                Runner,
                set_tracing_disabled,
                trace,
            )
        except ImportError as exc:
            raise RuntimeError(
                "Real agent mode requires the 'openai-agents' package. Run 'uv sync'."
            ) from exc

        set_tracing_disabled(True)

        gemini_client = AsyncOpenAI(
            api_key=self.settings.gemini_api_key,
            base_url=self.settings.gemini_base_url,
        )
        groq_client = AsyncOpenAI(
            api_key=self.settings.groq_api_key,
            base_url=self.settings.groq_base_url,
        )
        gemini_model = OpenAIChatCompletionsModel(
            model=self.settings.gemini_model,
            openai_client=gemini_client,
        )
        groq_model = OpenAIChatCompletionsModel(
            model=self.settings.groq_model,
            openai_client=groq_client,
        )

        context = prospect_context(p)

        async def run_writer(name: str, instructions: str) -> EmailDraft:
            provider = self.PROVIDER_BY_AGENT.get(name, "Gemini")
            model = groq_model if provider == "Groq" else gemini_model
            agent = Agent(name=name, instructions=instructions, model=model)
            result = await Runner.run(agent, context)
            return self._parse_draft(name, str(result.final_output), provider)

        with trace("SDR Outreach"):
            drafts = await asyncio.gather(
                *(run_writer(name, instructions) for name, instructions in PERSONAS.items())
            )
            candidate_texts = [
                f"AGENT: {d.agent_name}\nSUBJECT: {d.subject}\nBODY:\n{d.body}"
                for d in drafts
            ]
            manager = Agent(
                name="Sales Manager",
                instructions=(
                    "Select the strongest professional B2B outreach email. "
                    "Never invent facts and never rewrite the candidates. "
                    "Return exactly two fields: WINNER and RATIONALE."
                ),
                model=groq_model,
            )
            decision = await Runner.run(manager, manager_prompt(p, candidate_texts))

        winner_name, rationale = self._parse_manager(str(decision.final_output))
        winner = next(
            (draft for draft in drafts if draft.agent_name.lower() == winner_name.lower()),
            drafts[0],
        )
        return PipelineResult(
            candidates=drafts,
            winner=winner,
            rationale=rationale,
            manager_provider="Groq",
        )

    @staticmethod
    def _parse_draft(agent_name: str, text: str, provider: str = "") -> EmailDraft:
        subject_match = re.search(r"^SUBJECT:\s*(.+)$", text, flags=re.I | re.M)
        body_match = re.search(r"^BODY:\s*(.*)$", text, flags=re.I | re.M | re.S)
        subject = (
            subject_match.group(1).strip()
            if subject_match
            else f"Quick question from {agent_name}"
        )
        body = body_match.group(1).strip() if body_match else text.strip()
        return EmailDraft(
            agent_name=agent_name,
            subject=subject,
            body=body,
            provider=provider,
        )

    @staticmethod
    def _parse_manager(text: str) -> tuple[str, str]:
        winner = re.search(r"WINNER:\s*(.+)", text, flags=re.I)
        rationale = re.search(r"RATIONALE:\s*(.+)", text, flags=re.I | re.S)
        return (
            winner.group(1).strip() if winner else "Professional SDR",
            rationale.group(1).strip()
            if rationale
            else "Selected by the sales-manager agent.",
        )
