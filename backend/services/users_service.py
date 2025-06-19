import os
import mimetypes
from fastapi.responses import FileResponse
from fastapi import HTTPException

from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from starlette.datastructures import UploadFile

from passlib.hash import bcrypt

from backend.auth.auth2 import get_password_hash
from backend.domain.exceptions import NotFoundError, InternalError
from backend.models.media_models import ProfileUpload
from backend.services.helpers.uploads import save_file_to_model
from backend.utils.upload_helper import get_upload_subpath, VALID_SUBCATEGORIES
from backend.models.users_models import Users, UserProfile
from backend.models.pets_models import Pets
from backend.schemas.user_schema import UserAccountCreateSchema, UserProfileEditSchema, UserLoginSchema, \
    UserProfileShowSchema
from backend.utils.upload_helper import save_uploaded_file
from backend.auth.auth2 import create_access_token



# create data content version
async def register_user_service(
    user_data: UserAccountCreateSchema,
    session: AsyncSession
):
    try:
        # 1. Check for existing email
        result = await session.execute(
            select(Users).where(Users.email == user_data.email)
        )
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already registered")

        # 2. Create the Users row
        hashed_password = get_password_hash(user_data.password)
        new_user = Users(
            email=user_data.email,
            password_hash=hashed_password
        )
        session.add(new_user)

        # 3. Flush so new_user.id is populated
        await session.flush()

        # 4. Auto-create an (initially minimal) UserProfile
        #    UserProfile.name is non-nullable, so we give it a placeholder
        profile = UserProfile(
            user_id=new_user.id,
            name=user_data.email.split("@")[0]  # e.g. "jane.doe" from "jane.doe@example.com"
        )
        session.add(profile)

        # 5. Commit both the user and profile in one go
        await session.commit()

        # 6. Refresh to pull back any defaults
        await session.refresh(new_user)
        return new_user

    except HTTPException:
        # propagate known HTTP errors (e.g. duplicate email)
        raise
    except Exception as e:
        # rollback on unexpected failures
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"User creation failed: {str(e)}"
        )



async def login_user_service(user_data: UserLoginSchema, session: AsyncSession):
    """Authenticate user and return access token placeholder"""
    result = await session.execute(
        select(Users).where(Users.email == user_data.email)
    )
    user = result.scalar_one_or_none()

    if not user or not bcrypt.verify(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}



async def save_user_avatar(user_id: int, file: UploadFile, session: AsyncSession):
    return await save_file_to_model(
        session=session,
        file=file,
        model=ProfileUpload,
        category="user",
        subcategory="avatar",
        user_id=user_id,
    )


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



async def add_user_profile_service(
    user_id: int,
    data: UserProfileEditSchema,
    session: AsyncSession,
) -> UserProfileShowSchema:

    result = await session.execute(
        select(UserProfile).where(UserProfile.user_id == user_id)
    )
    profile = result.scalar_one_or_none()

    if profile is None:
        profile = UserProfile(user_id=user_id, **data.dict())
        session.add(profile)
        status_code = status.HTTP_201_CREATED
    else:
        for field, value in data.dict(exclude_unset=True).items():
            setattr(profile, field, value)
        status_code = status.HTTP_200_OK

    await session.commit()
    await session.refresh(profile)

    return UserProfileShowSchema.from_orm(profile)



async def edit_user_profile_service(
    user_id: int,
    data: UserProfileEditSchema,
    session: AsyncSession
) -> UserProfile:
    profile = await session.scalar(
        select(UserProfile).where(UserProfile.user_id == user_id)
    )
    if not profile:
        raise NotFoundError("Profile not found")

    updates = data.model_dump(
        mode="python",
        exclude_unset=True,
        exclude_none=True,
    )
    # optional guard against Swagger’s “string” placeholder:
    updates = {k: v for k, v in updates.items() if v != "string"}

    for field, value in updates.items():
        setattr(profile, field, value)

    try:
        await session.commit()
        await session.refresh(profile)
        return profile
    except SQLAlchemyError:
        await session.rollback()
        raise InternalError("Failed to update profile, please try again later.")



async def show_user_profile_service(user_id: int, session: AsyncSession, public: bool = False):
    try:
        result = await session.execute(
            select(Users).where(Users.id == user_id).options(selectinload(Users.profile))
        )
        user = result.scalar_one_or_none()

        if not user or not user.profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User or profile not found"
            )

        profile = user.profile

        if public:
            public_data = {field: getattr(profile, field, None) for field in profile.public_fields or []}
            public_data.setdefault('id', profile.id)
            public_data.setdefault('name', profile.name)
            return UserProfileShowSchema(**public_data)

        # For private view, return the complete schema from ORM object
        return UserProfileShowSchema.from_orm(profile)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {str(e)}"
        )


def is_user_profile_empty(profile: UserProfile) -> bool:
    return all([
        not profile.name,
        not profile.pronouns,
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

        user_result = await session.execute(
            select(Users).where(Users.id == user_id)
        )
        user = user_result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        pets_result = await session.execute(
            select(Pets).where(Pets.parent_id == user_id)
        )
        pets = pets_result.scalars().all()

        if pets:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete account: pet profiles still exist."
            )

        profile_result = await session.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        profile = profile_result.scalar_one_or_none()

        if profile and not is_user_profile_empty(profile):
            raise HTTPException(
                status_code=400,
                detail="Cannot delete account: user profile still contains data."
            )

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


