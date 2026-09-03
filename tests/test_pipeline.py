import asyncio

from src.models import Prospect
from src.pipeline import SDRPipeline
from src.settings import Settings


def _prospect() -> Prospect:
    return Prospect(
        prospect_name="Asha",
        company="Example Co",
        role="Operations Lead",
        product="AI workflow automation",
        pain_point="manual reporting",
        value_proposition="reduce repetitive work",
        call_to_action="a 15-minute call",
        sender_name="Kaushik",
    )


def test_demo_pipeline_returns_three_candidates():
    pipeline = SDRPipeline(Settings(demo_mode=True))
    result = asyncio.run(pipeline.generate(_prospect()))
    assert len(result.candidates) == 3
    assert result.winner in result.candidates
    assert result.winner.subject
    assert result.winner.body
    assert {draft.agent_name for draft in result.candidates} == {
        "Professional SDR",
        "Consultative SDR",
        "Creative SDR",
    }


def test_demo_is_zero_api_and_labels_candidates():
    pipeline = SDRPipeline(Settings(demo_mode=True))
    result = asyncio.run(pipeline.generate(_prospect()))
    assert all(draft.provider == "Demo" for draft in result.candidates)
    assert result.manager_provider == "Demo"


def test_email_sender_is_dry_run_by_default():
    pipeline = SDRPipeline(Settings(demo_mode=True, allow_email_send=False))
    status = pipeline.email_sender.send("person@example.com", "Hello", "Body")
    assert status.startswith("DRY RUN")


def test_live_mode_requires_both_provider_keys():
    settings = Settings(demo_mode=False, gemini_api_key="", groq_api_key="")
    try:
        settings.validate_live_models()
    except RuntimeError as exc:
        assert "GEMINI_API_KEY" in str(exc)
        assert "GROQ_API_KEY" in str(exc)
    else:
        raise AssertionError("Live mode should reject missing provider keys")
