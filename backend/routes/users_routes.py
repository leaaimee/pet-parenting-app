from email.policy import default

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from pycparser.ply.yacc import resultlimit

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import user
from starlette import status

from backend.models.users_models import Users
from backend.auth.auth2 import get_user
from backend.services.users_service import register_user_service, show_user_profile_service, add_user_profile_service, edit_user_profile_service
from backend.services.users_service import add_user_profile_image_service, login_user_service, get_user_profile_image_service, edit_user_profile_image_service
from backend.services.users_service import delete_user_profile_service, delete_user_account_service

from backend.schemas.user_schema import UserLoginSchema, UserProfileEditSchema, UserProfileShowSchema, UserAccountShowSchema, UserAccountCreateSchema
from backend.schemas.user_schema import TokenRequest
from backend.schemas.media_schema import MediaBaseShowSchema

from backend.auth.auth import get_current_user

from backend.database import get_async_session

from backend.auth.auth2 import get_current_user





router = APIRouter()


#@router.get("/demo_user", response_model=UserProfileShowSchema)
#async def demo_user(session: AsyncSession = Depends(get_async_session)):
#    result = await get_user("first_user@example.com", session=session)
#    return result

@router.get("/protected-test")
async def protected_test(current_user: dict = Depends(get_current_user)):
    return {"message": "You're in!", "user": current_user}



@router.post("/", response_model=UserAccountShowSchema, status_code=201)
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


# latest version
@router.get("/users/me", response_model=UserProfileShowSchema)
async def show_private_user_profile_data(
    session: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(get_current_user),
):
    # Option A: call your existing service
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
    return await show_user_profile_service(user_id, session, public=True)


# latest version
@router.post(
    "/users/me",
    response_model=UserProfileShowSchema,
    status_code=status.HTTP_200_OK,  # use 200 for upserts
)
async def add_user_profile_data(
    user_data: UserProfileEditSchema,
    session: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(get_current_user),
):
    # Derive the user_id from the authenticated user
    profile = await add_user_profile_service(
        user_id=current_user.id,
        data=user_data,
        session=session,
    )
    return profile


# @router.put("/users/me", response_model=UserProfileShowSchema)
# async def edit_user_profile_data(
#     user_data: UserProfileEditSchema,
#     session: AsyncSession = Depends(get_async_session),
#     current_user: dict = Depends(get_current_user)
# ):
#     user_id = current_user["id"]
#
#     updated_user = await edit_user_profile_service(user_id, user_data, session)
#     return updated_user

# latest version
@router.patch("/users/me", response_model=UserProfileShowSchema)
async def edit_user_profile_data(
    user_data: UserProfileEditSchema,
    session: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(get_current_user),
):
    updated_profile = await edit_user_profile_service(
        user_id=current_user.id,
        user_data=user_data,
        session=session,
    )
    return updated_profile



@router.post("/users/me/image", response_model=MediaBaseShowSchema)
async def add_user_profile_image_data(
    user_id: int,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user)
):
    """Add user profile image data"""

    user_id = current_user["id"]

    uploaded_file = await add_user_profile_image_service(session, file, user_id)
    return uploaded_file



@router.put("/users/me/image", response_model=MediaBaseShowSchema)
async def edit_user_profile_image_data(
    user_id: int,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user)
):
    """Replace user profile image"""
    user_id = current_user["id"]

    uploaded_file = await edit_user_profile_image_service(session, file, user_id)
    return uploaded_file



@router.get("/media/user/{subcategory}/{filename}")
async def get_user_profile_image_data(
    subcategory: str,
    filename: str
):
    return await get_user_profile_image_service(subcategory, filename)



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








