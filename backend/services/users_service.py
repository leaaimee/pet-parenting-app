import os
import mimetypes
from fastapi.responses import FileResponse
from fastapi import HTTPException

from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from starlette.datastructures import UploadFile

from passlib.hash import bcrypt

from backend.utils.upload_helper import get_upload_subpath, VALID_SUBCATEGORIES

from backend.models.users_models import Users, UserProfile
from backend.models.pets_models import Pets

from backend.schemas.user_schema import UserAccountCreateSchema, UserProfileEditSchema, UserLoginSchema

from backend.utils.upload_helper import save_uploaded_file

from backend.models.media_models import UploadedFile



async def register_user_service(user_data: UserAccountCreateSchema, session: AsyncSession):
    try:
        async with session.begin():
            # Check if user already exists
            result = await session.execute(
                select(Users).where(Users.email == user_data.email)
            )
            if result.scalar_one_or_none():
                raise HTTPException(status_code=400, detail="Email already registered")

            hashed_password = bcrypt.hash(user_data.password)

            new_user = Users(
                email=user_data.email,
                password_hash=hashed_password
            )
            session.add(new_user)
            await session.flush()  # gives us new_user.id without full commit

            # Optional: create an empty profile during registration
            # new_profile = UserProfile(
            #     user_id=new_user.id,
            #     name="",
            #     public_fields=[],
            # )
            # session.add(new_profile)

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



async def edit_user_profile_image_service(
    session: AsyncSession,
    file: UploadFile,
    user_id: int,
) -> UploadedFile:
    """Replace user's existing profile image with a new one."""

    # Optional: Remove old profile image file from DB
    old_file = await session.execute(
        select(UploadedFile).where(
            UploadedFile.user_id == user_id,
            UploadedFile.category == "user",
            UploadedFile.subcategory == "profile_image"
        )
    )
    old_file = old_file.scalar_one_or_none()

    # Save new uploaded file
    file_info = await save_uploaded_file(file, category="user", subcategory="profile_image")
    new_file = UploadedFile(
        **file_info,
        user_id=user_id,
        upload_time=datetime.utcnow()
    )

    if old_file:
        await session.delete(old_file)

    session.add(new_file)
    await session.commit()
    await session.refresh(new_file)

    return new_file



async def add_user_profile_service(
    user_id: int,
    user_data: UserProfileEditSchema,
    session: AsyncSession
):
    try:
        # Check if profile already exists
        result = await session.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Profile already exists")

        new_profile = UserProfile(
            user_id=user_id,
            **user_data.dict(exclude_unset=True)
        )
        session.add(new_profile)
        await session.commit()
        await session.refresh(new_profile)
        return new_profile

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create profile: {str(e)}")



async def edit_user_profile_service(
    user_id: int,
    user_data: UserProfileEditSchema,
    session: AsyncSession
):
    try:
        result = await session.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()

        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        for field, value in user_data.dict(exclude_unset=True).items():
            setattr(profile, field, value)

        await session.commit()
        await session.refresh(profile)
        return profile

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update profile: {str(e)}")



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



def is_user_profile_empty(profile: UserProfile) -> bool:
    return all([
        not profile.name,
        not profile.pronouns,
        not profile.profile_image,
        not profile.profile_description,
        not profile.phone,
        not profile.location,
        not profile.birth_date,
        not profile.languages_spoken,
        not profile.experience_with,
        not profile.certifications,
        not profile.certification_files
    ])



async def delete_user_account_service(user_id: int, session: AsyncSession):
    try:
        # Check if user exists
        user_result = await session.execute(
            select(Users).where(Users.id == user_id)
        )
        user = user_result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check for pets
        pets_result = await session.execute(
            select(Pets).where(Pets.parent_id == user_id)
        )
        pets = pets_result.scalars().all()

        if pets:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete account: pet profiles still exist."
            )

        # Check user profile
        profile_result = await session.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        profile = profile_result.scalar_one_or_none()

        if profile and not is_user_profile_empty(profile):
            raise HTTPException(
                status_code=400,
                detail="Cannot delete account: user profile still contains data."
            )

        # Proceed to delete user and optionally profile
        if profile:
            await session.delete(profile)
        await session.delete(user)
        await session.commit()

        return {"detail": "User deleted successfully"}

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")



async def delete_user_profile_service(user_id: int, session: AsyncSession):
    try:
        result = await session.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()

        if not profile:
            raise HTTPException(status_code=404, detail="User profile not found")

        await session.delete(profile)
        await session.commit()
        return {"detail": "User profile deleted successfully"}

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete profile: {str(e)}")



# async def delete_user_account_service(user_id: int, session: AsyncSession):
#     try:
#         # Check if user exists
#         user_result = await session.execute(
#             select(Users).where(Users.id == user_id)
#         )
#         user = user_result.scalar_one_or_none()
#
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#
#         # Check if profile still exists
#         profile_result = await session.execute(
#             select(UserProfile).where(UserProfile.user_id == user_id)
#         )
#         profile = profile_result.scalar_one_or_none()
#
#         if profile:
#             raise HTTPException(
#                 status_code=400,
#                 detail="Cannot delete account: profile still exists. Please delete it first."
#             )
#
#         # Proceed to delete user
#         await session.delete(user)
#         await session.commit()
#         return {"detail": "User deleted successfully"}
#
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")
