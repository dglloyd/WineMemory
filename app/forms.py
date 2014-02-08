from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, HiddenField, ValidationError, RadioField, SubmitField, PasswordField
from wtforms.validators import Required

class LoginForm(Form):
    username = TextField('User Name', validators = [Required()])
    password = PasswordField('Password', validators = [Required()])
    submit_button = SubmitField('Login')

class WineForm(Form):
    name = TextField('Name', validators = [Required()])
    variety = TextField('Variety', validators = [Required()])
    year = TextField('Year', validators = [Required()])
    country = TextField('Country')
    price = TextField('Price')
    submit_button = SubmitField('Submit Form')
