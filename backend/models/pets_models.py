
from backend.database import Base
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func



class Pets(Base):
    __tablename__ = "pets"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    birthday = Column(Date, nullable=True)
    birth_year = Column(Integer, nullable=True)
    birth_month = Column(Integer, nullable=True)
    species = Column(String(100), nullable=False)
    subspecies = Column(String(100), nullable=True)
    gender = Column(String(20), nullable=True)
    profile_picture = Column(String(300), nullable=False, default="")
    profile_description = Column(Text, nullable=False, default="")
    created_at = Column(DateTime, default=func.now())

    parent_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    parent = relationship("Users", back_populates="pets")

    roles = relationship('Roles', back_populates='pet', lazy=True)
    pet_data = relationship('PetData', backref='pet', lazy=True)
    medical_profile = relationship("MedicalProfile", back_populates="pet", lazy=True)
    tasks = relationship('Tasks', backref='pet', lazy=True)
    sitters = relationship('Sitters', back_populates='pet', lazy=True)


class PetData(Base):
    __tablename__ = "pet_data"
    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    favorite_things = Column(Text, nullable=False, default="")
    dislikes = Column(Text, nullable=False, default="")
    social_style = Column(Text, nullable=False, default="")
    communication = Column(Text, nullable=False, default="")
    preferred_treats = Column(Text, nullable=False, default="")
    diet = Column(Text, nullable=False, default="")
    allergies = Column(Text, nullable=False, default="")
    medical_alerts = Column(Text, nullable=False, default="")
    behavior_notes = Column(Text, nullable=False, default="")
    additional_info = Column(Text, nullable=False, default="")

    user = relationship("Users", backref="pet_data")


# class MedicalRecord(Base):
#     __tablename__ = "medical_record"
#     id = Column(Integer, primary_key=True)
#     pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
#     weight = Column(String(20), nullable=True, default="")
#     weight_updated = Column(String(20), nullable=True)
#     record_type = Column(String(100))
#     description = Column(Text)
#     date = Column(DateTime)
#     vet_name = Column(String(100))
#     next_due_date = Column(DateTime)
#     test_results = Column(Text)
#     medication = Column(Text)
#     documents = Column(String(300))


class MedicalProfile(Base):
    __tablename__ = "medical_profiles"
    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    blood_type = Column(String(10))
    weight = Column(String(20), nullable=True, default="")
    weight_updated = Column(String(20), nullable=True)
    chronic_conditions = Column(Text)
    notes = Column(Text)

    pet = relationship("Pets", back_populates="medical_profile", lazy=True)
    vaccination_records = relationship("VaccinationRecord", back_populates="medical_profile", lazy=True)
    medications = relationship("Medication", back_populates="medical_profile", lazy=True)
    test_results = relationship("TestResult", back_populates="medical_profile", lazy=True)
    vet_visits = relationship("VetVisit", back_populates="medical_profile", lazy=True)
    medical_documents = relationship("MedicalDocument", back_populates="medical_profile", lazy=True)


class VaccinationRecord(Base):
    __tablename__ = "vaccination_records"
    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    medical_profile_id = Column(Integer, ForeignKey("medical_profiles.id"), nullable=False)
    vaccine_name = Column(String(100), nullable=False)
    dose_number = Column(Integer, nullable=True)
    batch_number = Column(String(50), nullable=True)
    previous_vaccination_date = Column(Date, nullable=True)
    next_vaccination_date = Column(String(50), nullable=True)
    additional_info = Column(Text, nullable=True)

    medical_profile = relationship("MedicalProfile", back_populates="vaccination_records")


class Medication(Base):
    __tablename__ = "medications"
    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    medical_profile_id = Column(Integer, ForeignKey("medical_profiles.id"), nullable=False)
    name = Column(String(100), nullable=False)
    dosage = Column(String(100))
    duration = Column(String(100))
    additional_info = Column(Text)

    medical_profile = relationship("MedicalProfile", back_populates="medications")



class TestResult(Base):
    __tablename__ = "test_results"
    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    medical_profile_id = Column(Integer, ForeignKey("medical_profiles.id"), nullable=False)
    test_type = Column(String(100))
    result = Column(Text)
    date = Column(Date)
    additional_info = Column(Text)

    medical_profile = relationship("MedicalProfile", back_populates="test_results")


class VetVisit(Base):
    __tablename__ = "vet_visits"
    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    medical_profile_id = Column(Integer, ForeignKey("medical_profiles.id"), nullable=False)
    reason = Column(String(200))
    vet_name = Column(String(100))
    clinic_info = Column(Text)
    date = Column(Date)
    documents = Column(String(300))

    medical_profile = relationship("MedicalProfile", back_populates="vet_visits")


class MedicalDocument(Base):
    __tablename__ = "medical_documents"
    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    medical_profile_id = Column(Integer, ForeignKey("medical_profiles.id"), nullable=False)
    file_path = Column(String(300))
    description = Column(Text)
    uploaded_at = Column(DateTime, default=func.now())

    medical_profile = relationship("MedicalProfile", back_populates="medical_documents")