import mimetypes
import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from backend.models.users_models import Users

from backend.services.users_service import get_user_profile, edit_user_profile_data, create_user_profile_data

from backend.schemas.user_schema import UserProfileSchema, UserCreateSchema, UserLoginSchema, UserEditProfileSchema
from backend.schemas.user_schema import TokenRequest

from backend.auth.jwt import get_current_user, create_access_token

from backend.utils.upload_helper import get_upload_subpath, VALID_SUBCATEGORIES

from werkzeug.security import check_password_hash



router = APIRouter()



@router.post("/", response_model=UserProfileSchema, status_code=201)
def register_user(user_data: UserCreateSchema):
    new_user = create_user_profile_data(user_data)

    if not new_user:
        raise HTTPException(status_code=400, detail="User creation failed")

    return{
        "id": new_user.id,
        "email": new_user.email,
        "name": new_user.name
    }


@router.post("/login")
def login_user(user_data: UserLoginSchema):
    user = Users.query.filter_by(email=user_data.email).first()

    if not user or not check_password_hash(user.password_hash, user_data.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {"access_token": "FAKE-TOKEN-FOR-NOW", "token_type": "bearer"}


@router.put("/edit")
def edit_user_profile(
        updated_data: UserEditProfileSchema,
        current_user: dict = Depends(get_current_user)
):
    updated_user = edit_user_profile_data(current_user, updated_data)

    if not updated_user:
        raise HTTPException(status_code=400, detail="Profile update failed")

    return {
        "id": updated_user.id,
        "email": updated_user.email,
        "name": updated_user.name,
        "phone": updated_user.phone,
        "location": updated_user.location,
        "birth_date": updated_user.birth_date,
        "pronouns": updated_user.pronouns,
        "profile_description": updated_user.profile_description,
        "languages_spoken": updated_user.languages_spoken,
        "experience_with": updated_user.experience_with,
        "certifications": updated_user.certifications,
        "profile_picture": updated_user.profile_picture
    }


@router.get("/media/user/{subcategory}/{filename}")
def serve_user_image(subcategory: str, filename: str):
    """Serve user image from subcategories like profile_pic."""
    if subcategory not in VALID_SUBCATEGORIES["user"]:
        raise HTTPException(status_code=400, detail="Invalid user image subcategory")

    file_path = os.path.join(get_upload_subpath("user", subcategory), filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=file_path, media_type=mimetypes.guess_type(file_path)[0] or "application/octet-stream")





router.get("/profile", response_model=UserProfileSchema)
def show_user_profile(current_user: dict = Depends(get_current_user)):
    user = get_user_profile(current_user["id"])

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/token")
def get_token(data: TokenRequest):
    if not data.username:
        raise HTTPException(status_code=400, detail="Missing username")

    token = create_access_token({"sub" : data.username})
    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/whoami")
def whoami(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello: {current_user['username']}"}


@router.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello, {current_user['username']}. You're in a secure zone."}




