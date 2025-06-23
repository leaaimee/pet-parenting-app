import os
import mimetypes

from fastapi import HTTPException, UploadFile

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from sqlalchemy.future import select

from backend.models.media_models import ProfileUpload
from backend.models.users_models import Users
from backend.schemas.media_schema import ProfileUploadShowSchema
from backend.utils.uploads import save_file_to_model, save_user_avatar
from backend.services.users_service import register_user_service, show_user_profile_service, add_user_profile_service, edit_user_profile_service
from backend.services.users_service import login_user_service
from backend.services.users_service import delete_user_profile_service, delete_user_account_service

from backend.schemas.user_schema import UserLoginSchema, UserProfileEditSchema, UserProfileShowSchema, UserAccountShowSchema, UserAccountCreateSchema


from backend.database import get_async_session

from backend.auth.auth2 import get_current_user

from fastapi import APIRouter, Depends, File

from fastapi.responses import FileResponse

from backend.utils.upload_helper import get_upload_subpath, VALID_SUBCATEGORIES

router = APIRouter()


from alembic import command
from alembic.config import Config

@router.post("/run-migrations")
async def run_migrations():
    from alembic import command
    from alembic.config import Config
    import os

    cfg = Config("alembic.ini")
    cfg.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL", ""))
    command.upgrade(cfg, "head")
    return {"message": "Migrations applied"}



@router.get("/protected-test")
async def protected_test(current_user: dict = Depends(get_current_user)):
    return {"message": "You're in!", "user": current_user}



@router.post("/", response_model=UserAccountShowSchema)
async def register_user_data(
    user_data: UserAccountCreateSchema,
    session: AsyncSession = Depends(get_async_session)
):
    new_user = await register_user_service(user_data, session)

    return {
    "id": new_user.id,
    "email": new_user.email,
    "created_at": new_user.created_at
}


@router.post("/login")
async def login_user_data(
    user_data: UserLoginSchema,
    session: AsyncSession = Depends(get_async_session)
):
    return await login_user_service(user_data, session)



@router.get("/users/me", response_model=UserProfileShowSchema)
async def show_private_user_profile_data(
    session: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(get_current_user),
):
    profile_schema = await show_user_profile_service(
        user_id=current_user.id,
        session=session,
        public=False,
    )
    return profile_schema


@router.get("/users/{user_id}", response_model=UserProfileShowSchema)
async def show_public_user_profile_data(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    user_schema = await show_user_profile_service(
        user_id=user_id,
        session=session,
        public=True
    )
    return user_schema


@router.post(
    "/users/me",
    response_model=UserProfileShowSchema,
    status_code=status.HTTP_200_OK,
)
async def add_user_profile_data(
    user_data: UserProfileEditSchema,
    session: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(get_current_user),
):
    profile = await add_user_profile_service(
        user_id=current_user.id,
        data=user_data,
        session=session,
    )
    return profile



@router.patch("/users/me", response_model=UserProfileShowSchema)
async def edit_user_profile_data(
    user_data: UserProfileEditSchema,
    session: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(get_current_user),
):
    updated_profile = await edit_user_profile_service(
        user_id=current_user.id,
        data=user_data,
        session=session,
    )
    return updated_profile


@router.post("/me/avatar", response_model=ProfileUploadShowSchema)
async def upload_avatar_for_current_user(
    file: UploadFile = File(...),
    user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await save_user_avatar(user.id, file, session)



@router.post(
    "/users/me/image",
    response_model=ProfileUploadShowSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_user_profile_image_data(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await save_file_to_model(
        session=session,
        file=file,
        model=ProfileUpload,
        category="user",
        subcategory="profile_pic",
        user_id=current_user.id
    )
@router.post(
    "/users/me/image",
    response_model=ProfileUploadShowSchema,
    status_code=status.HTTP_201_CREATED,
)


@router.put(
    "/users/me/image",
    response_model=ProfileUploadShowSchema,
)
async def replace_user_profile_image_data(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    # Delete old profile picture if exists
    old = await session.execute(
        select(ProfileUpload).where(
            ProfileUpload.user_id == current_user.id,
            ProfileUpload.subcategory == "profile_pic",
        )
    )
    old_file = old.scalar_one_or_none()
    if old_file:
        await session.delete(old_file)
        await session.commit()

    # Reuse the POST logic
    return await add_user_profile_image_data(file, current_user, session)



@router.get("/media/user/{subcategory}/{filename}")
def get_user_profile_image_data(subcategory: str, filename: str):
    # Validate subcategory
    if subcategory not in VALID_SUBCATEGORIES["user"]:
        raise HTTPException(status_code=400, detail="Invalid user image subcategory")

    folder = get_upload_subpath("user", subcategory)
    path = os.path.join(folder, filename)
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="File not found")

    media_type, _ = mimetypes.guess_type(path)
    return FileResponse(
        path=path,
        media_type=media_type or "application/octet-stream",
        filename=filename
    )



@router.delete("/user/me")
async def delete_user_account_data(
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user)
):
    """Delete user account if no pets and profile is empty or non-existent"""
    return await delete_user_account_service(current_user["id"], session)



@router.delete("/user/me/profile")
async def delete_user_profile_data(
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user)
):
    """Delete user profile data"""
    return await delete_user_profile_service(current_user["id"], session)








