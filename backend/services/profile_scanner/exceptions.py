class NonResumeDocumentError(ValueError):
    """Raised when uploaded content is not primarily a resume or CV."""

    code = "not_a_resume"
    safe_message = (
        "Nền tảng hiện tại chỉ hỗ trợ phỏng vấn cho 10 ngành nghề thuộc khối Công nghệ & Kỹ thuật phần mềm "
        "(AI Engineer, Backend Developer, Business Analyst, Data Engineer, Data Scientist, "
        "DevOps Engineer, Full Stack Developer, Software Engineer, Tester/QA/QC, Web Developer). "
        "CV của bạn không thuộc các ngành được hỗ trợ hoặc không phải là một CV hợp lệ."
    )

    def __init__(self, message: str | None = None, code: str | None = None):
        super().__init__(message or self.safe_message)
        if message is not None:
            self.safe_message = message
        if code is not None:
            self.code = code


class MarginalResumeDocumentError(NonResumeDocumentError):
    """Raised when uploaded content is only marginally/slightly suitable."""

    code = "marginal_resume"

    def __init__(
        self,
        closest_domains: list[str] | None = None,
        match_percentage: int | None = None,
        message: str | None = None,
    ):
        if message is None:
            domains_str = ", ".join(closest_domains) if closest_domains else "Không xác định"
            percentage_str = f"{match_percentage}" if match_percentage is not None else "0"
            message = (
                "Rất tiếc, CV của bạn ít phù hợp với 10 ngành nghề thuộc khối Công nghệ & Kỹ thuật phần mềm hiện đang được hỗ trợ của hệ thống "
                "(AI Engineer, Backend Developer, Business Analyst, Data Engineer, Data Scientist, "
                "DevOps Engineer, Full Stack Developer, Software Engineer, Tester/QA/QC, Web Developer).\n"
                f"Hệ thống nhận định CV của bạn có thể thuộc domain: {domains_str} với mức độ phù hợp khoảng {percentage_str}%.\n"
                "Bạn có muốn tiếp tục không?"
            )
        super().__init__(message, code=self.code)
