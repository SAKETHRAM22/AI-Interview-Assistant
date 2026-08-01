from src.vector_store import get_vector_store

RELEVANCE_THRESHOLD = 0.55


def get_retriever(chunks=None):
    """
    Create and return a retriever.
    """

    vector_store = get_vector_store(chunks)

    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 5
        }
    )

    return retriever


def get_relevant_documents(query: str, chunks=None):
    """Return only documents with a meaningful semantic match to the query."""
    vector_store = get_vector_store(chunks)
    scored_documents = vector_store.similarity_search_with_relevance_scores(
        query,
        k=5,
    )

    return [
        document
        for document, score in scored_documents
        if score >= RELEVANCE_THRESHOLD
    ]
