
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
    profile_description = Column(Text, nullable=False, default="")
    created_at = Column(DateTime, default=func.now())

    parent_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    #parent = relationship("Users", back_populates="pets")
    #roles = relationship('Roles', back_populates='pet', lazy=True)
    pet_data = relationship(
    'PetData',
    back_populates = 'pet',  # prefer explicit back_populates to backref
    uselist = False,  # ← THIS makes it a one-to-one
    lazy = 'selectin',  # eager-load it in one go
    cascade = 'all, delete-orphan',
    )

    profile_uploads = relationship(
        "ProfileUpload",
        back_populates="pet",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    medical_profile = relationship(
        "MedicalProfile",      # string avoids circular import
        back_populates="pet",
        uselist=False,         # one-to-one
        lazy="selectin"
    )
    # tasks = relationship('Tasks', backref='pet', lazy=True)
    #sitters = relationship('Sitters', back_populates='pet', lazy=True)


class PetData(Base):
    __tablename__ = "pet_data"
    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False, unique=True)
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

    pet = relationship(
    "Pets",
    back_populates = "pet_data",
    lazy = "selectin",
    )
    user = relationship("Users", backref="pet_data")



