from wsgiref.validate import validator

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

from datetime import datetime
current_year = datetime.now().year


class PetForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=50)])
    birthday = DateField("Birthday", format='%Y-%m-%d', validators=[Optional()])

    birth_year = SelectField(
        "Birth Year",
        choices=[('', '—')] + [(str(y), str(y)) for y in range(current_year, current_year - 100, -1)],
        validators=[Optional()]
    )

    birth_month = SelectField(
        "Birth Month",
        choices=[('', '—')] + [(str(i), str(i)) for i in range(1, 13)],
        validators=[Optional()]
    )

    species = StringField("Species", validators=[Optional(), Length(min=2, max=100)])
    subspecies = StringField("Subspecies", validators=[Optional(), Length(min=2, max=100)])
    gender = StringField("Gender", validators=[Optional(), Length(max=20)])
    profile_picture = StringField("Profile Picture", validators=[Optional()])
    profile_description = TextAreaField("Description", validators=[Optional()])
    submit = SubmitField("Add Pet")


class PetDataForm(FlaskForm):
    favorite_things = TextAreaField("Favorite Things", validators=[Optional()])
    dislikes = TextAreaField("Dislikes", validators=[Optional()])
    social_style = TextAreaField("Social Style", validators=[Optional()])
    communication = TextAreaField("Communication", validators=[Optional()])
    preferred_treats = TextAreaField("Preferred Treats", validators=[Optional()])
    diet = TextAreaField("Diet", validators=[Optional()])
    allergies = TextAreaField("Allergies", validators=[Optional()])
    medical_alerts = TextAreaField("Medical Alerts", validators=[Optional()])
    behavior_notes = TextAreaField("Behaviour Notes", validators=[Optional()])
    additional_info = TextAreaField("Additional_info", validators=[Optional()])
    submit = SubmitField("Add Pet Data")


class MedicalProfileForm(FlaskForm):
    blood_type = StringField("Blood Type", validators=[Optional()])
    weight = StringField("Weight", validators=[Optional()])
    weight_updated = StringField("Last Weighed On", validators=[Optional()])
    chronic_conditions = TextAreaField("Chronic Conditions", validators=[Optional()])
    notes = TextAreaField("Notes", validators=[Optional()])
    submit = SubmitField("Save Medical Profile")


class VaccinationRecord(FlaskForm):
    vaccine_name = StringField("Vaccine Name", validators=[Optional()])
    dose_number = IntegerField("Dose Number", validators=[Optional(), NumberRange(min=1, max=10)])
    batch_number = StringField("Batch Number", validators=[Optional()])
    previous_vaccination_date = DateField("Next Vaccination Date", validators=[Optional()])
    next_vaccination_date = StringField("Next Vaccination Date", validators=[Optional()])
    additional_Info = TextAreaField("Additional Info", validators=[Optional()])
    submit = SubmitField("Add Data")


class MedicationForm(FlaskForm):
    name = StringField("Name", validators=[Optional()])
    dosage = StringField("Dosage", validators=[Optional()])
    duration = StringField("Duration", validators=[Optional()])
    additional_Info = TextAreaField("Additional Info", validators=[Optional()])
    submit = SubmitField("Add Data")


class TestResultsForm(FlaskForm):
    test_type = StringField("Test Type", validators=[Optional()])
    result = TextAreaField("Result", validators=[Optional()])
    date = DateField("Date", validators=[Optional()])
    additional_Info = TextAreaField("Additional Info", validators=[Optional()])
    submit = SubmitField("Add Data")


class MedicalDocumentForm(FlaskForm):
    file_path = StringField("File Path", validators=[Optional()])
    description = TextAreaField("Description", validators=[Optional()])
    uploaded_at = DateField("Uploaded At", validators=[Optional()])
    submit = SubmitField("Add Data")