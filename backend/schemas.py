from pydantic import BaseModel


class ItemCreate(BaseModel):
    title: str
    description: str | None = None
    category: str | None = None
    status: str = "lost"
    location: str | None = None
    contact_info: str | None = None
