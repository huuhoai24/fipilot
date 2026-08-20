from services.profile_scanner.context import build_resume_context
from services.profile_scanner.verification import (
    VerificationStatus,
    verify_and_reconcile_profile,
)
from shared.schemas import CandidateProfile


def test_section_aware_context_preserves_experience_at_end_of_long_section():
    filler = "Delivered routine operational work.\n" * 900
    text = (
        "Nguyen Van A\nKỸ NĂNG\nPython, FastAPI\nKINH NGHIỆM LÀM VIỆC\n"
        + filler
        + "Senior Backend Engineer at Boundary Systems 77 | 2021 - Present\n"
        + "HỌC VẤN\nExample University"
    )

    context = build_resume_context(text, max_characters=12_000)

    assert context.is_partial
    assert context.characters_considered <= 12_000
    assert context.total_characters > context.characters_considered
    assert "Boundary Systems 77" in context.text
    assert "content_omitted" in context.warnings


def test_section_aware_context_keeps_unique_fact_amid_repeated_boilerplate():
    filler = "Repeated delivery boilerplate covering routine operations. "
    text = "EXPERIENCE\n" + filler * 400 + "Unique fact: Go and gRPC in production. " + filler * 400

    context = build_resume_context(text, max_characters=2_000)

    assert context.is_partial
    assert "Unique fact: Go and gRPC in production" in context.text
    assert "repeated boilerplate omitted" in context.text


def test_verifier_repairs_company_suffix_from_experience_section():
    text = (
        "Synthetic Candidate 05\nBackend Developer\n"
        "EXPERIENCE\nBackend Developer at Synthetic Systems 05 | 2021-01 - 2025-06\n"
        "Built reliable APIs.\nEDUCATION\nExample University"
    )
    profile = CandidateProfile(
        name="Synthetic Candidate 05",
        recent_role="Backend Developer",
        experiences=[
            {
                "company": "Synthetic Systems",
                "title": "Backend Developer",
                "description": "Built reliable APIs.",
            }
        ],
    )

    result = verify_and_reconcile_profile(profile, text)

    assert result.profile.experiences[0].company == "Synthetic Systems 05"
    record = next(item for item in result.provenance if item.field_path == "experiences[0].company")
    assert record.status is VerificationStatus.NORMALIZED_MATCH


def test_verifier_removes_identity_block_false_experience_but_keeps_uncertain_claims():
    text = (
        "Synthetic Candidate 21\nIntern Backend Developer\n"
        "EXPERIENCE\nBackend Developer at Synthetic Systems 21 | 2021 - 2025\n"
    )
    profile = CandidateProfile(
        name="Synthetic Candidate 21",
        recent_role="Intern Backend Developer",
        experiences=[
            {"company": "Synthetic Candidate 21", "title": "Intern Backend Developer"},
            {"company": "Synthetic Systems 21", "title": "Backend Developer"},
            {"company": "Synthetic Systems 21", "title": "Intern Backend Developer"},
            {"company": "Unclear Consulting", "title": "Advisor"},
        ],
    )

    result = verify_and_reconcile_profile(profile, text)

    pairs = {(item.company, item.title) for item in result.profile.experiences}
    assert ("Synthetic Candidate 21", "Intern Backend Developer") not in pairs
    assert ("Synthetic Systems 21", "Backend Developer") in pairs
    assert ("Synthetic Systems 21", "Intern Backend Developer") not in pairs
    assert ("Unclear Consulting", "Advisor") in pairs
    assert any(
        item.status is VerificationStatus.UNCERTAIN and item.value == "Unclear Consulting"
        for item in result.provenance
    )
