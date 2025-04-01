from backend.database import db
from backend.utils.constants import RoleType, AccessLevel, InvitationStatus
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    profile_picture = db.Column(db.String(300))
    profile_description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    roles = db.relationship('Roles', back_populates='user', lazy=True)
    assigned_tasks = db.relationship('Tasks', backref='assigned_user', lazy=True)
    sitting_assignments = db.relationship('Sitters', back_populates='sitter')
    pets = db.relationship("Pets", back_populates="parent")


class Roles(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.Enum(RoleType), nullable=False)
    access_level = db.Column(db.Enum(AccessLevel), nullable=False, default=AccessLevel.VIEW_ALL)

    pet = db.relationship('Pets', back_populates='roles')
    user = db.relationship('Users', back_populates='roles')


class Sitters(db.Model):
    __tablename__ = "sitters"
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)
    sitter_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    invitation_status = db.Column(db.Enum(InvitationStatus), default=InvitationStatus.PENDING, nullable=False) # default: pending
    completed = db.Column(db.Boolean, default=False)
    access_level = db.Column(db.Enum(AccessLevel), nullable=False, default=AccessLevel.VIEW_LIMITED)

    pet = db.relationship('Pets', backref='sitter_assignments')
    sitter = db.relationship('Users', back_populates='sitting_assignments')


