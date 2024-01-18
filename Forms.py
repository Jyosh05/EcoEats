import wtforms.fields
from wtforms import Form, StringField, PasswordField, RadioField, SelectField, TextAreaField, validators
from wtforms.fields import EmailField, DateField, FloatField

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

class UpdateUserForm(Form):
    username = StringField("Username / Email Address", [validators.Length(min=4, max=16)])
    password = PasswordField("Password", [validators.Length(min=8, max=16), validators.DataRequired()])


class CreateReviewsForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.DataRequired()])
    feedback = TextAreaField('Any Feedback?',[validators.Length(min=0, max=1000)] ,[validators.Optional()])

class CreateMembershipForm(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    date_joined = DateField('Date Joined', format='%Y-%m-%d')
    address = TextAreaField('Mailing Address', [validators.length(max=200), validators.DataRequired()])

class CreateRewardsForm(Form):
    reward_name = StringField("Reward Name", [validators.Length(min=10,max=600)])
    reward_value = FloatField("Reward Price", [validators.NumberRange(min=10, max=200)])
    reward_type = RadioField("Reward Type", choices=[('S', 'StoreFixed'), ('P', 'Promotional')],default='S')