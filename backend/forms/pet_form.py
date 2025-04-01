from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Optional

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
    profile_picture = StringField("Profile Picture", validators=[Optional()])
    description = TextAreaField("Description", validators=[Optional()])
    submit = SubmitField("Add Pet")