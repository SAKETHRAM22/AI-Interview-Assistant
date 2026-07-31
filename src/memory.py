from langchain_core.chat_history import InMemoryChatMessageHistory

# Dictionary to store chat history for each session
store = {}


def get_session_history(session_id: str):
    """
    Returns chat history for a given session.
    If the session doesn't exist, create it.
    """

    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()

    return store[session_id]


def clear_session_history(session_id: str) -> None:
    """Remove one conversation without affecting other active sessions."""
    store.pop(session_id, None)
