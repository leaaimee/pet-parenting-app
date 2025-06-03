from datetime import datetime

from pydantic import BaseModel, EmailStr

from typing import List, Optional

from backend.schemas.media_schema import MediaBaseShowSchema



class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserProfileSchema(BaseModel):
    id: int
    email: EmailStr
    name: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserProfileShowSchema(BaseModel):
    id: int
    name: str | None = None
    pronouns: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    location: str | None = None
    birth_date: str | None = None
    profile_image: Optional[List[MediaBaseShowSchema]] = None
    profile_description: str | None = None
    languages_spoken: str | None = None
    experience_with: str | None = None
    certifications: str | None = None
    created_at: datetime | None = None


class UserProfileAddSchema(BaseModel):
    name: str | None = None
    pronouns: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    location: str | None = None
    birth_date: str | None = None
    profile_image: Optional[List[MediaBaseShowSchema]] = None
    profile_description: str | None = None
    languages_spoken: str | None = None
    experience_with: str | None = None
    certifications: str | None = None
    created_at: datetime | None = None


class UserProfileEditSchema(BaseModel):
    name: str | None = None
    pronouns: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    location: str | None = None
    birth_date: str | None = None
    profile_image: Optional[List[MediaBaseShowSchema]] = None
    profile_description: str | None = None
    languages_spoken: str | None = None
    experience_with: str | None = None
    certifications: str | None = None
    created_at: datetime | None = None


class UserProfilePublicSchema(BaseModel):
    id: int
    name: str
    profile_image: str | None = None
    profile_description: str | None = None


class TokenRequest(BaseModel):
    username: str
