from backend.database import Base
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.utils.constants import RoleType, AccessLevel, InvitationStatus
from werkzeug.security import generate_password_hash, check_password_hash


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key= True)
    name = Column(String(100), nullable=False)
    pronouns = Column(String(50))
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(200), nullable=False)
    profile_image = Column(String(300))
    profile_description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    phone = Column(String(20), nullable=True)
    location = Column(String(100))
    birth_date = Column(Date)
    languages_spoken = Column(String(100))
    experience_with = Column(Text)
    certifications = Column(Text)
    certification_files = Column(String(300))

    public_fields: JSON = Column(JSON, default=[])


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    roles = relationship('Roles', back_populates='user', lazy=True)
    assigned_tasks = relationship('Tasks', backref='assigned_user', lazy=True)
    sitting_assignments = relationship('Sitters', back_populates='sitter', overlaps="sitters")
    pets = relationship("Pets", back_populates="parent")


class Roles(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey('pets.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    role = Column(Enum(RoleType), nullable=False)
    access_level = Column(Enum(AccessLevel), nullable=False, default=AccessLevel.VIEW_ALL)

    pet = relationship('Pets', back_populates='roles')
    user = relationship('Users', back_populates='roles')


class Sitters(Base):
    __tablename__ = "sitters"
    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    sitter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    invitation_status = Column(Enum(InvitationStatus), default=InvitationStatus.PENDING, nullable=False) # default: pending
    completed = Column(Boolean, default=False)
    access_level = Column(Enum(AccessLevel), nullable=False, default=AccessLevel.VIEW_LIMITED)

    pet = relationship('Pets', backref='sitter_assignments')
    sitter = relationship('Users', back_populates='sitting_assignments')


