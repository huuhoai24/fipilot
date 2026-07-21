import re
from collections import Counter


class LightweightRAGService:
    """Small in-process retrieval helper for interview context.

    This is intentionally dependency-light so it can run on a laptop before
    moving to embeddings/pgvector/Qdrant later.
    """

    def __init__(self, max_glossary_terms: int = 40, max_context_chunks: int = 6):
        self.max_glossary_terms = max_glossary_terms
        self.max_context_chunks = max_context_chunks

    def build_session_context(self, session, template_questions=None, history=None) -> dict:
        template_questions = template_questions or []
        history = history or []

        profile_text = "\n".join(
            str(item or "")
            for item in [
                getattr(session, "candidate_name", ""),
                getattr(session, "role", ""),
                getattr(session, "level", ""),
            ]
        )
        template_chunks = self._template_chunks(template_questions)
        history_text = "\n".join(str(getattr(message, "content", "") or "") for message in history[-12:])
        query = f"{profile_text}\n{history_text}"

        retrieved_chunks = self.retrieve(query=query, chunks=template_chunks)
        glossary = self.build_glossary(
            "\n".join([profile_text, history_text, "\n".join(chunk["text"] for chunk in retrieved_chunks)])
        )

        return {
            "glossary": glossary,
            "retrieved_context": "\n\n".join(chunk["text"] for chunk in retrieved_chunks),
        }

    def retrieve(self, query: str, chunks: list[dict]) -> list[dict]:
        if not chunks:
            return []

        query_tokens = self._tokens(query)
        if not query_tokens:
            return chunks[: self.max_context_chunks]

        scored = []
        for index, chunk in enumerate(chunks):
            chunk_tokens = self._tokens(chunk.get("text", ""))
            overlap = len(query_tokens & chunk_tokens)
            tag_bonus = len(query_tokens & set(chunk.get("tags", []))) * 2
            difficulty_bonus = 0.5 if chunk.get("difficulty") else 0
            score = overlap + tag_bonus + difficulty_bonus
            scored.append((score, index, chunk))

        scored.sort(key=lambda item: (item[0], -item[1]), reverse=True)
        selected = [chunk for score, _index, chunk in scored if score > 0]
        return (selected or [chunk for _score, _index, chunk in scored])[: self.max_context_chunks]

    def build_glossary(self, text: str, extra_terms=None) -> list[str]:
        terms = []
        terms.extend(extra_terms or [])

        # Preserve multi-word English technical phrases and acronym-like terms.
        phrase_pattern = re.compile(
            r"\b(?:[A-Z][A-Za-z0-9+#.]*|[a-z]+)(?:[ ._-]+(?:[A-Z][A-Za-z0-9+#.]*|[a-z]+)){0,3}\b"
        )
        acronym_pattern = re.compile(r"\b[A-Z][A-Z0-9+#.]{1,}\b")

        for match in acronym_pattern.finditer(text or ""):
            terms.append(match.group(0).strip())

        for match in phrase_pattern.finditer(text or ""):
            value = re.sub(r"\s+", " ", match.group(0)).strip(" .,_-")
            if self._looks_like_domain_term(value):
                terms.append(value)

        canonical = {}
        counts = Counter()
        for term in terms:
            clean = self._clean_term(term)
            if not clean:
                continue
            key = clean.lower()
            canonical.setdefault(key, clean)
            counts[key] += 1

        ranked = sorted(canonical, key=lambda key: (-counts[key], key))
        return [canonical[key] for key in ranked[: self.max_glossary_terms]]

    def _template_chunks(self, template_questions: list[dict]) -> list[dict]:
        chunks = []
        for question in template_questions:
            question_text = str(question.get("question") or "")
            answer_text = str(question.get("expected_answer") or question.get("answer") or "")
            score_rule = question.get("score_rule", {}) if isinstance(question.get("score_rule"), dict) else {}
            tags = [str(tag).lower() for tag in question.get("tags", []) if str(tag).strip()]
            chunks.append(
                {
                    "text": (
                        f"Question {question.get('id')} ({question.get('topic', 'General')}): {question_text}\n"
                        f"Expected: {answer_text[:900]}\n"
                        f"Score rule: {score_rule}"
                    ).strip(),
                    "difficulty": question.get("difficulty"),
                    "tags": tags,
                }
            )
        return chunks

    def _tokens(self, text: str) -> set[str]:
        return set(re.findall(r"[a-zA-Z0-9+#.]{2,}", (text or "").lower()))

    def _clean_term(self, term: str) -> str:
        clean = re.sub(r"\s+", " ", str(term or "")).strip(" .,;:-_/")
        if len(clean) < 2 or len(clean) > 60:
            return ""
        if clean.lower() in {"the", "and", "or", "with", "for", "role", "level", "question", "rubric"}:
            return ""
        if clean.split()[0].lower() in {"ask", "based", "compare", "define", "describe", "explain", "how", "question", "tell", "what", "why"}:
            return ""
        return clean

    def _looks_like_domain_term(self, value: str) -> bool:
        clean = self._clean_term(value)
        if not clean:
            return False
        lowered = clean.lower()
        domain_markers = {
            "ai",
            "api",
            "backend",
            "cloud",
            "data",
            "database",
            "developer",
            "devops",
            "docker",
            "engineer",
            "fastapi",
            "frontend",
            "java",
            "javascript",
            "kubernetes",
            "learning",
            "llm",
            "machine",
            "python",
            "react",
            "sql",
            "testing",
            "typescript",
        }
        if any(marker in lowered.split() for marker in domain_markers):
            return True
        return bool(re.search(r"[A-Z]{2,}|[A-Za-z]+[+#.]|[A-Za-z]+[0-9]", clean))


rag_service = LightweightRAGService()
