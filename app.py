from __future__ import annotations

import asyncio
import html

import gradio as gr

from src.models import EmailDraft, Prospect
from src.pipeline import SDRPipeline
from src.settings import Settings
from styles import CSS, HEADER_HTML

settings = Settings()
pipeline = SDRPipeline(settings)


def build_prospect(
    prospect_name,
    company,
    role,
    product,
    pain_point,
    value_prop,
    cta,
    sender_name,
    recipient_email,
):
    return Prospect(
        prospect_name=(prospect_name or "").strip() or "Prospect",
        company=(company or "").strip() or "the company",
        role=(role or "").strip() or "decision maker",
        product=(product or "").strip() or "our solution",
        pain_point=(pain_point or "").strip() or "an operational challenge",
        value_proposition=(value_prop or "").strip() or "save time and improve outcomes",
        call_to_action=(cta or "").strip() or "a short 15-minute call",
        sender_name=(sender_name or "").strip() or "Kaushik",
        recipient_email=(recipient_email or "").strip(),
    )


def _badge(text: str, kind: str = "neutral") -> str:
    return f'<span class="badge badge-{kind}">{html.escape(text)}</span>'


def _draft_card(item: EmailDraft, is_winner: bool = False) -> str:
    provider_kind = (
        "gemini" if item.provider == "Gemini" else "groq" if item.provider == "Groq" else "neutral"
    )
    winner = _badge("Manager pick", "winner") if is_winner else ""
    safe_body = html.escape(item.body).replace("\n", "<br>")
    return f"""
    <article class="draft-card {'winner-card' if is_winner else ''}">
      <div class="draft-head">
        <div>
          <div class="agent-name">{html.escape(item.agent_name)}</div>
          <div class="agent-meta">{_badge(item.provider or 'Unknown', provider_kind)} {winner}</div>
        </div>
      </div>
      <div class="subject-label">SUBJECT</div>
      <div class="subject-text">{html.escape(item.subject)}</div>
      <div class="email-body">{safe_body}</div>
    </article>
    """


def _render_candidates(result) -> str:
    return '<div class="draft-stack">' + "".join(
        _draft_card(item, item is result.winner) for item in result.candidates
    ) + "</div>"


def _render_manager(result) -> str:
    provider_kind = "groq" if result.manager_provider == "Groq" else "neutral"
    return f"""
    <div class="manager-card">
      <div class="manager-eyebrow">SALES MANAGER · FINAL DECISION</div>
      <div class="manager-title">{html.escape(result.winner.agent_name)} selected</div>
      <div class="manager-badges">{_badge(result.manager_provider or 'Demo', provider_kind)} {_badge('Human review required', 'safe')}</div>
      <div class="manager-rule"></div>
      <div class="manager-label">WHY THIS WON</div>
      <div class="manager-copy">{html.escape(result.rationale)}</div>
    </div>
    """


def _activity(message: str, kind: str = "ok") -> str:
    return f'<div class="activity activity-{kind}"><span class="pulse"></span>{html.escape(message)}</div>'


def generate(
    prospect_name,
    company,
    role,
    product,
    pain_point,
    value_prop,
    cta,
    sender_name,
    recipient_email,
):
    prospect = build_prospect(
        prospect_name,
        company,
        role,
        product,
        pain_point,
        value_prop,
        cta,
        sender_name,
        recipient_email,
    )
    try:
        result = asyncio.run(pipeline.generate(prospect))
        mode = "Demo" if settings.demo_mode else "Live Gemini + Groq"
        return (
            _render_candidates(result),
            _render_manager(result),
            result.winner.subject,
            result.winner.body,
            _activity(f"Generation complete · {mode} · Manager selected {result.winner.agent_name}"),
        )
    except Exception as exc:
        return (
            _activity("No drafts rendered because generation stopped.", "error"),
            '<div class="manager-card"><div class="manager-eyebrow">WORKFLOW ERROR</div>'
            '<div class="manager-title">Generation stopped</div>'
            f'<div class="manager-copy">{html.escape(str(exc))}</div></div>',
            "",
            "",
            _activity(str(exc), "error"),
        )


def send_email(recipient_email, subject, body):
    status = pipeline.email_sender.send(
        to_email=(recipient_email or "").strip(),
        subject=(subject or "").strip(),
        body=(body or "").strip(),
    )
    kind = "ok" if status.startswith("SENT") else "safe"
    return status, _activity(status, kind)


mode_text = "LIVE AGENTS" if not settings.demo_mode else "DEMO AGENTS"
email_text = "EMAIL ENABLED" if settings.allow_email_send else "EMAIL DRY-RUN"
status_html = f"""
<div class="status-strip">
  <span class="status-chip {'live' if not settings.demo_mode else ''}">{mode_text}</span>
  <span class="status-chip gemini">GEMINI · 3.5 FLASH-LITE</span>
  <span class="status-chip groq">GROQ · GPT-OSS 20B</span>
  <span class="status-chip send">{email_text}</span>
</div>
"""

with gr.Blocks(title="SDR Agent · Outreach Intelligence Workspace") as demo:
    gr.HTML(HEADER_HTML)
    gr.HTML(status_html)

    with gr.Row(equal_height=False, elem_id="sdr-workspace"):
        with gr.Column(scale=4, min_width=300, elem_classes="workspace-panel", elem_id="brief-panel"):
            gr.HTML(
                '<div class="section-kicker">01 · OUTREACH BRIEF</div>'
                '<div class="section-heading">Define the prospect</div>'
                '<div class="section-copy">Give the agent team enough context to produce concise, specific B2B outreach.</div>'
            )
            prospect_name = gr.Textbox(label="Prospect name", value="Ananya")
            company = gr.Textbox(label="Company", value="Acme Technologies")
            role = gr.Textbox(label="Role", value="Head of Operations")
            recipient_email = gr.Textbox(label="Recipient email", placeholder="Required only when you send")
            product = gr.Textbox(label="Product / service", value="AI workflow automation")
            pain_point = gr.Textbox(label="Likely pain point", value="manual repetitive workflows")
            value_prop = gr.Textbox(
                label="Value proposition",
                value="reduce repetitive work and help teams respond faster",
                lines=2,
            )
            cta = gr.Textbox(label="Call to action", value="a 15-minute discovery call")
            sender_name = gr.Textbox(label="Sender name", value="Kaushik")
            generate_btn = gr.Button("Run SDR team", variant="primary", elem_id="run-sdr")
            gr.HTML(
                """
                <div class="provider-map">
                  <div class="provider-row"><span>Professional SDR</span><b>Gemini</b></div>
                  <div class="provider-row"><span>Consultative SDR</span><b>Groq</b></div>
                  <div class="provider-row"><span>Creative SDR</span><b>Gemini</b></div>
                  <div class="provider-row"><span>Sales Manager</span><b>Groq</b></div>
                </div>
                """
            )

        with gr.Column(scale=6, min_width=420, elem_classes="workspace-panel", elem_id="agent-panel"):
            gr.HTML(
                '<div class="section-kicker">02 · AGENT DESK</div>'
                '<div class="section-heading">Candidate outreach</div>'
                '<div class="section-copy">Compare all three drafts. The manager-selected winner receives a highlighted border and badge.</div>'
            )
            candidate_output = gr.HTML(
                _activity("Waiting for an outreach brief. Run the SDR team to generate candidates.", "safe"),
                elem_id="candidate-output",
            )

        with gr.Column(scale=4, min_width=330, elem_classes="workspace-panel", elem_id="decision-panel"):
            gr.HTML(
                '<div class="section-kicker">03 · HUMAN GATE</div>'
                '<div class="section-heading">Manager review & send</div>'
                '<div class="section-copy">Review the selected draft, edit it if needed, then approve delivery.</div>'
            )
            manager_output = gr.HTML(
                '<div class="manager-card"><div class="manager-eyebrow">SALES MANAGER · FINAL DECISION</div>'
                '<div class="manager-title">No decision yet</div>'
                '<div class="manager-copy">Run the SDR team to compare all candidate messages.</div></div>'
            )
            with gr.Column(elem_classes="review-box"):
                gr.HTML('<div class="review-heading">Selected email</div><div class="review-copy">The winning message remains editable before anything is sent.</div>')
                subject = gr.Textbox(label="Selected subject")
                body = gr.Textbox(label="Selected body", lines=12)
                send_btn = gr.Button("Send selected email", elem_id="send-email")
                send_status = gr.Textbox(label="Email status", interactive=False, elem_id="email-status")

    activity_output = gr.HTML(
        _activity(
            "Workspace ready · Demo mode" if settings.demo_mode else "Workspace ready · Live Gemini + Groq",
            "safe" if settings.demo_mode else "ok",
        )
    )

    generate_btn.click(
        generate,
        inputs=[
            prospect_name,
            company,
            role,
            product,
            pain_point,
            value_prop,
            cta,
            sender_name,
            recipient_email,
        ],
        outputs=[candidate_output, manager_output, subject, body, activity_output],
    )
    send_btn.click(
        send_email,
        inputs=[recipient_email, subject, body],
        outputs=[send_status, activity_output],
    )

if __name__ == "__main__":
    demo.launch(css=CSS)
