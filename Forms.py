import wtforms.fields

from wtforms import Form, StringField, PasswordField, RadioField, SelectField, TextAreaField, validators, EmailField
from wtforms.fields import EmailField, DateField

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
    username = StringField("Username / Email Address", [validators.Length(min=4,max=16)])
    password = PasswordField("Password" , [validators.Length(min=8, max=16), validators.DataRequired()])


class CreateReviewsForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.DataRequired()])
    feedback = TextAreaField('Any Feedback?',[validators.Length(min=0, max=1000)] ,[validators.Optional()])

class CreateMembershipForm(Form):
    # first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    # last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    # gender = SelectField('Gender', [validators.DataRequired()],
    #                      choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')],
    #                      default='')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    date_joined = DateField('Date Joined', format='%Y-%m-%d')
