import argparse
import difflib
import json
import os
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "Knowledge"
INDEX_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
EMBED_MODEL = os.getenv("AZURE_EMBEDDING_MODEL", "text-embedding-3-small")
MAX_TEXT_CHARS = 8000
BATCH_SIZE = 200


def _get_client() -> OpenAI:
    return OpenAI(
        api_key=os.getenv("AZURE_FOUNDRY_API_KEY"),
        base_url=os.getenv("AZURE_FOUNDRY_ENDPOINT").rstrip("/") + "/openai/v1/",
    )


def _normalize(name: str) -> str:
    return "".join(ch.lower() for ch in name if ch.isalnum())


def resolve_domain_folder(role: str) -> Path:
    candidates = sorted(
        d.name for d in (KNOWLEDGE_DIR / "Domains").iterdir() if d.is_dir()
    )
    match = difflib.get_close_matches(
        _normalize(role), [_normalize(c) for c in candidates], n=1, cutoff=0.7
    )
    if not match:
        raise ValueError(
            f"Cannot resolve role '{role}' to any Domain folder. Available: {candidates}"
        )
    return (
        KNOWLEDGE_DIR
        / "Domains"
        / candidates[[_normalize(c) for c in candidates].index(match[0])]
    )


def _embed_texts(client: OpenAI, texts: list[str]) -> list[list[float]]:
    vectors = []
    for i in range(0, len(texts), BATCH_SIZE):
        batch = [t[:MAX_TEXT_CHARS] for t in texts[i : i + BATCH_SIZE]]
        resp = client.embeddings.create(model=EMBED_MODEL, input=batch)
        vectors.extend([d.embedding for d in resp.data])
    return vectors


def _build_index(domain_dir: Path) -> Path:
    files = sorted(p for p in domain_dir.rglob("*.md") if p.is_file())
    if not files:
        raise ValueError(f"No .md files found in {domain_dir}")

    texts = []
    for f in files:
        rel_path = f.relative_to(KNOWLEDGE_DIR)
        content = f.read_text(encoding="utf-8")
        texts.append(f"{rel_path}\n{content}")

    print(f"Embedding {len(texts)} files of domain '{domain_dir.name}'...")
    vectors = _embed_texts(_get_client(), texts)
    embeddings = np.array(vectors, dtype=np.float32)
    embeddings /= np.linalg.norm(embeddings, axis=1, keepdims=True)

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    index_path = INDEX_DIR / f"domain_index_{domain_dir.name}.npz"
    np.savez_compressed(
        index_path, embeddings=embeddings, paths=np.array([str(t) for t in texts])
    )
    print(f"Index saved: {index_path}")
    return index_path


def build_index(role: str) -> Path:
    domain_dir = resolve_domain_folder(role)
    return _build_index(domain_dir)


def build_all_indexes() -> None:
    domain_dirs = sorted(
        d for d in (KNOWLEDGE_DIR / "Domains").iterdir() if d.is_dir()
    )
    for domain_dir in domain_dirs:
        try:
            _build_index(domain_dir)
        except ValueError as e:
            print(f"Skip {domain_dir.name}: {e}")


def search_domain(job_description: str, role: str, top_k: int = 5) -> list[dict]:
    domain_dir = resolve_domain_folder(role)
    index_path = INDEX_DIR / f"domain_index_{domain_dir.name}.npz"
    if not index_path.exists():
        raise FileNotFoundError(
            f'Index not found: {index_path}. Run: python fipilot/knowledge_index.py build --role "{role}"'
        )

    data = np.load(index_path, allow_pickle=False)
    embeddings = data["embeddings"]
    paths = data["paths"].astype(str)

    [query_vec] = _embed_texts(_get_client(), [job_description])
    query = np.array(query_vec, dtype=np.float32)
    query /= np.linalg.norm(query)

    scores = embeddings @ query
    top_idx = np.argsort(scores)[::-1][:top_k]
    return [{"path": paths[i], "score": round(float(scores[i]), 4)} for i in top_idx]


def main():
    parser = argparse.ArgumentParser(
        description="Build knowledge domain index and search matching files"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_build = sub.add_parser(
        "build", help="Embed all Domain files of a role and save index"
    )
    p_build.add_argument("--role", default="AI Engineer")

    sub.add_parser(
        "build-all", help="Embed every Domain folder and save one index each"
    )

    p_search = sub.add_parser(
        "search", help="Match a job description to the top-k Domain files"
    )
    p_search.add_argument("--role", default="AI Engineer")
    p_search.add_argument(
        "--desc", required=True, help="Job description text of a project"
    )
    p_search.add_argument("--top-k", type=int, default=5)

    args = parser.parse_args()
    if args.command == "build":
        build_index(args.role)
    elif args.command == "build-all":
        build_all_indexes()
    else:
        results = search_domain(args.desc, args.role, args.top_k)
        print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
