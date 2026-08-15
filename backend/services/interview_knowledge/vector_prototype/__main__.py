from __future__ import annotations

from services.interview_knowledge.vector_prototype.logic import (
    PrototypeState,
    initial_state,
    retrieve,
)


BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
CLEAR = "\033[2J\033[H"

SAMPLES = {
    "1": "How do you manage LangGraph agent state and session memory?",
    "2": "Tối ưu độ trễ nhận dạng giọng nói tiếng Việt như thế nào?",
    "3": "How do database transactions and bounded retries protect a FastAPI service?",
}


def render(state: PrototypeState) -> None:
    print(CLEAR, end="")
    print(f"{BOLD}FAKE VECTOR RETRIEVAL — THROWAWAY PROTOTYPE{RESET}")
    print(f"{DIM}Production FiPilot still uses lexical retrieval.{RESET}\n")
    print(f"{BOLD}embedding_model:{RESET}      {state.config.embedding_model}")
    print(f"{BOLD}output_dimensions:{RESET}    {state.config.output_dimensionality}")
    print(f"{BOLD}vector_database:{RESET}      {state.config.vector_database}")
    print(f"{BOLD}collection:{RESET}           {state.config.collection}")
    print(f"{BOLD}vector_field:{RESET}         {state.config.vector_field}")
    print(f"{BOLD}top_k:{RESET}                {state.config.top_k}")
    print(f"{BOLD}similarity_metric:{RESET}    {state.config.similarity_metric}")
    print(f"{BOLD}indexed_chunks:{RESET}       {state.indexed_chunks}")
    print(f"{BOLD}fake_dimensions:{RESET}      {state.simulated_dimensions}")
    print(f"{BOLD}query:{RESET}                {state.query or '(none)'}")
    print(f"{BOLD}fake_query_vector:{RESET}    {list(state.query_vector) or '(none)'}\n")
    print(f"{BOLD}Top-{state.config.top_k} results{RESET}")
    if not state.results:
        print(f"{DIM}Run a query to populate the ranking.{RESET}")
    for result in state.results:
        print(
            f"{result.rank}. score={result.score:.3f}  "
            f"id={result.chunk_id}  domain={result.domain}\n"
            f"   {result.text}"
        )
    print("\n[1] agent state  [2] Vietnamese speech  [3] backend reliability")
    print("[type] custom query  [q] quit")


def main() -> None:
    state = initial_state()
    while True:
        render(state)
        action = input("\nquery> ").strip()
        if action.casefold() == "q":
            return
        query = SAMPLES.get(action, action)
        if query:
            state = retrieve(state, query)


if __name__ == "__main__":
    main()
