from . import users
from . import jobs
from . import item
from . import allitems
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField

class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    email = EmailField('Login / email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat Password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ItemsForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    about = StringField('about', validators=[DataRequired()])
    howm = IntegerField('howmany', validators=[DataRequired()])
    submit = SubmitField('Submit')