from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def get_prompt():

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an expert AI Interview Assistant.

Your job is to answer interview questions accurately using ONLY the retrieved context.

Instructions:
- Use the retrieved context whenever possible.
- If the answer is not available in the context, clearly say:
"I don't have enough information in the provided documents."
- Keep answers concise and interview-focused.
- If asked for examples, provide simple interview-relevant examples.
"""
            ),

            MessagesPlaceholder(variable_name="chat_history"),

            (
                "human",
                """
Context:
{context}

Question:
{question}
"""
            ),
        ]
    )

    return prompt