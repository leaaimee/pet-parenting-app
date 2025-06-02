import mimetypes
import os

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.responses import FileResponse\

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.models.users_models import Users

from backend.services.users_service import register_user_service, show_user_profile_service, edit_user_profile_service
from backend.services.users_service import add_user_profile_image_service, login_user_service, get_user_profile_image_service

from backend.schemas.user_schema import UserProfileSchema, UserCreateSchema, UserLoginSchema, UserProfileEditSchema, UserProfileShowSchema, UserProfilePublicSchema
from backend.schemas.user_schema import TokenRequest
from backend.schemas.media_schema import MediaBaseShowSchema

from backend.auth.jwt import get_current_user, create_access_token

from backend.models.media_models import UploadedFile
from backend.database import get_db

from backend.utils.upload_helper import get_upload_subpath, VALID_SUBCATEGORIES

from werkzeug.security import check_password_hash



router = APIRouter()



@router.post("/", response_model=UserProfileSchema, status_code=201)
async def register_user_data(
    user_data: UserCreateSchema,
    session: AsyncSession = Depends(get_db)
):
    new_user = await register_user_service(user_data, session)

    return {
        "id": new_user.id,
        "email": new_user.email,
        "name": new_user.name
    }



@router.get("/users/{user_id}", response_model=UserProfilePublicSchema)
async def show_public_user_profile_data(
    user_id: int,
    session: AsyncSession = Depends(get_db)
):
    return await show_user_profile_service(user_id, session, public=True)


@router.get("/users/me", response_model=UserProfileShowSchema)
async def show_private_user_profile_data(
    session: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await show_user_profile_service(current_user["id"], session)



@router.put("/users/{user_id}/profile", response_model=UserProfileShowSchema)
async def edit_user_profile_data(
    user_id: int,
    user_data: UserProfileEditSchema,
    session: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Unauthorized to edit this profile")

    updated_user = await edit_user_profile_service(user_id, user_data, session)
    return updated_user



@router.post("/login")
async def login_user_data(
    user_data: UserLoginSchema,
    session: AsyncSession = Depends(get_db)
):
    return await login_user_service(user_data, session)



@router.post("/users/{user_id}/image", response_model=MediaBaseShowSchema)
async def add_user_profile_image_data(
    user_id: int,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Add user profile image data"""

    if current_user["id"] != user_id:
        raise HTTPException(status_code=403, detail="Access forbidden")

    uploaded_file = await add_user_profile_image_service(session, file, user_id)
    return uploaded_file



@router.get("/media/user/{subcategory}/{filename}")
async def get_user_profile_image_data(
    subcategory: str,
    filename: str
):
    return await get_user_profile_image_service(subcategory, filename)






@router.post("/token")
def get_token(data: TokenRequest):
    """Generate access token for given username (no password validation here)"""
    if not data.username.strip():
        raise HTTPException(status_code=400, detail="Missing username")

    token = create_access_token({"sub": data.username})
    return {
        "access_token": token,
        "token_type": "bearer"
    }



@router.get("/whoami")
def whoami(current_user: dict = Depends(get_current_user)):
    """Simple identity check for current user"""
    return {"message": f"Hello, {current_user['username']}"}



@router.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    """Example of a protected route that requires valid token"""
    return {"message": f"Hello, {current_user['username']}. You're in a secure zone."}





