import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import SystemMessage

load_dotenv()
OPEN_API_KEY = os.getenv("OPEN_API_KEY")
if not OPEN_API_KEY:
    raise ValueError("Please set the OPENAI_API_KEY in your .env file!")


store = {}


# way to add context
def get_session_history(
    session_id: str, config: dict = None
) -> InMemoryChatMessageHistory:
    """
    Retrieves or creates a chat message history for a given session ID.

    Args:
        session_id (str): A unique identifier for the session.

    Returns:
        InMemoryChatMessageHistory: The chat message history associated with the session ID.
                                   If the session ID does not exist, a new history is created
                                   and initialized with a system message.
    """
    print(session_id)
    if config:
        print(config.get("context"))
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
        store[session_id].add_message(
            SystemMessage(
                content="My name is muhammed sirajudeen add my name in all responses"
            )
        )
    return store[session_id]


llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPEN_API_KEY)
chain = RunnableWithMessageHistory(
    llm, lambda session_id: get_session_history(session_id, config={"context": "hey"})
)

# way to add sessions
response1 = chain.invoke(
    "hello how are you", config={"configurable": {"session_id": "1", "context": "hey"}}
)
print(response1)
# response2=chain.invoke(
#     "what did i ask you",
#     config={"configurable":{"session_id":"1"}}
# )
# print(response2)
