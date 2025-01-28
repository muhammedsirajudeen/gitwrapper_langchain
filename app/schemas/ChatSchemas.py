from pydantic import BaseModel

class ChatResponse(BaseModel):
    '''
    response model for the chat
    '''
    id:str
    response:str
class ChatRequest(BaseModel):
    '''
    request model
    '''
    query:str
    repo_full_name:str
    session_id:str