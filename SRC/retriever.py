from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer, CrossEncoder


PROJECT_ROOT = Path(__file__).resolve().parents[1]

CHROMA_DIR = (
    PROJECT_ROOT
    / "DATA"
    / "CHROMA_DB"
)

EMBEDDING_MODEL_NAME = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

RERANKER_MODEL_NAME = (
    "cross-encoder/ms-marco-MiniLM-L6-v2"
)


print("Loading embedding model...")

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL_NAME
)


print("Loading reranker model...")

reranker = CrossEncoder(
    RERANKER_MODEL_NAME
)


client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_collection(
    "thinkpad_knowledge"
)


def retrieve(
    query: str,
    top_k: int = 3,
    candidate_k: int = 8
):

    # STEP 1:
    # Convert question into an embedding
    query_embedding = embedding_model.encode(
        query
    ).tolist()

    # STEP 2:
    # Retrieve more candidates than we ultimately need
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=candidate_k
    )

    candidates = []

    for i in range(
        len(results["documents"][0])
    ):

        candidates.append({
            "text": results["documents"][0][i],
            "document": (
                results["metadatas"][0][i][
                    "document"
                ]
            ),
            "page": (
                results["metadatas"][0][i][
                    "page"
                ]
            ),
            "distance": (
                results["distances"][0][i]
            )
        })

    # STEP 3:
    # Build query-document pairs
    pairs = [
        (
            query,
            candidate["text"]
        )
        for candidate in candidates
    ]

    # STEP 4:
    # CrossEncoder gives each pair a relevance score
    rerank_scores = reranker.predict(
        pairs
    )

    # STEP 5:
    # Attach reranking score
    for candidate, score in zip(
        candidates,
        rerank_scores
    ):
        candidate["rerank_score"] = float(
            score
        )

    # STEP 6:
    # Highest CrossEncoder score comes first
    candidates.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    # STEP 7:
    # Return only final top-k
    return candidates[:top_k]