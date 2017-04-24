from wtforms import Form, StringField, TextAreaField, IntegerField, PasswordField, validators
from flask_wtf.file import FileField

class UserForm(Form):
    firstname = StringField('Firstname', [validators.Length(min=1, max=25), validators.DataRequired()])
    lastname = StringField('Lastname', [validators.Length(min=1, max=25), validators.DataRequired()])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Email("This field requires a valid email address")])

class WishlistForm(Form):
    name = StringField('Item Name', [validators.Length(min=1, max=25), validators.DataRequired()])
    thumbnail = StringField('Thumbnail', [validators.Length(min=1), validators.DataRequired()])