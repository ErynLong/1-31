from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class AshKetchum(FlaskForm):
    enter_field = StringField('Please enter a pokemon name', validators=[DataRequired()])
    submit_button = SubmitField('Submit')