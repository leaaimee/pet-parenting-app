from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    original_filename = Column(String(255), nullable=False)
    stored_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)  # Path to the file in the storage

    category = Column(String(50), nullable=False)  # e.g., 'medical', 'pet', 'profile', 'certification'
    subcategory = Column(String(50), nullable=True)  # e.g., 'xray', 'profile_picture'
    label = Column(String(100), nullable=True)  # e.g., 'vet-visit-123.pdf'

    mime_type = Column(String(100), nullable=True)
    file_size = Column(Integer, nullable=True)
    file_hash = Column(String(64), nullable=True)

    uploaded_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    pet = relationship("Pets", back_populates="uploaded_files", lazy="selectin")
    user = relationship("Users", back_populates="uploaded_files", lazy="selectin")