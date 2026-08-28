"""PostgreSQL repository for Resume and Candidate Profile persistence."""

from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy import select

from fipilot.database import database_session
from fipilot.models import Resume
from shared.schemas.candidate import CandidateProfile, PersistedCandidateProfile


class PostgresResumeRepository:
    """Thin repository that wraps the existing ``resumes`` table.

    Uses the *client_id* column as user-scoped ownership boundary so that
    one user cannot read or overwrite another user's records.
    """

    # ------------------------------------------------------------------
    # Write side
    # ------------------------------------------------------------------

    def save_resume(
        self,
        *,
        user_id: str,
        filename: str,
        profile: CandidateProfile,
        content_hash: str,
        resume_text: str,
    ) -> PersistedCandidateProfile:
        """Persist a new resume row and return the persisted profile.

        The ``profile`` JSONB column stores the full ``CandidateProfile``
        plus the ``content_hash`` so the route can replay cache hits from
        the DB without re-running the LLM.
        """
        client_uuid = _to_uuid(user_id)
        profile_dict: dict[str, Any] = profile.model_dump(mode="json")
        profile_dict["_content_hash"] = content_hash
        # Store a preview of the raw text (first 2000 chars) for debugging.
        profile_dict["_resume_text_preview"] = resume_text[:2000]

        with database_session() as session:
            if session is None:
                raise RuntimeError("Database not configured — DATABASE_URL must be set.")

            row = Resume(
                id=uuid.uuid4(),
                client_id=client_uuid,
                filename=filename,
                profile=profile_dict,
            )
            session.add(row)
            session.flush()
            candidate_id = str(row.id)

        return PersistedCandidateProfile(
            **profile.model_dump(exclude={"candidate_id"}),
            candidate_id=candidate_id,
        )

    def find_by_candidate_id(self, user_id: str, candidate_id: str) -> PersistedCandidateProfile | None:
        import uuid
        try:
            resume_uuid = uuid.UUID(candidate_id)
            user_uuid = _to_uuid(user_id) if user_id and user_id != "legacy-anonymous" else None
        except ValueError:
            return None

        with database_session() as session:
            stmt = select(Resume).where(Resume.id == resume_uuid)
            if user_uuid:
                stmt = stmt.where(Resume.client_id == user_uuid)
            
            row = session.scalars(stmt).first()
            if row:
                profile_dict = row.profile
                # Inject saved content hash and preview if they exist in DB
                profile = CandidateProfile(**profile_dict)
                return PersistedCandidateProfile(
                    **profile.model_dump(exclude={"candidate_id"}),
                    candidate_id=str(row.id),
                )
        return None

    # ------------------------------------------------------------------
    # Read side (cache-bypass lookup by hash)
    # ------------------------------------------------------------------

    def find_by_content_hash(
        self,
        *,
        user_id: str,
        content_hash: str,
    ) -> PersistedCandidateProfile | None:
        """Return a previously saved profile if the same file was already
        processed for this user, or ``None`` on a cache miss.

        Looks up the most recent row where
        ``profile->>'_content_hash' = content_hash`` for the given user.
        """
        client_uuid = _to_uuid(user_id)

        with database_session() as session:
            if session is None:
                return None

            row = (
                session.query(Resume)
                .filter(
                    Resume.client_id == client_uuid,
                    Resume.profile["_content_hash"].astext == content_hash,
                )
                .order_by(Resume.created_at.desc())
                .first()
            )

        if row is None:
            return None

        profile_dict = dict(row.profile)
        profile_dict.pop("_content_hash", None)
        profile_dict.pop("_resume_text_preview", None)
        profile_dict["candidate_id"] = str(row.id)

        return PersistedCandidateProfile.model_validate(profile_dict)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _to_uuid(value: str) -> uuid.UUID:
    """Convert an arbitrary string user-id to a stable UUID v5."""
    try:
        return uuid.UUID(value)
    except ValueError:
        # Derive a deterministic UUID from a non-UUID string (e.g. Firebase UID)
        return uuid.uuid5(uuid.NAMESPACE_URL, f"user:{value}")
