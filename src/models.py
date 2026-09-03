from __future__ import annotations
from dataclasses import dataclass


@dataclass(slots=True)
class Prospect:
    prospect_name: str
    company: str
    role: str
    product: str
    pain_point: str
    value_proposition: str
    call_to_action: str
    sender_name: str
    recipient_email: str = ""


@dataclass(slots=True)
class EmailDraft:
    agent_name: str
    subject: str
    body: str
    provider: str = ""


@dataclass(slots=True)
class PipelineResult:
    candidates: list[EmailDraft]
    winner: EmailDraft
    rationale: str
    manager_provider: str = ""
