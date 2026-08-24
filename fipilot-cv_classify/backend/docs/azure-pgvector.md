# Azure PostgreSQL pgvector deployment

FiPilot stores embedded interview knowledge in the existing Azure Database for
PostgreSQL Flexible Server. PostgreSQL full-text ranking and cosine vector
ranking run in parallel and are fused before knowledge is sent to the question
generator.

The application continues to use packaged lexical knowledge when pgvector is
unavailable or has no matching rows.

## 1. Allow the extension on the Azure server

In the Azure portal, open the PostgreSQL Flexible Server, select **Server
parameters**, find `azure.extensions`, add `vector` without removing any
existing values, and save the deployment.

Verify from pgAdmin or another PostgreSQL client:

```sql
SHOW azure.extensions;

SELECT name, default_version, installed_version
FROM pg_available_extensions
WHERE name = 'vector';
```

Azure requires an extension to be allowlisted before `CREATE EXTENSION` can
succeed. The extension name is `vector`, even though the project is commonly
called pgvector.

Official Azure documentation:

- https://learn.microsoft.com/azure/postgresql/extensions/how-to-allow-extensions
- https://learn.microsoft.com/azure/postgresql/extensions/how-to-use-pgvector

## 2. Configure the release environment

Set these values in the backend deployment environment. Store secrets in the
Azure application configuration or Key Vault, never in a committed `.env`.

```dotenv
DATABASE_URL=postgresql+psycopg://<user>:<encoded-password>@<server>.postgres.database.azure.com:5432/<database>?sslmode=require
DATABASE_CONNECT_TIMEOUT=10
AZURE_FOUNDRY_ENDPOINT=https://<resource>.openai.azure.com
AZURE_FOUNDRY_API_KEY=<secret>
AZURE_EMBEDDING_MODEL=text-embedding-3-small
KNOWLEDGE_RETRIEVAL_BACKEND=pgvector
```

Reserved URL characters in the database password, including `@`, must be
percent-encoded in `DATABASE_URL`.

For local Docker development, `compose.yaml` uses the pgvector PostgreSQL 17
image so the same migration can run locally.

## 3. Apply the schema migration once

Run this as a release step, not on every application worker startup:

```powershell
cd fipilot-cv_classify/backend
uv sync
uv run alembic upgrade head
```

Migration `20260822_03` installs the `vector` extension and creates:

- `knowledge_chunks`
- a role filter index
- a GIN full-text index
- an HNSW cosine vector index over 1,536-dimensional embeddings

If migration reports that `vector` is not allowlisted, complete step 1 and run
the migration again.

## 4. Publish the knowledge snapshot

Test one role first:

```powershell
uv run python -m fipilot.knowledge_ingestion --role "Backend Developer"
```

Then publish all ten roles:

```powershell
uv run python -m fipilot.knowledge_ingestion --all
```

Ingestion embeds every bounded Markdown chunk before opening the replacement
transaction. A failed embedding call therefore leaves the existing role
snapshot untouched. Each successful role is replaced atomically.

Do not run `--all` as part of every backend startup. Run it as a one-off release
job whenever `Knowledge/Domains` or the embedding model changes.

## 5. Verify readiness

```sql
SELECT extname, extversion
FROM pg_extension
WHERE extname = 'vector';

SELECT role_id, count(*) AS chunks
FROM knowledge_chunks
GROUP BY role_id
ORDER BY role_id;

SELECT count(*) AS total_chunks
FROM knowledge_chunks;
```

After at least one role has rows, restart the backend with
`KNOWLEDGE_RETRIEVAL_BACKEND=pgvector`. Interview responses expose
`retrieval_sources`; pgvector results report `method` as `pgvector`,
`postgres-lexical`, or `pgvector-hybrid` internally.

## Recovery

If PostgreSQL retrieval is temporarily unavailable, interview generation falls
back to the packaged lexical retriever. To deliberately disable database
retrieval, set:

```dotenv
KNOWLEDGE_RETRIEVAL_BACKEND=local
```

Downgrading the migration removes `knowledge_chunks` but deliberately does not
drop the shared `vector` extension.
