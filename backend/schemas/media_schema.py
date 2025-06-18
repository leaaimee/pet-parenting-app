from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator, field_serializer

from backend.utils.upload_helper import VALID_SUBCATEGORIES
from backend.utils.settings import MEDIA_BASE_URL


# === Base Shared Fields ===
class UploadBase(BaseModel):
    original_filename: str
    stored_filename: str
    file_path: str
    file_hash: str
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    is_active: bool = True


# === ADD Schemas ===
class ProfileUploadAddSchema(UploadBase):
    user_id: Optional[int] = None
    pet_id: Optional[int] = None
    subcategory: str

    @field_validator("subcategory")
    @classmethod
    def check_subcat(cls, v):
        if v not in VALID_SUBCATEGORIES["user"] + VALID_SUBCATEGORIES["pet"]:
            raise ValueError(f"Invalid subcategory: {v}")
        return v


class MedicalUploadAddSchema(UploadBase):
    medical_profile_id: Optional[int] = None
    vet_visit_id: Optional[int] = None
    document_type: str


# === EDIT Schemas ===
class ProfileUploadEditSchema(BaseModel):
    is_active: Optional[bool] = None
    subcategory: Optional[str] = None


class MedicalUploadEditSchema(BaseModel):
    is_active: Optional[bool] = None
    document_type: Optional[str] = None


# === SHOW Schemas ===
class ProfileUploadShowSchema(UploadBase):
    id: int
    subcategory: str
    user_id: Optional[int]
    pet_id: Optional[int]
    uploaded_at: datetime
    url: str

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("url", mode="plain")
    def generate_url(self, url: str, info):
        return f"{MEDIA_BASE_URL}/user/{self.subcategory}/{self.stored_filename}"


class MedicalUploadShowSchema(UploadBase):
    id: int
    document_type: str
    medical_profile_id: Optional[int]
    vet_visit_id: Optional[int]
    uploaded_at: datetime
    url: str

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("url", mode="plain")
    def generate_url(self, url: str, info):
        return f"{MEDIA_BASE_URL}/medical/{self.document_type}/{self.stored_filename}"
