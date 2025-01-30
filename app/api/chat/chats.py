from fastapi import APIRouter,Depends,status
from fastapi.responses import JSONResponse
from app.schemas.ChatSchemas import ChatResponse,ChatRequest
from app.services.chat_service import ChatService,get_chat_service
import redis
import requests
router = APIRouter()
redis_client=redis.Redis(host='redis',port=6379)
backend_url="http://nginx"
import json
@router.post("/")
def chat_user(chat: ChatRequest,chat_service:ChatService=Depends(get_chat_service)):
    '''
        used to chat with the ai model
    '''
    query=chat.query
    session_id=chat.session_id
    #now fetch the entire content from repo if the user is new meaning if the users session doesnt exist maybe use redis

    client_status=redis_client.get(session_id)
    file_contents=[]
    if client_status is None:
        redis_client.set(session_id,"user exists")
        print('first time')
        payload={
            "githubRepo":chat.repo_full_name,
            "githubToken":chat.github_token
        }
        summary_response=requests.post(f"{backend_url}/dir/summary", json=payload, timeout=10)
        if summary_response.status_code!=200:
            return JSONResponse(
                content={"message":"success","response":""},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        file_contents=summary_response.json()["filecontents"]
    filecontent_str=json.dumps(file_contents)
    response=chat_service.chat(query,session_id,filecontent_str)
    return JSONResponse(
        content={"message":"success", "response": response},
        status_code=status.HTTP_200_OK
    )

@router.delete("/{session_id}")
def chat_user_delete(session_id:str,chat_service:ChatService=Depends(get_chat_service)):
    '''
    used to clear the session of the user
    '''
    chat_service.clear_chat(session_id)
    redis_client.delete(session_id)
    print(session_id)
    return JSONResponse(
        content={"message":"success"},
        status_code=status.HTTP_200_OK
    )