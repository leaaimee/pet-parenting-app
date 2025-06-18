from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship, foreign
from datetime import datetime
from backend.database import Base

from backend.models.users_models import UserProfile


class UploadBase:
    id = Column(Integer, primary_key=True)
    original_filename = Column(String(255), nullable=False)
    stored_filename   = Column(String(255), nullable=False)
    file_path         = Column(String(500), nullable=False)
    file_hash         = Column(String(64), nullable=False)
    mime_type         = Column(String(100))
    file_size         = Column(Integer)
    uploaded_at       = Column(DateTime, default=func.now())
    is_active         = Column(Boolean, default=True)


class ProfileUpload(UploadBase, Base):
    __tablename__ = "profile_uploads"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    pet_id  = Column(Integer, ForeignKey("pets.id"), nullable=True)
    subcategory = Column(String(50), nullable=False)  # e.g. "avatar","portrait"

    pet = relationship("Pets", back_populates="profile_uploads", lazy="selectin")

    profile_owner = relationship(
        "UserProfile",  # refer by name
        primaryjoin="foreign(ProfileUpload.user_id) == UserProfile.user_id",
        back_populates="profile_uploads",
        lazy="selectin",
    )


class MedicalUpload(UploadBase, Base):
    __tablename__ = "medical_uploads"

    medical_profile_id = Column(Integer, ForeignKey("medical_profiles.id"), nullable=True)
    vet_visit_id       = Column(Integer, ForeignKey("vet_visits.id"), nullable=True)
    document_type      = Column(String(50), nullable=False)  # e.g. "xray","lab","prescription"

