from fastapi import FastAPI
from app.api.chat import chats
# Initialize FastAPI
app = FastAPI(
    title="FastAPI Boilerplate",
    description="A boilerplate for FastAPI projects",
    version="1.0.0"
)

# Register API routers
app.include_router(chats.router, prefix="/api/v1/chat", tags=["Chats"])
