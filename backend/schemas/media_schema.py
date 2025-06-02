from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MediaBaseShowSchema(BaseModel):
    id: int
    pet_id: int | None = None
    user_id: int | None = None
    original_filename: str
    stored_filename: str
    file_path: str
    category: str
    subcategory: str | None = None
    label: str | None = None
    mime_type: str | None = None
    file_size: int | None = None
    file_hash: str | None = None
    uploaded_at: datetime
    is_active: bool = True

    class Config:
        orm_mode = True


class MediaBaseAddSchema(BaseModel):
    original_filename: str
    stored_filename: str
    file_path: str
    category: str
    subcategory: Optional[str] = None
    label: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    file_hash: Optional[str] = None

    class Config:
        orm_mode = True


class MediaBaseEditSchema(BaseModel):
    original_filename: Optional[str] = None
    stored_filename: Optional[str] = None
    file_path: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    label: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    file_hash: Optional[str] = None
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True