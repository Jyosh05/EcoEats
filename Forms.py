import wtforms.fields
from wtforms import Form, StringField, PasswordField, RadioField, SelectField, TextAreaField, validators, FloatField
from flask_wtf.file import FileField, FileAllowed
# class CreateUserForm(Form):
        # first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    # last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    # gender = SelectField('Gender', [validators.DataRequired()],
    #                      choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')],
    #                      default='')
    # membership = RadioField('Membership', choices=[('F', 'Fellow'), ('S', 'Senior'), ('P', 'Professional')],
    #                         default='F')
    # remarks = TextAreaField('Remarks', [validators.Optional()])


    # customer username password fields
    # username = StringField("Username / Email Address", [validators.Length(min=4,max=16)])
    # password = PasswordField("Password" , [validators.Length(min=8, max=16), validators.DataRequired()])


class CreateProductForm(Form):
    name = StringField(' Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    price = StringField('Price', [validators.Length(min=1, max=150),validators.DataRequired()])
    category = StringField('Category', [validators.Length(min=1, max=150), validators.DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    description = TextAreaField('Description', [validators.Length(min=1, max=400), validators.DataRequired()])
    ingredients_info = TextAreaField('Ingredients Info', [validators.Length(min=1, max=600), validators.DataRequired()])



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



