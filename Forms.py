import wtforms.fields

from wtforms import Form, StringField, PasswordField, RadioField, SelectField, TextAreaField, validators, EmailField, \
    ValidationError, FileField, IntegerField, BooleanField
from wtforms.fields import EmailField, DateField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed


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
    date_joined = DateField('Date Joined', format='%Y-%m-%d')
    address = StringField('Mailing Address', [validators.length(max=200), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])


class UpdateMembershipForm(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    address = StringField('Mailing Address', [validators.length(max=200), validators.DataRequired()])


class RedeemForm(Form):
    rewards = SelectField('rewards', choices=[(1, '$5 off'), (2, '$10 off'), (3, '$15 off')])

class CreateProductForm(Form):
    idproducts = IntegerField('Product ID', render_kw={'readonly': True})
    name = StringField(' Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    price = StringField('Price', [validators.Length(min=1, max=150),validators.DataRequired()])
    category = StringField('Category', [validators.Length(min=1, max=150), validators.DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    description = TextAreaField('Description', [validators.Length(min=1, max=400), validators.DataRequired()])
    ingredients_info = TextAreaField('Ingredients Info', [validators.Length(min=1, max=600), validators.DataRequired()])

    
    is_recommended = BooleanField('Display in Recommended?')




    # function to validate price entered to make sure that the price entered is either integers or float
    def validate_price(form, field):
        try:
            # Attempt to convert the input from the above field, price, to a float
            float_value = float(field.data)
        except ValueError:
            raise validators.ValidationError('Price must be a valid number.')

    def validate_category(form, field):
        # Check if the field being validated is 'category'
        if field.name == 'category':
            # Convert the input to lowercase
            field.data = field.data.lower()


class DineInForm(Form):
    time = StringField('Approximated Dine-in Timing',[validators.Length(min=1, max=4), validators.DataRequired()])
    pax = StringField('No. of People Dining-In', [validators.Length(min=1, max=150), validators.DataRequired()])


class DeliveryForm(Form):
    street = StringField('Street', [validators.Length(min=1, max=150), validators.DataRequired()])
    block = StringField('Block', [validators.Length(min=1, max=150), validators.DataRequired()])
    unit_no = StringField('Unit No', [validators.Length(min=1, max=150), validators.DataRequired()])
    postal_code = StringField('Postal Code', [validators.Length(min=1, max=150), validators.DataRequired()])

class CreateStaffForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    role = RadioField('Role', choices=[('A', 'Admin'), ('M', 'Manager'), ('S', 'Staff')], default='S')
    email = EmailField('Email', [validators.DataRequired()])