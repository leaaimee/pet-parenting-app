
from __future__ import annotations

from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

from backend.schemas.media_schema import MediaBaseShowSchema





class PetBasicSchema(BaseModel):
    id: int
    name: str
    species: str
    subspecies: str | None = None
    gender: str | None = None

    class Config:
        from_attributes = True


class PetProfileShowSchema(BaseModel):
    id: int
    name: str
    birthday: date | None = None
    birth_year: int | None = None
    birth_month: int | None = None
    species: str | None = None
    subspecies: str | None = None
    gender: str | None = None
    profile_picture: MediaBaseShowSchema | None = None
    profile_description: str | None = None
    created_at: datetime | None = None

    pet_data: Optional["PetDataShowSchema"]

    class Config:
        from_attributes = True



class PetProfileAddSchema(BaseModel):
    name: str
    birth_year: int | None = None
    birth_month: int | None = None
    birthday: date | None = None  # ✅ ISO format expected
    species: str | None = None
    subspecies: str | None = None
    gender: str | None = None
    profile_picture: str | None = None
    profile_description: str | None = None

    class Config:
        from_attributes = True
# Still useful if using models


class PetProfileEditSchema(BaseModel):
    name: str | None = None
    species: str | None = None
    subspecies: str | None = None
    gender: str | None = None
    birthday: date | None = None
    birth_year: int | None = None
    birth_month: int | None = None
    profile_picture: str | None = None
    profile_description: str | None = None

    class Config:
        from_attributes = True


class PetDataShowSchema(BaseModel):
    id: int
    favorite_things: str | None = None
    dislikes: str | None = None
    social_style: str | None = None
    communication: str | None = None
    preferred_treats: str | None = None
    diet: str | None = None
    allergies: str | None = None
    medical_alerts: str | None = None
    behavior_notes: str | None = None
    additional_info: str | None = None

    class Config:
        from_attributes = True


class PetDataAddSchema(BaseModel):
    favorite_things: str | None = None
    dislikes: str | None = None
    social_style: str | None = None
    communication: str | None = None
    preferred_treats: str | None = None
    diet: str | None = None
    allergies: str | None = None
    medical_alerts: str | None = None
    behavior_notes: str | None = None
    additional_info: str | None = None

    class Config:
        from_attributes = True


class PetDataEditSchema(BaseModel):
    favorite_things: str | None = None
    dislikes: str | None = None
    social_style: str | None = None
    communication: str | None = None
    preferred_treats: str | None = None
    diet: str | None = None
    allergies: str | None = None
    medical_alerts: str | None = None
    behavior_notes: str | None = None
    additional_info: str | None = None

    class Config:
        from_attributes = True


class PetMedicalProfileShowSchema(BaseModel):
    id: int
    pet_id: int
    blood_type: str | None = None
    weight: str | None = None
    weight_updated: str | None = None
    chronic_conditions: str | None = None
    notes: str | None = None

    class Config:
        from_attributes = True


class PetMedicalProfileAddSchema(BaseModel):
    blood_type: str | None = None
    weight: str | None = None
    weight_updated: str | None = None
    chronic_conditions: str | None = None
    notes: str | None = None

    class Config:
        from_attributes = True


class PetMedicalProfileEditSchema(BaseModel):
    blood_type: str | None = None
    weight: str | None = None
    weight_updated: str | None = None
    chronic_conditions: str | None = None
    notes: str | None = None

    class Config:
        from_attributes = True


class PetVaccinationShowSchema(BaseModel):
    id: int
    pet_id: int | None = None
    medical_profile_id: int | None = None
    vaccine_name: str | None = None
    dose_number: int | None = None
    batch_number: str | None = None
    previous_vaccination_date: date | None = None
    next_vaccination_date: str | None = None
    additional_info: str | None = None

    class Config:
        from_attributes = True


class PetVaccinationAddSchema(BaseModel):
    vaccine_name: str | None = None
    dose_number: str | None = None
    batch_number: str | None = None
    previous_vaccination_date: date | None = None
    next_vaccination_date: str | None = None
    additional_info: str | None = None

    class Config:
        from_attributes = True


class PetVaccinationEditSchema(BaseModel):
    vaccine_name: str | None = None
    dose_number: str | None = None
    batch_number: str | None = None
    previous_vaccination_date: date | None = None
    next_vaccination_date: str | None = None
    additional_info: str | None = None

    class Config:
        from_attributes = True


class PetMedicationShowSchema(BaseModel):
    id: int
    pet_id: int | None = None
    medical_profile_id: int | None = None
    name: str | None = None
    dosage: str | None = None
    duration: str | None = None
    additional_info: str | None = None

    class Config:
        from_attributes = True


class PetMedicationAddSchema(BaseModel):
    name: str | None = None
    dosage: str | None = None
    duration: str | None = None
    additional_info: str | None = None

    class Config:
        from_attributes = True


class PetMedicationEditSchema(BaseModel):
    name: str | None = None
    dosage: str | None = None
    duration: str | None = None
    additional_info: str | None = None

    class Config:
        from_attributes = True


class PetTestResultShowSchema(BaseModel):
    id: int
    pet_id: int | None = None
    medical_profile_id: int | None = None
    test_type: str | None = None
    result: str | None = None
    test_date: date | None = None
    additional_info: str | None = None

    class Config:
        from_attributes = True


class PetTestResultAddSchema(BaseModel):
    test_type: str | None = None
    result: str | None = None
    test_date: date | None = None
    additional_info: str | None = None

    class Config:
        from_attributes = True


class PetTestResultEditSchema(BaseModel):
    test_type: str | None = None
    result: str | None = None
    test_date: date | None = None
    additional_info: str | None = None

    class Config:
        from_attributes = True


class PetMedicalDocumentShowSchema(BaseModel):
    id: int
    pet_id: int | None = None
    medical_profile_id: int | None = None
    document_name: str | None = None
    document_type: str | None = None
    upload_date: date | None = None
    file_path: str | None = None
    additional_info: str | None = None

    class Config:
        from_attributes = True


class PetMedicalDocumentAddSchema(BaseModel):
    medical_profile_id: int | None = None
    document_name: str | None = None
    document_type: str | None = None
    upload_date: date | None = None
    additional_info: str | None = None

    class Config:
        from_attributes = True


class PetMedicalDocumentEditSchema(BaseModel):
    medical_profile_id: int | None = None
    document_name: str | None = None
    document_type: str | None = None
    upload_date: date | None = None
    additional_info: str | None = None

    class Config:
        from_attributes = True


class PetVetVisitShowSchema(BaseModel):
    id: int
    pet_id: int | None = None
    medical_profile_id: int | None = None
    reason: str | None = None
    vet_name: str | None = None
    clinic_info: str | None = None
    visit_date: date | None = None
    documents: list[PetMedicalDocumentShowSchema] = []

    class Config:
        from_attributes = True


class PetVetVisitAddSchema(BaseModel):
    medical_profile_id: int | None = None
    reason: str | None = None
    vet_name: str | None = None
    clinic_info: str | None = None
    visit_date: str | None = None
    documents: list[PetMedicalDocumentShowSchema] = []

    class Config:
        from_attributes = True


class PetVetVisitEditSchema(BaseModel):
    medical_profile_id: int | None = None
    reason: str | None = None
    vet_name: str | None = None
    clinic_info: str | None = None
    visit_date: date | None = None
    documents: list[PetMedicalDocumentShowSchema] = []

    class Config:
        from_attributes = True


PetProfileShowSchema.model_rebuild()

