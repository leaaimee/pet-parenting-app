from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, Length, Optional
from flask_wtf.file import FileField, FileAllowed

class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class EditUserProfileForm(FlaskForm):
    phone = StringField("Phone", validators=[DataRequired()])
    location = StringField("Location", validators=[Optional()])
    birth_date = DateField("Birth Date", format="%Y-%m-%d", validators=[Optional()])
    pronouns = StringField("Pronouns", validators=[Optional()])
    profile_description = TextAreaField("About Me", validators=[Optional()])

    profile_picture = FileField("Upload User Profile Image", validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])

    languages_spoken = StringField("Languages Spoken", validators=[Optional()])
    experience_with = TextAreaField("Experience With", validators=[Optional()])
    certifications = TextAreaField("Certifications", validators=[Optional()])
    # File field can come later with Flask-Uploads or WTForms-Alchemy

    submit = SubmitField("Save Profile")