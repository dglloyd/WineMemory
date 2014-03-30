from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, HiddenField, ValidationError, RadioField, SubmitField, PasswordField, TextAreaField, DecimalField
from wtforms.validators import Required, Email

class LoginForm(Form):
    name = TextField('User Name', validators = [Required()])
    password = PasswordField('Password', validators = [Required()])
    submit_button = SubmitField('Login')

class RegisterForm(Form):
    name = TextField('User Name', validators = [Required()])
    password = PasswordField('Password', validators = [Required()])
    email = TextField("Email Address", validators = [Email()])
    submit_button = SubmitField('Register')

class WineEditForm(Form):
    name = TextField('Winery', validators = [Required()])
    variety = TextField('Variety', validators = [Required()])
    year = TextField('Year', validators = [Required()])
    country = TextField('Country')
    description = TextAreaField('Description')
    submit_button = SubmitField('Submit Form')

class WineForm(Form):
    name = TextField('Name', validators = [Required()])
    variety = TextField('Variety', validators = [Required()])
    year = TextField('Year')
    country = TextField('Country')
    region = TextField('Region')
    description = TextAreaField('Description')
    notes = TextAreaField('Notes')
    price = DecimalField('Price (Optional)')
    store = TextField('Store (Optional)')
    drank = BooleanField('Already Drank') 
    rating = TextField('Rating')
    submit_button = SubmitField('Submit Form')

class PurchaseForm(Form):
    price = TextField('Price')
    store = TextField('Store')
    drank = BooleanField('Drank') 
    submit_button = SubmitField('Submit')

class RatingForm(Form):
    rating = TextField('Rating')
    notes = TextAreaField('Notes')

