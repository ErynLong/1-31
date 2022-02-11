from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Email, DataRequired, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords do not match.')])
    submit = SubmitField('Register')

    def validate_email(form, field):
        same_email_user = User.query.filter_by(email = field.data).first()
        if same_email_user:
            raise ValidationError('Email is already in use.')

class EditProfileForm(FlaskForm):
    first_name= StringField('First Name',validators=[DataRequired()])
    last_name= StringField('Last Name',validators=[DataRequired()])
    email = StringField('Email Address',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Password',validators=[DataRequired(), EqualTo('password',message='Passwords have to match')])
    submit = SubmitField('Update')
    