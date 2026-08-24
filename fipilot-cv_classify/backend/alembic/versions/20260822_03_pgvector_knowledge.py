"""Add pgvector-backed interview knowledge chunks."""

from collections.abc import Sequence

from alembic import op

revision: str = "20260822_03"
down_revision: str | None = "20260820_02"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute(
        """
        CREATE TABLE knowledge_chunks (
            id uuid PRIMARY KEY,
            role_id varchar(100) NOT NULL,
            role_title varchar(200) NOT NULL,
            source text NOT NULL,
            chunk_index integer NOT NULL,
            content text NOT NULL,
            content_hash char(64) NOT NULL,
            embedding vector(1536) NOT NULL,
            search_vector tsvector GENERATED ALWAYS AS (
                to_tsvector('simple', coalesce(source, '') || ' ' || coalesce(content, ''))
            ) STORED,
            created_at timestamptz NOT NULL DEFAULT now(),
            updated_at timestamptz NOT NULL DEFAULT now(),
            CONSTRAINT uq_knowledge_chunk_source UNIQUE (role_id, source, chunk_index)
        )
        """
    )
    op.execute("CREATE INDEX ix_knowledge_chunks_role_id ON knowledge_chunks (role_id)")
    op.execute(
        "CREATE INDEX ix_knowledge_chunks_search_vector "
        "ON knowledge_chunks USING gin (search_vector)"
    )
    op.execute(
        "CREATE INDEX ix_knowledge_chunks_embedding_hnsw "
        "ON knowledge_chunks USING hnsw (embedding vector_cosine_ops)"
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS knowledge_chunks")
