from pathlib import Path
import os

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.items import router as items_router

load_dotenv()

app = FastAPI(
    title="FastAPI + React",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items_router)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/hello")
def hello(name: str = "World") -> dict[str, str]:
    return {"message": f"Hello, {name}!"}


@app.get("/api/db-test")
def test_database():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        return {"status": "error", "message": "DATABASE_URL not found"}

    try:
        with psycopg.connect(
            database_url,
            connect_timeout=10,
            sslmode="require"
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()

        return {
            "status": "success",
            "message": "Supabase database connected successfully!",
            "test_result": result[0]
        }

    except Exception as error:
        return {
            "status": "error",
            "message": str(error)
        }


FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend" / "dist"

if FRONTEND_DIR.is_dir():
    app.frontend("/", directory=FRONTEND_DIR)
