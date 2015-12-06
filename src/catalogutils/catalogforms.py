from wtforms import Form, StringField, validators, PasswordField
from wtforms import BooleanField, HiddenField, SelectField


class UserForm(Form):
    name = StringField('User Name', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(
        min=6, max=135),
        validators.Email(message=('That\'s not a valid email address.'))])
    accounttype = SelectField(u'Account Type', choices=[(
        'GOOGLE', 'Google'), ('FACEBOOK', 'Facebook'), ('ADMIN', 'Admin')])
    isActive = BooleanField('Active')
    pictureurl = StringField(
        'Profile Picture', [validators.Length(max=255)])
    password = PasswordField('Password',
                             [validators.InputRequired(), validators.EqualTo(
                                 'confirmpassword',
                                 message='Passwords must match')])
    confirmpassword = PasswordField(
        'Repeat Password', [validators.Length(min=4, max=25)])
    id = HiddenField('id')


class AdminLoginForm(Form):
    email = StringField('Email Address', [validators.Length(
        min=6, max=135),
        validators.Email(message=('That\'s not a valid email address.'))])
    password = PasswordField(
        'Password',
        [validators.InputRequired(message="Password cannot be blank!")])


class CategoriesForm(Form):
    name = StringField('Category Name', [validators.Length(min=4, max=255)])
    parent = SelectField(u'Parent Category', coerce=int,
                         validators=[validators.optional()])
    isActive = BooleanField('Active')
    hasChildren = BooleanField('Has Sub Categories')
    id = HiddenField('id')
