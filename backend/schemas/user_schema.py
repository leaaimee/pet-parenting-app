from datetime import datetime, date

from pydantic import BaseModel, EmailStr, ConfigDict


from typing import List, Optional

from backend.schemas.media_schema import MediaBaseShowSchema


class UserPublic(BaseModel):
    email: EmailStr
    id: int
    password_hash: str
    class Config:
        from_attributes = True


class UserAccountCreateSchema(BaseModel):
    email: EmailStr
    password: str


class UserAccountShowSchema(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserAccountPublicSchema(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserProfileAddSchema(BaseModel):
    name: str
    pronouns: str | None = None
    phone: str | None = None
    location: str | None = None
    birth_date: date | None = None
    profile_image: str | None = None
    profile_description: str | None = None
    languages_spoken: str | None = None
    experience_with: str | None = None
    certifications: str | None = None
    certification_files: str | None = None
    public_fields: list[str] | None = []

    class Config:
        from_attributes = True


class UserProfileEditSchema(BaseModel):
    name: str | None = None
    pronouns: str | None = None
    phone: str | None = None
    location: str | None = None
    birth_date: date | None = None
    profile_image: str | None = None
    profile_description: str | None = None
    languages_spoken: str | None = None
    experience_with: str | None = None
    certifications: str | None = None
    certification_files: str | None = None
    public_fields: list[str] | None = []

    class Config:
        from_attributes = True


class UserProfileShowSchema(BaseModel):
    id: int
    name: str
    pronouns: str | None = None
    phone: str | None = None
    location: str | None = None
    birth_date: date | None = None
    profile_image: str | None = None
    profile_description: str | None = None
    languages_spoken: str | None = None
    experience_with: str | None = None
    certifications: str | None = None
    certification_files: str | None = None
    public_fields: list[str] | None = []
    created_at: datetime | None = None


    model_config = ConfigDict(from_attributes=True)

    #class Config:
    #    from_attributes = True



class TokenRequest(BaseModel):
    username: str
    password: str


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


## Charles
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
