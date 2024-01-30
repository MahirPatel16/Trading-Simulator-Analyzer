from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired

class RegisterForm(FlaskForm):
    username = StringField(label='', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='Enter your Username / Email Address', validators=[Length(min=2,max=30), DataRequired()])
    password = PasswordField(label='Enter your password', validators=[Length(min=6), DataRequired()])
    submit = SubmitField(label='Login')
