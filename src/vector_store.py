import os

from langchain_chroma import Chroma

from src.config import CHROMA_DB_PATH
from src.embeddings import get_embedding_model


def create_vector_store(chunks):
    """
    Create and persist a Chroma vector database.
    """

    embeddings = get_embedding_model()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_PATH,
    )

    print(f"Vector database created successfully!")
    print(f"Stored {len(chunks)} chunks.")

    return vector_store


def load_vector_store():
    """
    Load an existing Chroma vector database.
    """

    embeddings = get_embedding_model()

    vector_store = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings,
    )

    print("Existing vector database loaded.")

    return vector_store


def get_vector_store(chunks=None):
    """
    Return an existing vector database if available,
    otherwise create a new one.
    """

    if os.path.exists(CHROMA_DB_PATH):
        return load_vector_store()

    if chunks is None:
        raise ValueError("Chunks are required to create a new vector database.")

    return create_vector_store(chunks)