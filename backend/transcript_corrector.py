import os
import re


class TranscriptCorrector:
    def __init__(self):
        self.enabled = os.environ.get("TRANSCRIPT_CORRECTION_ENABLED", "true").lower() in {"1", "true", "yes"}
        self.max_chars = int(os.environ.get("TRANSCRIPT_CORRECTION_MAX_CHARS", "1200"))

    async def correct(
        self,
        raw_text: str,
        *,
        role: str = "",
        level: str = "",
        glossary=None,
        retrieved_context: str = "",
        llm_chat=None,
    ) -> str:
        raw_text = self._clean(raw_text)
        if not raw_text or not self.enabled or not llm_chat:
            return raw_text
        if len(raw_text) > self.max_chars:
            return raw_text

        glossary = [str(term).strip() for term in (glossary or []) if str(term).strip()][:50]
        context = (retrieved_context or "")[:1800]
        glossary_text = ", ".join(glossary) if glossary else "None"

        system_prompt = (
            "You repair speech-to-text transcripts for a Vietnamese technical interview. "
            "The candidate may mix Vietnamese with English technical terms. "
            "Only fix transcription errors, punctuation, capitalization, and technical terms. "
            "Do not add new meaning. Do not remove candidate meaning. "
            "If unsure, keep the original wording. Return only the corrected transcript."
        )
        user_prompt = (
            f"Role: {role}\n"
            f"Level: {level}\n"
            f"Dynamic glossary: {glossary_text}\n\n"
            f"Relevant interview context:\n{context}\n\n"
            f"Raw transcript:\n{raw_text}"
        )

        try:
            corrected = await llm_chat(
                [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                json_mode=False,
                temperature=0.0,
            )
            corrected = self._clean_llm_output(corrected)
            if self._is_safe_correction(raw_text, corrected):
                return corrected
        except Exception as error:
            print(f"Transcript correction skipped: {error}")
        return raw_text

    def _clean(self, text: str) -> str:
        return re.sub(r"\s+", " ", str(text or "")).strip()

    def _clean_llm_output(self, text: str) -> str:
        cleaned = self._clean(text)
        cleaned = re.sub(r"^```(?:text)?\s*|\s*```$", "", cleaned, flags=re.I).strip()
        for prefix in ["Corrected transcript:", "Transcript:", "Output:"]:
            if cleaned.lower().startswith(prefix.lower()):
                cleaned = cleaned[len(prefix):].strip()
        return cleaned.strip('"').strip()

    def _is_safe_correction(self, raw_text: str, corrected: str) -> bool:
        if not corrected:
            return False
        raw_words = re.findall(r"\w+", raw_text, flags=re.UNICODE)
        corrected_words = re.findall(r"\w+", corrected, flags=re.UNICODE)
        if not raw_words:
            return False
        if len(corrected_words) > max(len(raw_words) * 2.2, len(raw_words) + 12):
            return False
        if len(corrected) > max(len(raw_text) * 2.5, len(raw_text) + 80):
            return False
        return True


transcript_corrector = TranscriptCorrector()
