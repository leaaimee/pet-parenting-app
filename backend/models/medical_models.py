from sqlalchemy import Column, Integer, ForeignKey, String, Text, Date, DateTime, func
from sqlalchemy.orm import relationship

from backend.database import Base


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
    documents = relationship("MedicalDocument", back_populates="vet_visit")

    medical_profile = relationship("MedicalProfile", back_populates="vet_visits")
    linked_documents = relationship("VetVisitDocument", back_populates="vet_visit", cascade="all, delete")


class MedicalDocument(Base):
    __tablename__ = "medical_documents"
    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    medical_profile_id = Column(Integer, ForeignKey("medical_profiles.id"), nullable=False)
    file_path = Column(String(300))
    description = Column(Text)
    uploaded_at = Column(DateTime, default=func.now())

    medical_profile = relationship("MedicalProfile", back_populates="medical_documents")
    linked_visits = relationship("VetVisitDocument", back_populates="medical_document", cascade="all, delete")

    vet_visit_id = Column(Integer, ForeignKey("vet_visits.id"), nullable=True)
    vet_visit = relationship("VetVisit", back_populates="documents")


class VetVisitDocument(Base):
    __tablename__ = "vet_visit_documents"
    id = Column(Integer, primary_key=True)

    vet_visit_id = Column(Integer, ForeignKey("vet_visits.id"), nullable=False)
    medical_document_id = Column(Integer, ForeignKey("medical_documents.id"), nullable=False)

    vet_visit = relationship("VetVisit", back_populates="linked_documents")
    medical_document = relationship("MedicalDocument", back_populates="linked_visits")
