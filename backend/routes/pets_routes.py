import os
import mimetypes

from fastapi import APIRouter, Depends, File

from fastapi.responses import FileResponse

from backend.database import get_async_session

from backend.auth.jwt import get_current_user
# from backend.database import get_db

from backend.schemas.media_schema import MediaBaseShowSchema

from backend.schemas.pet_schema import PetBasicSchema, PetProfileShowSchema

from backend.services.pets_service import *

from backend.utils.upload_helper import get_upload_subpath, VALID_SUBCATEGORIES




router = APIRouter()

@router.get("/pets/family", response_model=list[PetBasicSchema])
async def view_pets_family_data(
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """View all pets owned or cared for by the current user."""
    return await get_user_pets_service(current_user["id"], session)




@router.get("/pets/{pet_id}", response_model=PetProfileShowSchema)
async def get_pet_profile_data(
    pet_id: int,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Return detailed pet profile including optional pet data"""
    pet = await get_pet_profile_data_service(pet_id, current_user["id"], session)

    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    return pet



@router.post("/pets", response_model=PetProfileShowSchema)
async def add_pet_profile_data(
    pet_data: PetProfileAddSchema,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Create a new pet profile for the logged-in user"""
    pet_dict = prepare_pet_profile_data(pet_data, current_user["id"])
    new_pet = await add_pet_profile_data_service(**pet_dict, session=session)

    if not new_pet:
        raise HTTPException(status_code=500, detail="Pet creation failed")

    return {"message": "New pet profile added", "pet_id": new_pet.id}




@router.patch("/pets/{pet_id}", response_model=PetProfileShowSchema)
async def edit_pet_profile_data(
    pet_id: int,
    data: PetProfileEditSchema,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    updated_pet = await edit_pet_profile_data_service(pet_id, current_user["id"], data, session)

    if not updated_pet:
        raise HTTPException(status_code=404, detail="Pet not found or unauthorized")

    return updated_pet



@router.post("/pets/{pet_id}/image", response_model=MediaBaseShowSchema)
async def add_pet_profile_image_data(
    pet_id: int,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user)
):
    uploaded_file = await add_pet_profile_image_service(session, file, pet_id)
    return uploaded_file



@router.get("/media/pet/{subcategory}/{filename}")
def get_pet_profile_image_data(subcategory: str, filename: str):
    """Serve pet image from a subcategory like portrait/action."""
    if subcategory not in VALID_SUBCATEGORIES["pet"]:
        raise HTTPException(status_code=400, detail="Invalid pet image subcategory")

    file_path = os.path.join(get_upload_subpath("pet", subcategory), filename)
    media_type, _ = mimetypes.guess_type(file_path)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=file_path, media_type=media_type or "application/octet-stream")



@router.post("/pets/{pet_id}/data", response_model=PetDataAddSchema)
async def add_pet_data(
    pet_id: int,
    pet_data: PetDataAddSchema,
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user)
):
    new_data = await add_pet_data_service(pet_id, current_user["id"], pet_data, session)

    if not new_data:
        raise HTTPException(status_code=404, detail="Pet not found or data submission failed")

    return new_data



@router.patch("/pets/{pet_id}/data/edit", response_model=PetDataEditSchema)
async def edit_pet_data(
        pet_id:int,
        pet_data: PetDataEditSchema,
        session: AsyncSession = Depends(get_async_session),
        current_user: dict = Depends(get_current_user)
):
    """Edit existing pet data"""
    updated_data = await edit_pet_data_service(pet_id, current_user["id"], pet_data, session)
    if not updated_data:
        raise HTTPException(status_code=404, detail="Pet not found or data update failed")

    return updated_data




