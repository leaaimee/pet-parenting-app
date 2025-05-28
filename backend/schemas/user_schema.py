from pydantic import BaseModel, EmailStr
from wtforms.validators import Optional


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


class UserEditProfileSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    birth_date: Optional[str] = None
    pronouns: Optional[str] = None
    profile_description: Optional[str] = None
    languages_spoken: Optional[str] = None
    experience_with: Optional[str] = None
    certifications: Optional[str] = None
    profile_picture: Optional[str] = None


class TokenRequest(BaseModel):
    username: str
