class NonResumeDocumentError(ValueError):
    """Raised when uploaded content is not primarily a resume or CV."""

    code = "not_a_resume"
    safe_message = (
        "Nền tảng hiện tại chỉ hỗ trợ phỏng vấn cho 10 ngành nghề thuộc khối Công nghệ & Kỹ thuật phần mềm "
        "(AI Engineer, Backend Developer, Business Analyst, Data Engineer, Data Scientist, "
        "DevOps Engineer, Full Stack Developer, Software Engineer, Tester/QA/QC, Web Developer). "
        "CV của bạn không thuộc các ngành được hỗ trợ hoặc không phải là một CV hợp lệ."
    )
