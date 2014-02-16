from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, HiddenField, ValidationError, RadioField, SubmitField, PasswordField, TextAreaField, DecimalField
from wtforms.validators import Required

class LoginForm(Form):
    username = TextField('User Name', validators = [Required()])
    password = PasswordField('Password', validators = [Required()])
    submit_button = SubmitField('Login')

class WineEditForm(Form):
    name = TextField('Name', validators = [Required()])
    variety = TextField('Variety', validators = [Required()])
    year = TextField('Year', validators = [Required()])
    country = TextField('Country')
    description = TextAreaField('Description')
    notes = TextAreaField('Notes')
    submit_button = SubmitField('Submit Form')

class WineForm(Form):
    name = TextField('Name', validators = [Required()])
    variety = TextField('Variety', validators = [Required()])
    year = TextField('Year', validators = [Required()])
    country = TextField('Country')
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
