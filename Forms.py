import wtforms.fields

from wtforms import Form, StringField, PasswordField, RadioField, SelectField, TextAreaField, validators, EmailField, \
    ValidationError, FileField, IntegerField
from wtforms.fields import EmailField, DateField, SubmitField
from wtforms.validators import DataRequired


class CreateUserForm(Form):
    # first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    # last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    # gender = SelectField('Gender', [validators.DataRequired()],
    #                      choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')],
    #                      default='')
    # membership = RadioField('Membership', choices=[('F', 'Fellow'), ('S', 'Senior'), ('P', 'Professional')],
    #                         default='F')
    # remarks = TextAreaField('Remarks', [validators.Optional()])


    # customer username password fields
    username = StringField("Username / Email Address", [validators.Length(min=4,max=16),validators.Regexp("^[^\s]+$", message="Username cannot contain whitespace.") ], render_kw={'autocomplete': 'off'})
    password = PasswordField("Password" , [validators.Length(min=8, max=16), validators.DataRequired(), validators.Regexp("^[^\s]+$", message="Password cannot contain whitespace.")], render_kw={'autocomplete': 'off'})
    email = EmailField("Email",)
    gender = SelectField('Gender',
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default = '')
    postal_code = StringField("Postal Code")
    profilePic = FileField("Profile Picture", )




class UpdateUserForm(Form):
    # username = StringField("Username / Email Address", [validators.Length(min=4, max=16)])
    # password = PasswordField("Password", [validators.Length(min=8, max=16), validators.DataRequired()])
    # email = EmailField("Email")
    username = StringField('Username', [validators.Length(max=16),validators.Regexp("^(?:[^\s]|.{4,})$", message="Username cannot contain whitespace.")])
    password = PasswordField('Password', [validators.Length(min=8,max=16), validators.Regexp("^$|^[^\s]+$", message="Password cannot contain whitespace.")])
    email = EmailField('Email', [validators.Regexp("^$|^[^\s]+$", message="Email cannot contain whitespace.")])
    gender = SelectField('Gender',
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    postal_code = StringField("Postal Code", [validators.length(min=6,), validators.Regexp("^$|^[^\s]+$", message="Postal Code cannot contain whitespace.")])
    profilePic = FileField("Profile Picture")


class CreateReviewsForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    stars = SelectField('Stars',
                        choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')],
                        coerce=int, validators=[DataRequired()])
    feedback = TextAreaField('Any Feedback?',[validators.Optional()])

class CreateMembershipForm(Form):
    # first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    # last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    # gender = SelectField('Gender', [validators.DataRequired()],
    #                      choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')],
    #                      default='')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    date_joined = DateField('Date Joined', format='%Y-%m-%d')
