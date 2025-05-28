from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime


class PetBasicSchema(BaseModel):
    id: int
    name: str
    species: str
    subspecies: str | None = None
    gender: str | None = None

    class Config:
        orm_mode = True



class PetProfileShowSchema(BaseModel):
    id: int
    name: str
    birthday: date | None = None
    birth_year: int | None = None
    birth_month: int | None = None
    species: str | None = None
    subspecies: str | None = None
    gender: str | None = None
    profile_picture: str | None = None
    profile_description: str | None = None
    created_at: datetime | None = None

    pet_data: Optional["PetDataSchema"]

    class Config:
        orm_mode = True


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
        orm_mode = True  # Still useful if using models


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
        orm_mode = True



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
        orm_mode = True


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
        orm_mode = True


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
        orm_mode = True



class PetMedicalProfileShowSchema(BaseModel):
    id: int
    pet_id: int
    blood_type: str | None = None
    weight: str | None = None
    weight_updated: str | None = None
    chronic_conditions: str | None = None
    notes: str | None = None

    class Config:
        orm_mode = True


class PetMedicalProfileAddSchema(BaseModel):
    blood_type: str | None = None
    weight: str | None = None
    weight_updated: str | None = None
    chronic_conditions: str | None = None
    notes: str | None = None

    class Config:
        orm_mode = True


class PetMedicalProfileEditSchema(BaseModel):
    blood_type: str | None = None
    weight: str | None = None
    weight_updated: str | None = None
    chronic_conditions: str | None = None
    notes: str | None = None

    class Config:
        orm_mode = True



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
        orm_mode = True


class PetVaccinationAddSchema(BaseModel):
    vaccine_name: str | None = None
    dose_number: str | None = None
    batch_number: str | None = None
    previous_vaccination_date: date | None = None
    next_vaccination_date: str | None = None
    additional_info: str | None = None

    class Config:
        orm_mode = True


class PetVaccinationEditSchema(BaseModel):
    vaccine_name: str | None = None
    dose_number: str | None = None
    batch_number: str | None = None
    previous_vaccination_date: date | None = None
    next_vaccination_date: str | None = None
    additional_info: str | None = None

    class Config:
        orm_mode = True


class PetMedicationShowSchema(BaseModel):
    id: int
    pet_id: int | None = None
    medical_profile_id: int | None = None
    name: str | None = None
    dosage: str | None = None
    duration: str | None = None
    additional_info: str | None = None

    class Config:
        orm_mode = True


class PetMedicationAddSchema(BaseModel):
    name: str | None = None
    dosage: str | None = None
    duration: str | None = None
    additional_info: str | None = None

    class Config:
        orm_mode = True


class PetMedicationEditSchema(BaseModel):
    name: str | None = None
    dosage: str | None = None
    duration: str | None = None
    additional_info: str | None = None

    class Config:
        orm_mode = True


class PetTestResultShowSchema(BaseModel):
    id: int
    pet_id: int | None = None
    medical_profile_id: int | None = None
    test_type: str | None = None
    result: str | None = None
    date: date | None = None
    additional_info: str | None = None

    class Config:
        orm_mode = True


class PetTestResultAddSchema(BaseModel):
    test_type: str | None = None
    result: str | None = None
    date: date | None = None
    additional_info: str | None = None

    class Config:
        orm_mode = True


class PetTestResultEditSchema(BaseModel):
    test_type: str | None = None
    result: str | None = None
    date: date | None = None
    additional_info: str | None = None

    class Config:
        orm_mode = True


class PetVetVisitShowSchema(BaseModel):
    id: int
    pet_id: int | None = None
    medical_profile_id: int | None = None
    reason: str | None = None
    vet_name: str | None = None
    clinic_info: str | None = None
    date: date | None = None
    documents: str | None = None

    class Config:
        orm_mode = True


class PetVetVisitAddSchema(BaseModel):
    medical_profile_id: int | None = None
    reason: str | None = None
    vet_name: str | None = None
    clinic_info: str | None = None
    date: str | None = None
    documents: str | None = None

    class Config:
        orm_mode = True


class PetVetVisitEditSchema(BaseModel):
    medical_profile_id: int | None = None
    reason: str | None = None
    vet_name: str | None = None
    clinic_info: str | None = None
    date: date | None = None
    documents: str | None = None

    class Config:
        orm_mode = True


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
        orm_mode = True


class PetMedicalDocumentAddSchema(BaseModel):
    document_name: str | None = None
    document_type: str | None = None
    upload_date: date | None = None
    file_path: str | None = None
    additional_info: str | None = None

    class Config:
        orm_mode = True


class PetMedicalDocumentEditSchema(BaseModel):
    document_name: str | None = None
    document_type: str | None = None
    upload_date: date | None = None
    file_path: str | None = None
    additional_info: str | None = None

    class Config:
        orm_mode = True