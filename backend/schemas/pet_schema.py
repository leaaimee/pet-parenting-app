
from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

from backend.schemas.media_schema import MediaBaseShowSchema





class PetBasicSchema(BaseModel):
    id: int
    name: str
    species: str
    subspecies: str | None = None
    gender: str | None = None

    class Config:
        from_attributes = True


class PetProfileShowSchema(BaseModel):
    id: int
    name: str
    birthday: date | None = None
    birth_year: int | None = None
    birth_month: int | None = None
    species: str | None = None
    subspecies: str | None = None
    gender: str | None = None
    profile_image: MediaBaseShowSchema | None = None
    profile_description: str | None = None
    created_at: datetime | None = None

    pet_data: Optional["PetDataShowSchema"]

    class Config:
        from_attributes = True



class PetProfileAddSchema(BaseModel):
    name: str
    birth_year: int | None = None
    birth_month: int | None = None
    birthday: date | None = None  # ✅ ISO format expected
    species: str | None = None
    subspecies: str | None = None
    gender: str | None = None
    # profile_image: str | None = Field(None, example=None)
    profile_description: str | None = None

    class Config:
        from_attributes = True
# Still useful if using models


class PetProfileEditSchema(BaseModel):
    name: str | None = None
    species: str | None = None
    subspecies: str | None = None
    gender: str | None = None
    birthday: date | None = None
    birth_year: int | None = None
    birth_month: int | None = None
    profile_image: str | None = None
    profile_description: str | None = None

    class Config:
        from_attributes = True


class PetDataShowSchema(BaseModel):
    id: int
    favorite_things: str | None = None
    dislikes: str | None = None
    social_style: str | None = None
    communication: str | None = None
    preferred_treats: str | None = None
    diet: str | None = None
    allergies: str | None = None
    medical_alerts: str | None = None
    behavior_notes: str | None = None
    additional_info: str | None = None

    class Config:
        from_attributes = True


class PetDataAddSchema(BaseModel):
    favorite_things: str | None = None
    dislikes: str | None = None
    social_style: str | None = None
    communication: str | None = None
    preferred_treats: str | None = None
    diet: str | None = None
    allergies: str | None = None
    medical_alerts: str | None = None
    behavior_notes: str | None = None
    additional_info: str | None = None

    class Config:
        from_attributes = True


class PetDataEditSchema(BaseModel):
    favorite_things: str | None = None
    dislikes: str | None = None
    social_style: str | None = None
    communication: str | None = None
    preferred_treats: str | None = None
    diet: str | None = None
    allergies: str | None = None
    medical_alerts: str | None = None
    behavior_notes: str | None = None
    additional_info: str | None = None

    class Config:
        from_attributes = True


PetProfileShowSchema.model_rebuild()

