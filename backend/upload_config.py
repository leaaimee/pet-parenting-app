import os

base_upload = os.path.join(os.getcwd(), 'backend', 'uploads')

UPLOAD_CONFIG = {
    "MAX_CONTENT_LENGTH": 16 * 1024 * 1024,  # 16MB
    "ALLOWED_EXTENSIONS": {'png', 'jpg', 'jpeg', 'gif', 'pdf'},
    "PET_IMAGE_UPLOAD_FOLDER": os.path.join(base_upload, 'pet_images'),
    "USER_IMAGE_UPLOAD_FOLDER": os.path.join(base_upload, 'user_images'),
    "MEDICAL_UPLOAD_FOLDER": os.path.join(base_upload, 'medical_docs'),
}
