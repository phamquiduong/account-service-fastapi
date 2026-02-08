from fastapi import FastAPI

from routers import auth_router, user_router

app = FastAPI(
    title="Account Service",
    version="1.0.0",
    summary="Account service for user management and authentication.",
    contact={"name": "Pham Qui Duong", "url": "https://phamquiduong.github.io/"},
)

# Router
app.include_router(user_router)
app.include_router(auth_router)
