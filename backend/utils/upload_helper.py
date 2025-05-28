import os
import shutil
from fastapi import UploadFile

UPLOAD_BASE = os.path.join(os.getcwd(), 'backend', 'uploads')

# upload_helper.py
VALID_UPLOAD_CATEGORIES = {
    "pet": "pet_images",
    "user": "user_images",
    "medical": "medical_docs",
}

VALID_SUBCATEGORIES = {
    "medical": ["xray", "bloodwork", "lab", "prescription", "misc"],
    "pet": ["portrait", "action"],
    "user": ["profile_pic"]
}




def get_upload_subpath(category: str, subcategory: str = None) -> str:
    if category not in VALID_UPLOAD_CATEGORIES:
        raise ValueError(f"Invalid category: {category}")

    base_folder = os.path.join(UPLOAD_BASE, VALID_UPLOAD_CATEGORIES[category])

    if subcategory:
        if category not in VALID_SUBCATEGORIES or subcategory not in VALID_SUBCATEGORIES[category]:
            raise ValueError(f"Invalid subcategory '{subcategory}' for category '{category}'")
        base_folder = os.path.join(base_folder, subcategory)

    os.makedirs(base_folder, exist_ok=True)
    return base_folder


def save_uploaded_file(file: UploadFile, category: str, subcategory: str = None) -> str:
    upload_path = get_upload_subpath(category, subcategory)
    file_path = os.path.join(upload_path, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file.filename  # or full path if needed


