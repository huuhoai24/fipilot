import os


# Unit tests must not depend on an external Azure PostgreSQL connection.
os.environ["KNOWLEDGE_RETRIEVAL_BACKEND"] = "local"
