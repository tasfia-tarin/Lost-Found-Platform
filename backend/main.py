from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import psycopg
from dotenv import load_dotenv

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

class ItemCreate(BaseModel):
    title: str
    description: str | None = None
    category: str | None = None
    status: str = "lost"
    location: str | None = None
    contact_info: str | None = None


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


@app.post("/api/items")
def create_item(item: ItemCreate):
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise HTTPException(status_code=500, detail="Database URL not found")

    try:
        with psycopg.connect(
            database_url,
            sslmode="require"
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO public.items
                    (title, description, category, status, location, contact_info)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id, title, description, category, status,
                              location, contact_info, created_at
                    """,
                    (
                        item.title,
                        item.description,
                        item.category,
                        item.status,
                        item.location,
                        item.contact_info
                    )
                )

                new_item = cursor.fetchone()

        return {
            "message": "Item created successfully",
            "item": {
                "id": new_item[0],
                "title": new_item[1],
                "description": new_item[2],
                "category": new_item[3],
                "status": new_item[4],
                "location": new_item[5],
                "contact_info": new_item[6],
                "created_at": new_item[7]
            }
        }

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))   


@app.get("/api/items")
def get_items():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise HTTPException(status_code=500, detail="Database URL not found")

    try:
        with psycopg.connect(
            database_url,
            sslmode="require"
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, title, description, category, status,
                           location, contact_info, created_at
                    FROM public.items
                    ORDER BY created_at DESC
                    """
                )

                rows = cursor.fetchall()

        items = []

        for row in rows:
            items.append({
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "category": row[3],
                "status": row[4],
                "location": row[5],
                "contact_info": row[6],
                "created_at": row[7]
            })

        return {"items": items}

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

@app.get("/api/items/{item_id}")
def get_item(item_id: int):
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise HTTPException(status_code=500, detail="Database URL not found")

    try:
        with psycopg.connect(
            database_url,
            sslmode="require"
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, title, description, category, status,
                           location, contact_info, created_at
                    FROM public.items
                    WHERE id = %s
                    """,
                    (item_id,)
                )

                row = cursor.fetchone()

        if row is None:
            raise HTTPException(status_code=404, detail="Item not found")

        return {
            "item": {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "category": row[3],
                "status": row[4],
                "location": row[5],
                "contact_info": row[6],
                "created_at": row[7]
            }
        }

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))



@app.put("/api/items/{item_id}")
def update_item(item_id: int, item: ItemCreate):
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise HTTPException(status_code=500, detail="Database URL not found")

    try:
        with psycopg.connect(
            database_url,
            sslmode="require"
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE public.items
                    SET title = %s,
                        description = %s,
                        category = %s,
                        status = %s,
                        location = %s,
                        contact_info = %s
                    WHERE id = %s
                    RETURNING id, title, description, category, status,
                              location, contact_info, created_at
                    """,
                    (
                        item.title,
                        item.description,
                        item.category,
                        item.status,
                        item.location,
                        item.contact_info,
                        item_id
                    )
                )

                row = cursor.fetchone()

        if row is None:
            raise HTTPException(status_code=404, detail="Item not found")

        return {
            "message": "Item updated successfully",
            "item": {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "category": row[3],
                "status": row[4],
                "location": row[5],
                "contact_info": row[6],
                "created_at": row[7]
            }
        }

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))



@app.delete("/api/items/{item_id}")
def delete_item(item_id: int):
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise HTTPException(status_code=500, detail="Database URL not found")

    try:
        with psycopg.connect(
            database_url,
            sslmode="require"
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM public.items
                    WHERE id = %s
                    RETURNING id
                    """,
                    (item_id,)
                )

                deleted_item = cursor.fetchone()

        if deleted_item is None:
            raise HTTPException(status_code=404, detail="Item not found")

        return {
            "message": "Item deleted successfully",
            "deleted_item_id": deleted_item[0]
        }

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

# EXERCISE (part 1): uncomment to add POST /api/user, then test it at /docs.
# from pydantic import BaseModel, EmailStr
#
#
# class User(BaseModel):
#     id: int
#     name: str
#     email: EmailStr  # invalid emails get a 422 response automatically
#
#
# @app.post("/api/user")
# def create_user(user: User) -> dict[str, str]:
#     return {"message": f"Hello {user.name} (ID {user.id}), we'll email you at {user.email}."}


FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend" / "dist"

# dist/ only exists after `npm run build`; in dev the Vite server serves the UI.
if FRONTEND_DIR.is_dir():
    app.frontend("/", directory=FRONTEND_DIR)
