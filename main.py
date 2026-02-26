from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, post
import sys


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def index() -> str:
    return "Version 0.0.1"

@app.get("/crash")
async def index() -> str:
    sys.exit(0)

app.include_router(auth.router)
app.include_router(post.router)
