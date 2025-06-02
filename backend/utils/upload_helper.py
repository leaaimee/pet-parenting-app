import os
import shutil
import hashlib
import uuid
import aiofiles
from pathlib import Path
from datetime import datetime
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

def generate_file_hash(file_bytes: bytes) -> str:
    return hashlib.sha256(file_bytes).hexdigest()


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


async def save_uploaded_file(file: UploadFile, category: str, subcategory: str = None) -> dict:
    upload_path = get_upload_subpath(category, subcategory)

    # Read the entire file for hashing and saving
    file_bytes = await file.read()
    file_hash = generate_file_hash(file_bytes)
    file_size = len(file_bytes)
    mime_type = file.content_type
    original_filename = file.filename
    ext = Path(file.filename).suffix
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    unique_id = uuid.uuid4().hex
    stored_filename = f"{timestamp}_{unique_id}{ext}"
    full_path = os.path.join(upload_path, stored_filename)

    # Save file with aiofiles
    async with aiofiles.open(full_path, "wb") as out_file:
        await out_file.write(file_bytes)

    return {
        "original_filename": original_filename,
        "stored_filename": stored_filename,
        "file_path": full_path,
        "file_hash": file_hash,
        "file_size": file_size,
        "mime_type": mime_type
    }
