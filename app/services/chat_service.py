import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import SystemMessage

load_dotenv()
store = {}


class ChatService:
    """
    For chatting using the langchain api's
    """

    def __init__(self):
        self.openaikey = os.getenv("OPEN_API_KEY")

    def get_session_history(self, session_id: str) -> InMemoryChatMessageHistory:
        """
        helper function to access the session
        """
        if session_id not in store:
            store[session_id] = InMemoryChatMessageHistory()
            # remember to add all context here
            store[session_id].add_message(
                SystemMessage(
                    content="My name is muhammed sirajudeen add my name in all responses"
                )
            )
        return store[session_id]

    def chat(self, query: str, session_id: str) -> str:
        """
        used to chat
        """
        return self.openaikey


def get_chat_service() -> ChatService:
    """
    DI
    """
    return ChatService()
