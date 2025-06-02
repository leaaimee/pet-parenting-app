import os
import mimetypes
from fastapi.responses import FileResponse
from fastapi import HTTPException

from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from starlette.datastructures import UploadFile
from unicodedata import category
from werkzeug.security import generate_password_hash
from passlib.hash import bcrypt

from backend.utils.upload_helper import get_upload_subpath, VALID_SUBCATEGORIES

from backend.models.users_models import Users

from backend.schemas.user_schema import UserCreateSchema, UserProfileEditSchema, UserLoginSchema

from backend.utils.upload_helper import save_uploaded_file

from backend.models.media_models import UploadedFile



async def register_user_service(user_data: UserCreateSchema, session: AsyncSession):
    try:
        # Check if user already exists
        result = await session.execute(select(Users).where(Users.email == user_data.email))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = bcrypt.hash(user_data.password)

        new_user = Users(
            name=user_data.name,
            email=user_data.email,
            password_hash=hashed_password
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"User creation failed: {str(e)}")



async def login_user_service(user_data: UserLoginSchema, session: AsyncSession):
    """Authenticate user and return access token placeholder"""
    result = await session.execute(
        select(Users).where(Users.email == user_data.email)
    )
    user = result.scalar_one_or_none()

    if not user or not bcrypt.verify(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {"access_token": "FAKE-TOKEN-FOR-NOW", "token_type": "bearer"}



async def get_user_profile_image_service(subcategory: str, filename: str) -> FileResponse:
    if subcategory not in VALID_SUBCATEGORIES["user"]:
        raise HTTPException(status_code=400, detail="Invalid user image subcategory")

    file_path = os.path.join(get_upload_subpath("user", subcategory), filename)

    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    media_type, _ = mimetypes.guess_type(file_path)

    return FileResponse(
        path=file_path,
        media_type=media_type or "application/octet-stream",
        filename=filename
    )



async def add_user_profile_image_service(
    session: AsyncSession,
    file: UploadFile,
    user_id: int,
) -> UploadedFile:
    """Add user profile image data"""

    file_info = await save_uploaded_file(file, category="user", subcategory="profile_image")
    file_hash: str = file_info["file_hash"]

    existing = await session.execute(
        select(UploadedFile).where(UploadedFile.file_hash == file_hash)
    )
    existing_file = existing.scalar_one_or_none()

    if existing_file:
        if existing_file.user_id != user_id:
            existing_file.user_id = user_id
            await session.commit()
        return existing_file

    new_file = UploadedFile(
        **file_info,
        user_id=user_id,
        upload_time=datetime.utcnow()
    )
    session.add(new_file)
    await session.commit()
    await session.refresh(new_file)

    return new_file



async def show_user_profile_service(user_id: int, session: AsyncSession, public: bool = False):
    try:
        result = await session.execute(select(Users).where(Users.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if public:
            visible_fields = user.public_fields or []
            return {field: getattr(user, field, None) for field in visible_fields}

        return user  # full object for private use

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")



async def edit_user_profile_service(
    user_id: int,
    user_data: UserProfileEditSchema,
    session: AsyncSession
):
    try:
        result = await session.execute(select(Users).where(Users.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        for field, value in user_data.dict(exclude_unset=True).items():
            setattr(user, field, value)

        await session.commit()
        await session.refresh(user)

        return user

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update user: {str(e)}")




