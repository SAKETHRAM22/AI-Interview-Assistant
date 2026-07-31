from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader


def load_documents(data_path: str = "data"):
    """
    Load all PDF documents from the data directory recursively.
    """

    documents = []

    pdf_files = Path(data_path).rglob("*.pdf")

    for pdf in pdf_files:
        try:
            print(f"Loading: {pdf}")

            loader = PyPDFLoader(str(pdf))
            docs = loader.load()

            # Remove empty pages
            docs = [doc for doc in docs if doc.page_content.strip()]

            documents.extend(docs)

        except Exception as e:
            print(f"Error loading {pdf}")
            print(e)
    print(f"\nLoaded {len(documents)} pages.")

    return documents        