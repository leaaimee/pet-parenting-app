from backend.database import db
from backend.utils.constants import AccessLevel, InvitationStatus, RoleType


class Invitations(db.Model):
    __tablename__ = "invitations"
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)
    inviter_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    invitee_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    role = db.Column(db.Enum(RoleType), nullable=False)  # Roommate, Sitter, etc.
    access_level = db.Column(db.Enum(AccessLevel), nullable=False)
    status = db.Column(db.Enum(InvitationStatus), default=InvitationStatus.PENDING, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())


class Permissions(db.Model):
    __tablename__ = "permissions"
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    access_level = db.Column(db.Enum(AccessLevel), nullable=False, default=AccessLevel.VIEW_ALL)




