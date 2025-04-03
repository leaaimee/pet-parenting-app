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
    medical_profile = db.relationship("MedicalProfile", back_populates="pet", lazy=True)
    tasks = db.relationship('Tasks', backref='pet', lazy=True)
    sitters = db.relationship('Sitters', back_populates='pet', lazy=True)


class PetData(db.Model):
    __tablename__ = "pet_data"
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)
    favorite_things = db.Column(db.Text, nullable=False, default="")
    dislikes = db.Column(db.Text, nullable=False, default="")
    social_style = db.Column(db.Text, nullable=False, default="")
    communication = db.Column(db.Text, nullable=False, default="")
    preferred_treats = db.Column(db.Text, nullable=False, default="")
    diet = db.Column(db.Text, nullable=False, default="")
    allergies = db.Column(db.Text, nullable=False, default="")
    medical_alerts = db.Column(db.Text, nullable=False, default="")
    behavior_notes = db.Column(db.Text, nullable=False, default="")
    additional_info = db.Column(db.Text, nullable=False, default="")


# class MedicalRecord(db.Model):
#     __tablename__ = "medical_record"
#     id = db.Column(db.Integer, primary_key=True)
#     pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)
#     weight = db.Column(db.String(20), nullable=True, default="")
#     weight_updated = db.Column(db.String(20), nullable=True)
#     record_type = db.Column(db.String(100))
#     description = db.Column(db.Text)
#     date = db.Column(db.DateTime)
#     vet_name = db.Column(db.String(100))
#     next_due_date = db.Column(db.DateTime)
#     test_results = db.Column(db.Text)
#     medication = db.Column(db.Text)
#     documents = db.Column(db.String(300))


class MedicalProfile(db.Model):
    __tablename__ = "medical_profiles"
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)
    blood_type = db.Column(db.String(10))
    weight = db.Column(db.String(20), nullable=True, default="")
    weight_updated = db.Column(db.String(20), nullable=True)
    chronic_conditions = db.Column(db.Text)
    notes = db.Column(db.Text)

    pet = db.relationship("Pets", back_populates="medical_profile", lazy=True)
    vaccination_records = db.relationship("VaccinationRecord", back_populates="medical_profile", lazy=True)
    medications = db.relationship("Medication", back_populates="medical_profile", lazy=True)
    test_results = db.relationship("TestResult", back_populates="medical_profile", lazy=True)
    vet_visits = db.relationship("VetVisit", back_populates="medical_profile", lazy=True)
    medical_documents = db.relationship("MedicalDocument", back_populates="medical_profile", lazy=True)


class VaccinationRecord(db.Model):
    __tablename__ = "vaccination_records"
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)
    medical_profile_id = db.Column(db.Integer, db.ForeignKey("medical_profiles.id"), nullable=False)
    vaccine_name = db.Column(db.String(100), nullable=False)
    dose_number = db.Column(db.Integer, nullable=True)
    batch_number = db.Column(db.String(50), nullable=True)
    previous_vaccination_date = db.Column(db.Date, nullable=True)
    next_vaccination_date = db.Column(db.String(50), nullable=True)
    additional_Info = db.Column(db.Text, nullable=True)

    medical_profile = db.relationship("MedicalProfile", back_populates="vaccination_records")


class Medication(db.Model):
    __tablename__ = "medications"
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)
    medical_profile_id = db.Column(db.Integer, db.ForeignKey("medical_profiles.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(100))
    duration = db.Column(db.String(100))
    additional_Info = db.Column(db.Text)

    medical_profile = db.relationship("MedicalProfile", back_populates="medications")



class TestResult(db.Model):
    __tablename__ = "test_results"
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)
    medical_profile_id = db.Column(db.Integer, db.ForeignKey("medical_profiles.id"), nullable=False)
    test_type = db.Column(db.String(100))
    result = db.Column(db.Text)
    date = db.Column(db.Date)
    additional_Info = db.Column(db.Text)

    medical_profile = db.relationship("MedicalProfile", back_populates="test_results")


class VetVisit(db.Model):
    __tablename__ = "vet_visits"
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)
    medical_profile_id = db.Column(db.Integer, db.ForeignKey("medical_profiles.id"), nullable=False)
    reason = db.Column(db.String(200))
    vet_name = db.Column(db.String(100))
    clinic_info = db.Column(db.Text)
    date = db.Column(db.Date)
    documents = db.Column(db.String(300))

    medical_profile = db.relationship("MedicalProfile", back_populates="vet_visits")


class MedicalDocument(db.Model):
    __tablename__ = "medical_documents"
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)
    medical_profile_id = db.Column(db.Integer, db.ForeignKey("medical_profiles.id"), nullable=False)
    file_path = db.Column(db.String(300))
    description = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, default=db.func.now())

    medical_profile = db.relationship("MedicalProfile", back_populates="medical_documents")