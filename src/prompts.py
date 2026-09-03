from __future__ import annotations
from src.models import Prospect

PERSONAS = {
    "Professional SDR": (
        "Write a concise, credible B2B cold email. Be direct, respectful and specific. "
        "Avoid hype, fake statistics, urgency tricks and unsupported claims."
    ),
    "Consultative SDR": (
        "Write a thoughtful consultative outreach email. Lead with the prospect's likely "
        "business problem, show empathy, then connect the value proposition naturally."
    ),
    "Creative SDR": (
        "Write a distinctive but professional cold email with a strong opening. "
        "Keep it brief and human. Do not use gimmicks, manipulation or exaggerated claims."
    ),
}

def prospect_context(p: Prospect) -> str:
    return f"""
Prospect: {p.prospect_name}
Company: {p.company}
Role: {p.role}
Offering: {p.product}
Likely pain point: {p.pain_point}
Value proposition: {p.value_proposition}
Requested CTA: {p.call_to_action}
Sender: {p.sender_name}

Return exactly:
SUBJECT: <one subject line>
BODY:
<plain-text email body>

Constraints:
- 70 to 140 words for the body
- one clear call to action
- no invented customer names, metrics, awards or case studies
- no pressure language
- professional B2B tone
""".strip()

def manager_prompt(p: Prospect, candidates: list[str]) -> str:
    joined = "\n\n--- CANDIDATE ---\n".join(candidates)
    return f"""
You are the Sales Manager. Pick the single strongest cold outreach email for this prospect.

Evaluate:
1. relevance to {p.role} at {p.company}
2. clarity and brevity
3. credibility
4. quality of call to action
5. absence of invented claims or manipulative wording

Candidates:
{joined}

Return exactly:
WINNER: <agent name>
RATIONALE: <one or two sentences>
""".strip()
