from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from operator import itemgetter

from src.retriever import get_retriever
from src.prompt import get_prompt
from src.largelanguagemodel import get_llm
from src.memory import get_session_history


def format_docs(docs):
    """
    Convert retrieved documents into a single string.
    """
    return "\n\n".join(doc.page_content for doc in docs)


def get_rag_chain(chunks=None):
    """
    Create and return the conversational RAG chain.
    """

    retriever = get_retriever(chunks)
    prompt = get_prompt()
    llm = get_llm()

    # ``RunnableWithMessageHistory`` adds ``chat_history`` to the input dict.
    # ``assign`` preserves that key (and ``question``) while adding the RAG
    # context.  The previous mapping rebuilt the input, discarding history and
    # passing the full input dict to the retriever.
    rag_chain = (
        RunnablePassthrough.assign(
            context=itemgetter("question") | retriever | format_docs,
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    conversation_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history",
    )

    return conversation_chain
