
from backend.database import Base
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from backend.utils.constants import AccessLevel, InvitationStatus, RoleType


class Invitations(Base):
    __tablename__ = "invitations"
    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    inviter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    invitee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(Enum(RoleType), nullable=False)  # Roommate, Sitter, etc.
    access_level = Column(Enum(AccessLevel), nullable=False)
    status = Column(Enum(InvitationStatus), default=InvitationStatus.PENDING, nullable=False)
    created_at = Column(DateTime, default=func.now())


class Permissions(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    access_level = Column(Enum(AccessLevel), nullable=False, default=AccessLevel.VIEW_ALL)




