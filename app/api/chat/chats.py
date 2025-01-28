from fastapi import APIRouter,Depends,status
from fastapi.responses import JSONResponse
from app.schemas.ChatSchemas import ChatResponse,ChatRequest
from app.services.chat_service import ChatService,get_chat_service
import redis
router = APIRouter()
redis_client=redis.Redis(host='redis',port=6379)


@router.post("/")
def chat_user(chat: ChatRequest,chat_service:ChatService=Depends(get_chat_service)):
    '''
        used to chat with the ai model
    '''
    query=chat.query
    repo_full_name=chat.repo_full_name
    session_id=chat.session_id
    #now fetch the entire content from repo if the user is new meaning if the users session doesnt exist maybe use redis
    response=chat_service.chat(query,session_id)
    client_status=redis_client.get(session_id)
    if client_status is None:
        # redis_client.set(session_id,"user exists")
        print('first time')
    return JSONResponse(
        content={"id": 1, "response": response},
        status_code=status.HTTP_200_OK
    )
