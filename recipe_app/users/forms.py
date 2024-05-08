from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import ValidationError, EqualTo, DataRequired, Email
from recipe_app.models import User
from flask_wtf.file import FileAllowed, FileField


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo(
        'password2', message='Passwords do not match')])
    password2 = PasswordField('Confirm Passowrd', validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('The email has already been used.')

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(
                'Username has already been Used'
            )


class UpdateForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('The email has already been registered')

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('The username has already been used')
