class NonResumeDocumentError(ValueError):
    """Raised when uploaded content is not primarily a resume or CV."""

    code = "not_a_resume"
    safe_message = (
        "This document does not appear to be a resume. "
        "Upload a CV or resume that summarizes your experience, skills, and education."
    )
