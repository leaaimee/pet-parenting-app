from datetime import date
from fastapi import UploadFile

def prepare_medical_document_data(
    pet_id: int,
    document_name: str,
    document_type: str,
    upload_date: date | None,
    additional_info: str | None,
    file: UploadFile | None
) -> dict:
    return {
        "pet_id": pet_id,
        "document_name": document_name,
        "document_type": document_type,
        "upload_date": upload_date or date.today(),
        "additional_info": additional_info or "",
        "file": file
    }
