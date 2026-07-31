from src.vector_store import get_vector_store


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