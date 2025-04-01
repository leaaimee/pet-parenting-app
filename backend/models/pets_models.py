from backend.database import db
from backend.models.tasks_models import Tasks


class Pets(db.Model):
    __tablename__ = "pets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.Date, nullable=True)
    birth_year = db.Column(db.Integer, nullable=True)
    birth_month = db.Column(db.Integer, nullable=True)
    species = db.Column(db.String(100), nullable=False)
    subspecies = db.Column(db.String(100), nullable=True)
    profile_picture = db.Column(db.String(300), nullable=False, default="")
    profile_description = db.Column(db.Text, nullable=False, default="")
    created_at = db.Column(db.DateTime, default=db.func.now())

    parent_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    parent = db.relationship("Users", back_populates="pets")

    roles = db.relationship('Roles', back_populates='pet', lazy=True)
    pet_data = db.relationship('PetData', backref='pet', lazy=True)
    medical_records = db.relationship('MedicalRecord', backref='pet', lazy=True)
    tasks = db.relationship('Tasks', backref='pet', lazy=True)
    sitters = db.relationship('Sitters', back_populates='pet', lazy=True)


class PetData(db.Model):
    __tablename__ = "pet_data"
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)
    allergies = db.Column(db.Text, nullable=False, default="")
    diet = db.Column(db.Text, nullable=False, default="")
    behavior_notes = db.Column(db.Text, nullable=False, default="")
    additional_info = db.Column(db.Text, nullable=False, default="")


class MedicalRecord(db.Model):
    __tablename__ = "medical_record"
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)
    record_type = db.Column(db.String(100))  # Type of record (Vaccination, Checkup, etc.)
    description = db.Column(db.Text) # Detailed notes on diagnosis or procedure
    date = db.Column(db.DateTime) # date of record
    vet_name = db.Column(db.String(100))
    next_due_date = db.Column(db.DateTime) # scheduled follow-ups
    test_results = db.Column(db.Text) #  lab notes - not sure if this is obsolete with documents
    medication = db.Column(db.Text) # Prescription details
    documents = db.Column(db.String(300)) # Stores link to PDF/image of lab results, prescriptions, etc


class MedicalDocuments(db.Model):
    __tablename__ = "medical_documents"
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)
    file_path = db.Column(db.String(300), nullable=False)