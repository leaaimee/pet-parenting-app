import os
import mimetypes

from fastapi import APIRouter, Depends, File, HTTPException

from fastapi.responses import FileResponse
from starlette import status

from backend.database import get_async_session

from backend.auth.auth2 import get_current_user

from backend.models.users_models import Users
from backend.schemas.media_schema import ProfileUploadShowSchema

from backend.schemas.pet_schema import PetBasicSchema, PetProfileShowSchema, PetDataShowSchema
from backend.utils.uploads import save_file_to_model

from backend.services.pets_service import *

from backend.utils.upload_helper import get_upload_subpath, VALID_SUBCATEGORIES




router = APIRouter()


@router.get("/family", response_model=list[PetBasicSchema])
async def view_pets_family_data(
    current_user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await get_user_pets_service(current_user.id, session)



@router.get(
    "/pets/{pet_id}",
    response_model=PetProfileShowSchema,
)
async def get_pet_profile_data(
    pet_id: int,
    current_user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    pet = await get_pet_profile_service(pet_id, current_user.id, session)
    return pet



@router.patch(
    "/pets/{pet_id}",
    response_model=PetProfileShowSchema,
)
async def edit_pet_profile_data(
    pet_id: int,
    data: PetProfileEditSchema,
    current_user: Users      = Depends(get_current_user),
    session: AsyncSession    = Depends(get_async_session),
):
    updated = await edit_pet_profile_service(
        pet_id=pet_id,
        owner_id=current_user.id,
        data=data,
        session=session,
    )
    return updated



@router.post(
    "/pets",
    response_model=PetProfileShowSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_pet_profile_data(
    pet_data: PetProfileAddSchema,
    current_user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await add_pet_profile_service(pet_data, current_user.id, session)



@router.patch(
    "/pets/{pet_id}",
    response_model=PetProfileShowSchema,
)
async def edit_pet_profile_data(
    pet_id: int,
    data: PetProfileEditSchema,
    current_user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await edit_pet_profile_service(pet_id, current_user.id, data, session)



@router.post(
    "/pets/{pet_id}/image",
    response_model=ProfileUploadShowSchema,
    status_code=status.HTTP_201_CREATED,
)
async def upload_pet_image(
    pet_id: int,
    file: UploadFile = File(...),
    current_user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await save_file_to_model(
        session=session,
        file=file,
        model=ProfileUpload,
        pet_id=pet_id,
        user_id=current_user.id,
        subcategory="portrait"
    )



@router.put(
    "/pets/{pet_id}/image",
    response_model=ProfileUploadShowSchema,
)
async def replace_pet_profile_image(
    pet_id: int,
    file: UploadFile = File(...),
    current_user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await replace_pet_profile_image_service(
        session=session,
        file=file,
        pet_id=pet_id,
        user_id=current_user.id,
    )



# --- Static file serving stays in HTTP layer ---
@router.get("/media/pet/{subcategory}/{filename}")
def get_pet_profile_image_data(subcategory: str, filename: str):
    if subcategory not in VALID_SUBCATEGORIES["pet"]:
        raise HTTPException(status_code=400, detail="Invalid pet image subcategory")

    file_path = get_upload_subpath("pet", subcategory)
    full_path = os.path.join(file_path, filename)
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="File not found")

    media_type, _ = mimetypes.guess_type(full_path)
    return FileResponse(path=full_path, media_type=media_type or "application/octet-stream")



@router.get("/pets/{pet_id}/data", response_model=PetDataShowSchema)
async def show_pet_data(
    pet_id: int,
    current_user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    pet_data = await show_pet_data_service(
        pet_id=pet_id,
        parent_id=current_user.id,
        session=session
    )
    return pet_data


# --- Add pet data ---
@router.post("/pets/{pet_id}/data", response_model=PetDataAddSchema, status_code=status.HTTP_201_CREATED)
async def add_pet_data(
    pet_id: int,
    pet_data: PetDataAddSchema,
    session: AsyncSession = Depends(get_async_session),
    current_user = Depends(get_current_user),
):
    # service will raise NotFoundError if pet not found / unauthorized
    return await add_pet_data_service(pet_id, current_user.id, pet_data, session)



# --- Edit pet data ---
@router.patch("/pets/{pet_id}/data", response_model=PetDataEditSchema)
async def edit_pet_data(
    pet_id: int,
    pet_data: PetDataEditSchema,
    session: AsyncSession = Depends(get_async_session),
    current_user = Depends(get_current_user),
):
    return await edit_pet_data_service(pet_id, current_user.id, pet_data, session)



# --- Delete entire pet if empty ---
@router.delete("/pets/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pet_profile_data(
    pet_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user = Depends(get_current_user),
):
    # service raises NotFoundError, PermissionDeniedError, ConflictError, or InternalError
    await delete_pet_profile_service(pet_id, current_user.id, session)



# --- Delete just the pet_data record ---
@router.delete("/pets/{pet_id}/data", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pet_data(
    pet_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user = Depends(get_current_user),
):
    await delete_pet_data_service(pet_id, current_user.id, session)


