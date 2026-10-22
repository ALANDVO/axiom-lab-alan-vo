from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.database import init_db
from app.api import dictionary


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dictionary.router)


@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.app_name, "version": "1.0.0"}


@app.get("/")
def root():
    return {
        "name": "freehire",
        "description": "Open-source search engine for job seekers",
        "version": "1.0.0",
        "author": "Alan Vo",
        "email": "alanvo@gmail.com",
    }