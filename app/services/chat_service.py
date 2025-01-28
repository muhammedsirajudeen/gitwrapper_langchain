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
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=os.getenv("OPEN_API_KEY"))

    def get_session_history(
        self,session_id: str, config: dict = None
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
        if session_id not in store:
            store[session_id] = InMemoryChatMessageHistory()
            store[session_id].add_message(
                SystemMessage(
                    content=config.get("context")
                )
            )
        return store[session_id]


    def chat(self, query: str, session_id: str,context:str) -> str:
        """
        used to chat
        """
        chain = RunnableWithMessageHistory(
            self.llm,
            lambda session_id: self.get_session_history(
                session_id, config={"context": context}
            ),
        )
        response = chain.invoke(
            query, config={"configurable": {"session_id": session_id, "context": context}}
        )
        print(response.content)
        return response.content

    def clear_chat(self,session_id:str)->str:
        '''
        used to clear the current memory of user
        '''
        if session_id in store:
            del store[session_id]
        return "chat cleared"

def get_chat_service() -> ChatService:
    """
    DI
    """
    return ChatService()
