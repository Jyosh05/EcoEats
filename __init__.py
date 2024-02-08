# first file to run when starting the web application
import datetime

from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import User, Membership

import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from Forms import CreateUserForm, CreateMembershipForm, CreateReviewsForm, UpdateUserForm
import ReviewUser

# 1:56pm
# pip install mysql-connector-python
import mysql.connector
from flask import session
from functools import wraps
from flask import flash



import pandas as pd
import matplotlib.pyplot as plt

from werkzeug.utils import secure_filename
import os
from Forms import CreateProductForm, DineInForm, DeliveryForm
from Product import Product
from cart import CartItem
from order_type import DineIn, Delivery


app = Flask(__name__)
app.secret_key = 'my_super_secret_key_123'
UPLOAD_FOLDER = 'static/img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif'])

# # mySql Credentials
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='JYOSHNA2006!',
    port='3306',
    database='ecoeatsusers'
)

# db = mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='JYOSHNA2006!',
#     port=3306,
#     database='ecoeatsusers'
# )
#
# mydb = mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='JYOSHNA2006!',
#     port=3306,
#     database='ecoeatsusers'
# )
#
# my_db = mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='JYOSHNA2006!',
#     port=3306,
#     database='ecoeatsusers'
# )

mycursor = mydb.cursor(buffered=True)

tableCheck = ['users']
for a in tableCheck:
    mycursor.execute(f"SHOW TABLES LIKE 'users'")
    tableExist = mycursor.fetchone()


    if not tableExist:

        mycursor.execute("CREATE TABLE `ecoeatsusers`.`users` (`id` INT AUTO_INCREMENT NOT NULL, `username` VARCHAR(45) NULL, `password` VARCHAR(45) NULL, PRIMARY KEY (`id`)); ")
        print(f"Table 'users' Created")






mycursor.execute('SELECT * FROM users')
print(f"Using table 'users' ")

users = mycursor.fetchall()
# index 0 is used for count / unique id
for a in users:
    print(a)
    print('Username: ', a[1])
    print('Password: ', a[2])



# @app.route('/')
# def home():
#     return render_template("home.html")

# cursor = db.cursor()
# cur = mydb.cursor()
# mycursor = mydb.cursor()


tableCheck = ['products']
for a in tableCheck:
    mycursor.execute(f"SHOW TABLES LIKE 'products'")
    tableExist = mycursor.fetchone()

    if not tableExist:
        mycursor.execute("CREATE TABLE `ecoeatsusers`"
                       "`products` "
                       "(`idproducts` INT NOT NULL, `name` VARCHAR(100) NULL, "
                       "`price` DECIMAL(10,2) NULL, "
                       "`category` VARCHAR(45) NULL, "
                       "`image` VARCHAR(200) NULL,"
                       "`description` VARCHAR(400) NULL,"
                       "`ingredients_info` VARCHAR(1000) NULL,"
                       "`is_recommended` TINYINT(1) NULL DEFAULT 0,"
                       "PRIMARY KEY (`idproducts`)); ")
        print(f"Table 'products' Created")

mycursor.execute('SELECT * FROM products')
print(f"Using table 'products' ")







products = mycursor.fetchall()
cart = mycursor.fetchall()
# order_info = mycursor.fetchall()



@app.route('/createUser', methods=['GET', 'POST'])
def create_user():
    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        try:
            mydb = mysql.connector.connect(
                host='localhost',
                user='root',
                password='JYOSHNA2006!',
                port='3306',
                database='ecoeatsusers'
            )

            mycursor = mydb.cursor()

            # mycursor.execute("SELECT COUNT(*) FROM users")
            # id = mycursor.fetchone()[0]
            # id = User.User.get_userCount()
            # autoIncrement = "ALTER TABLE users ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY FIRST;"
            # mycursor.execute(autoIncrement)
            print(id)
            form = CreateUserForm()
            check_query = "SELECT COUNT(*) FROM users WHERE username = %s"
            mycursor.execute(check_query, (create_user_form.username.data,))
            username_count = mycursor.fetchone()[0]

            if username_count > 0:
                flash("Username already exists. Please choose a different username.")
                return render_template('createUser.html', form=create_user_form)

            insert_query = "INSERT INTO users ( username, password) " \
                               "VALUES (%s, %s)"
            user = User.User(create_user_form.username.data, create_user_form.password.data)
            user_data = (user.get_username(), user.get_password())
            mycursor.execute(insert_query, user_data)
            mydb.commit()

            lastest_id = mycursor.lastrowid

            print(
                f"{user.get_userCount()} {lastest_id} {user.get_username()} {user.get_password()} was stored in the database successfully.")
            return redirect(url_for('retrieve_user'))
        except Exception as e:
            print("Error:", e)
            mydb.rollback()
            return "Error occurred. Check logs for details."
    return render_template('createUser.html', form=create_user_form)


@app.route('/retrieveUser')
def retrieve_user():
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='JYOSHNA2006!',
        port='3306',
        database='ecoeatsusers'
    )

    mycursor = mydb.cursor()
    select_query = "SELECT * FROM users"
    mycursor.execute(select_query)
    users = mycursor.fetchall()
    return render_template('retrieveUser.html', users=users, User=User)


@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_user_form = CreateUserForm(request.form)

    if request.method == 'POST' and update_user_form.validate():
        try:
            # reetrieve user data from db
            select_query = "SELECT username, password FROM users WHERE id = %s"
            mycursor.execute(select_query, (id,))
            user_details = mycursor.fetchone()

            if user_details:
                username = update_user_form.username.data
                password = update_user_form.password.data

                update_query = "UPDATE users SET username = %s, password = %s WHERE id = %s"
                data = (username, password, id)
                mycursor.execute(update_query, data)
                mydb.commit()

                print(f"User ID: {id} updated successfully.")
                return redirect(url_for('retrieve_user'))
            else:
                return "User not found."
        except Exception as e:
            print("Error:", e)
            mydb.rollback()
            return "Error occurred while updating user."

    else:
        try:
            # retrieve user data from mysql db
            select_query = "SELECT username, password FROM users WHERE id = %s"
            mycursor.execute(select_query, (id,))
            user_details = mycursor.fetchone()

            if user_details:
                update_user_form.username.data = user_details[0]
                update_user_form.password.data = user_details[1]

                return render_template('updateUser.html', form=update_user_form)
            else:
                return "User not found."
        except Exception as e:
            print("Error:", e)
            return "Error occurred while fetching user details."


@app.route('/deleteUser/<int:id>/', methods=['GET', 'POST'])
def delete_user(id):
    try:
        # Check if the user exists before attempting deletion
        select_query = "SELECT * FROM users WHERE id = %s"
        mycursor.execute(select_query, (id,))
        user = mycursor.fetchone()

        if user:
            delete_query = "DELETE FROM users WHERE id = %s"
            mycursor.execute(delete_query, (id,))
            mydb.commit()

            print(f"User ID: {id} deleted successfully.")
            return redirect(url_for('retrieve_user'))
        else:
            return "User not found."
    except Exception as e:
        print("Error:", e)
        mydb.rollback()
        return "Error occurred while deleting user."


@app.route('/deleteUser/', methods=['POST'])
def delete_users():
    try:
        ids_to_delete = request.form.getlist('selected_users[]')

        if ids_to_delete:
            placeholders = ', '.join(['%s'] * len(ids_to_delete))

            select_query = f"SELECT * FROM users WHERE id IN ({placeholders})"
            mycursor.execute(select_query, tuple(ids_to_delete))
            users = mycursor.fetchall()

            if users:
                # delete all the selected users from db
                delete_query = f"DELETE FROM users WHERE id IN ({placeholders})"
                mycursor.execute(delete_query, tuple(ids_to_delete))
                mydb.commit()

                print(f"Users with IDs: {', '.join(ids_to_delete)} deleted successfully.")
                return redirect(url_for('retrieve_user'))
            else:
                return "Users not found."
        else:
            return "No users selected for deletion."
    except Exception as e:
        print("Error:", e)
        mydb.rollback()
        return "Error occurred while deleting users."


@app.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = CreateUserForm(request.form)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        select_query = "SELECT * FROM users WHERE username = %s AND password = %s"
        mycursor.execute(select_query, (username, password))
        user = mycursor.fetchone()

        if user:
            user_id = user[0]
            session['user_id'] = user_id

            if is_admin(user_id):
                #admin login
                return redirect(url_for('dashboard'))
            else:
                # cust user login
                return redirect(url_for('home'))

        else:
            # invalid login error msg
            flash("Invalid credentials. Please try again or sign up.", "error")

    return render_template('login.html', form=loginForm)

def is_admin(user_id):
    admin_ids = [2]  #admin user ids
    return user_id in admin_ids

def login_required(role=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))

            user_id = session['user_id']

            if role is not None and not is_admin(user_id):

                return redirect(url_for('login'))

            return func(*args, **kwargs)

        return wrapper

    return decorator


@app.route('/logout')
def logout():
    session.pop('user_id', None)

    return redirect(url_for('login'))

@app.route('/updateProfile', methods=['GET', 'POST'])
@login_required()
def update_profile():
    user_id = session['user_id']  # Get the current user's ID from the session

    update_user_form = UpdateUserForm(request.form)

    if request.method == 'POST' and update_user_form.validate() :
        try:
            # Retrieve user data from the database
            select_query = "SELECT username, password, email, gender, postal_code FROM users WHERE id = %s"
            mycursor.execute(select_query, (user_id,))
            user_details = mycursor.fetchone()

            if user_details:
                # Get the form data
                username = update_user_form.username.data
                password = update_user_form.password.data
                email = update_user_form.email.data
                gender = update_user_form.gender.data
                postal_code = update_user_form.postal_code.data

                # Check if form fields are empty, and use existing data if they are
                username = username if username else user_details[0]
                password = password if password else user_details[1]
                email = email if email else user_details[2]
                gender = gender if gender else user_details[3]
                postal_code = postal_code if postal_code else user_details[4]

                # Update user information in the database
                update_query = "UPDATE users SET username = %s, password = %s, email = %s, gender = %s, postal_code = %s WHERE id = %s"
                data = (username, password, email, gender, postal_code, user_id)
                mycursor.execute(update_query, data)
                mydb.commit()

                print(f"User ID: {user_id} updated successfully.")
                return redirect(url_for('retrieve_user'))
            else:
                return "User not found."
        except Exception as e:
            print("Error:", e)
            mydb.rollback()
            return "Error occurred while updating user."

    else:
        try:
            # Retrieve user data from the database
            select_query = "SELECT username, password, email, gender, postal_code FROM users WHERE id = %s"
            mycursor.execute(select_query, (user_id,))
            user_details = mycursor.fetchone()
            print(user_details)
            user_select = "SELECT username FROM users WHERE id = %s"
            mycursor.execute(user_select, (user_id,))
            user = mycursor.fetchone()

            if user_details:
                update_user_form.username.data = user_details[0]
                update_user_form.password.data = user_details[1]
                update_user_form.email.data = '' #user_details[2]
                update_user_form.gender.data = ''
                update_user_form.postal_code.data = ''

                return render_template('updateProfile.html', form=update_user_form, user=user, User=User)
            else:
                return "User not found."
        except Exception as e:
            print("Error:", e)
            return "Error occurred while fetching user details."


@app.route('/report')
def report():
    select_query = "SELECT * from fakeSales"
    mycursor.execute(select_query)

    compile = mycursor.fetchall()

    compile_saleId = []
    compile_product_name = []
    compile_product_price = []
    for saleId, product_name, product_price in compile:
        compile_saleId.append(saleId)
        compile_product_name.append(product_name)
        compile_product_price.append(product_price)

    dict = {'saleId' : compile_saleId, 'product_name' : compile_product_name, 'product_price':compile_product_price}
    df = pd.DataFrame (dict)
    df_csv = df.to_csv("C:/Users/dawin/Downloads/TestReport.csv")

    return "yes!"



@app.route('/chart')
def chart():
    # Connect to MySQL

    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='JYOSHNA2006!',
        port='3306',
        database='ecoeatsusers'
    )

    mycursor = mydb.cursor()

    # Execute SQL Query
    mycursor.execute("SELECT `saleId`, `product_name`, `product_price` FROM `fakesales`")

    # Fetch all the data
    rows = mycursor.fetchall()

    # Process the data for plotting
    product_names = [row[1] for row in rows]
    product_prices = [float(row[2]) for row in rows]



    # Create the bar chart for product prices
    plt.figure(figsize=(10, 6))
    plt.bar(product_names, product_prices)
    plt.xlabel('Product')
    plt.ylabel('Total Revenue')
    plt.title('Total Revenue by Product')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    html_chart_prices = f'<img src="data:image/png;base64,{plot_to_base64()}" alt="Product Prices Chart">'

    # Execute SQL Query for total revenue by product
    mycursor.execute(
        "SELECT `product_name`, COUNT(*) * AVG(`product_price`) AS revenue FROM `fakesales` GROUP BY `product_name`")
    rows = mycursor.fetchall()
    product_names_rev = [row[0] for row in rows]
    revenues = [float(row[1]) for row in rows]

    # Create the bar chart for total revenue by product
    plt.figure(figsize=(10, 6))
    plt.bar(product_names_rev, revenues, color='orange')
    plt.xlabel('Product')
    plt.ylabel('Total Revenue')
    plt.title('Total Revenue by Product')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    html_chart_revenues = f'<img src="data:image/png;base64,{plot_to_base64()}" alt="Total Revenue Chart">'
    # Get base64 encoded image


    # Close MySQL Connection
    mycursor.close()
    mydb.close()

    return render_template('chart.html' ,chart_prices=html_chart_prices, chart_revenues=html_chart_revenues, User=User)





# Function to convert Matplotlib plot to base64 image
def plot_to_base64():
    from io import BytesIO
    import base64

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode()
    buffer.close()
    return img_str





# @app.route('/updateProfile' ,methods=['GET', 'POST'])
# @login_required()
# def update_profile():
#     user_id = session['user_id']  # Get the current user's ID from the session
#
#     update_user_form = UpdateUserForm(request.form)
#
#     if request.method == 'POST' and update_user_form.validate():
#         try:
#             # Retrieve user data from the database
#             select_query = "SELECT username, password, email FROM users WHERE id = %s"
#             mycursor.execute(select_query, (user_id,))
#             user_details = mycursor.fetchone()
#
#             if user_details:
#                 username = update_user_form.username.data
#                 password = update_user_form.password.data
#                 email = update_user_form.email.data
#
#                 # Update user information in the database
#                 update_query = "UPDATE users SET username = %s, password = %s, email = %s WHERE id = %s"
#                 data = (username, password, email, user_id)
#                 mycursor.execute(update_query, data)
#                 mydb.commit()
#
#                 print(f"User ID: {user_id} updated successfully.")
#                 return redirect(url_for('retrieve_user'))
#             else:
#                 return "User not found."
#         except Exception as e:
#             print("Error:", e)
#             mydb.rollback()
#             return "Error occurred while updating user."
#
#     else:
#         try:
#             # Retrieve user data from the database
#             select_query = "SELECT username, password, email FROM users WHERE id = %s"
#             mycursor.execute(select_query, (user_id,))
#             user_details = mycursor.fetchone()
#             print(user_details)
#             user_select = "SELECT username FROM users WHERE id = %s"
#             mycursor.execute(user_select, (user_id,))
#             user = mycursor.fetchone()
#
#             if user_details:
#                 update_user_form.username.data = user_details[0]
#                 update_user_form.password.data = user_details[1]
#                 update_user_form.email.data = user_details[2]
#
#                 return render_template('updateProfile.html', form=update_user_form, user=user)
#             else:
#                 return "User not found."
#         except Exception as e:
#             print("Error:", e)
#             return "Error occurred while fetching user details."



# def is_admin(user_id):
#     # Add logic to check if the user with the given ID is an admin
#     # You can fetch additional information from the database to determine the user role
#     # For example, if there is a 'role' column in the users table
#     select_role_query = "SELECT role FROM users WHERE id = %s"
#     mycursor.execute(select_role_query, (user_id,))
#     role = mycursor.fetchone()
#
#     return role and role[0] == 'admin'


# # @app.route('/login', methods=['GET', 'POST'])
# # def login():
# #     loginForm = CreateUserForm(request.form)
# #
# #     if request.method == 'POST':
# #         username = request.form['username']
# #         password = request.form['password']
# #
# #         #query to fetch user by username and password
# #         select_query = "SELECT * FROM users WHERE username = %s AND password = %s"
# #         mycursor.execute(select_query, (username, password))
# #         user = mycursor.fetchone()[0]
# #
# #         id = user #retrieve id of user
#         # query to fetch user by username and password
#         select_query = "SELECT * FROM users WHERE username = %s AND password = %s"
#         mycursor.execute(select_query, (username, password))
#         user = mycursor.fetchone()
#         id = user[0]  # retrieve id of user
#
#         if user:
#             # logged in, redirect  back to website
#             print(f"User ID: {id} , Username: {username} Password:wont display but possible logged in successfully.  ")
#             return redirect(url_for('profile'))
#
#         else:
#             # invalid login error msg
#             return "Invalid credentials. Please try again or sign up."
#
#     return render_template('login.html', form=loginForm)


#
#
#         if user:
#             #logged in, redirect  back to website
#             print(f"User ID: {id} , Username: {username} Password: {password}  ")
#             return redirect(url_for('profile'))
#
#         else:
#             #invalid login error msg
#             return "Invalid credentials. Please try again or sign up."
#
#     return render_template('login.html', form=loginForm)





# previous /createUser, only left here for reference. do not use.
# @app.route('/createUser', methods = ['GET', 'POST'])
# def create_user():
#     create_user_form = CreateUserForm(request.form)
#     if request.method == 'POST' and create_user_form.validate():
#         users_dict = {}
#         db = shelve.open('user.db', 'c')
#         try:
#             users_dict = db['Users']
#         except:
#              print("Error in retrieving Users from user.db.")
#         user = User.User(create_user_form.first_name.data, create_user_form.last_name.data,
#                          create_user_form.gender.data, create_user_form.membership.data, create_user_form.remarks.data)
#         users_dict[user.get_user_id()] = user
#         db['Users'] = users_dict
#         # Test codes
#         users_dict = db['Users']
#         user = users_dict[user.get_user_id()]
#         print(user.get_first_name(), user.get_last_name(), "was stored in user.db successfully with user_id ==",
#               user.get_user_id())
#         db.close()
#
#         return redirect(url_for('home'))
#     return render_template('createUser.html', form = create_user_form)


intents = json.loads(open('intents.json').read())

lemmatizer = WordNetLemmatizer()
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbotmodel.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 133
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result


@app.route("/get")
def get_bot_response():
    user_message = request.args.get("msg")
    ints = predict_class(user_message)
    res = get_response(ints, intents)
    return res

@app.route('/dashboard')
@login_required(role='admin')
def dashboard():
    select_query = "SELECT * FROM reviews"
    mycursor.execute(select_query)
    reviews = mycursor.fetchall()
    print('a')
    return render_template("dashboard.html", User=User, reviews=reviews)
# to redirect back to previous page
# @app.route("/previous")
# def previous():
#     prev_route = session.get("prev_route")
#     if prev_route:
#         return redirect(url_for(prev_route))
#     else:
#         return "No previous route"
#
# @app.before_request
# def before_request():
#     session["prev_route"] = request.endpoint


@app.route('/')
def home():
    return render_template("home.html", User=User)


@app.route('/productBase/<category>')
def category(category):
    mycursor.execute('SELECT * FROM products WHERE category = %s', (category,))
    data = mycursor.fetchall()

    return render_template('productBase.html', category=category, products=data)





@app.route('/recommended')
def recommended():
    mycursor.execute('SELECT * FROM products WHERE is_recommended = true')
    recommended_products = mycursor.fetchall()

    return render_template('recommended.html', recommended_products=recommended_products)

@app.route('/appetizers')
def appetizers():
    return redirect(url_for('category', category='Appetizer')) # the category field here is
    # what helps to input the page title in then respective html pages
    
    
@app.route('/breakfast')
def breakfast():
    return redirect(url_for('category', category='Breakfast'))


@app.route('/lunch')
def lunch():
    return redirect(url_for('category', category='Lunch'))


@app.route('/dinner')
def dinner():
    return redirect(url_for('category', category='Dinner'))


@app.route('/dessert')
def dessert():
    return redirect(url_for('category', category='Dessert'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/create_product', methods=['GET', 'POST'])
def create_product():
    create_product_form = CreateProductForm(request.form)

    if request.method == 'POST' and create_product_form.validate():
        try:
            # Handle image upload
            if 'image' in request.files:
                image = request.files['image']
                if image.filename == '':
                    flash('No image selected for uploading')
                    return redirect(request.url)

                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    # image.save(image_path)
                else:
                    flash('Allowed image types are - jpg, png, jpeg')
                    return redirect(request.url)

            # Check if a product with the same name already exists
            existing_product_query = "SELECT * FROM products WHERE name = %s"
            mycursor.execute(existing_product_query, (create_product_form.name.data,))
            existing_product = mycursor.fetchone()

            if existing_product:
                flash('Product with the same name already exists. Please choose a different name.')
                return render_template('create_product.html', form=create_product_form)


            # Create an instance of the Product class
            product = Product(
                name=create_product_form.name.data,
                price=create_product_form.price.data,
                category=create_product_form.category.data,
                image=filename,
                description=create_product_form.description.data,
                ingredients_info=create_product_form.ingredients_info.data,
                is_recommended=create_product_form.is_recommended.data
            )

            insert_query = "INSERT INTO products (name, price, category, image, description, ingredients_info, is_recommended) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            product_data = (product.get_name(), product.get_price(), product.get_category(), product.get_image(), product.get_description(), product.get_ingredients_info(), product.get_is_recommended())
            mycursor.execute(insert_query, product_data)

            mydb.commit()
            # Use url_for to generate the URL for the 'home' endpoint
            return redirect(url_for('retrieve_product'))

        except Exception as e:
            print('Error:', e)
            mydb.rollback()
            return "Error Occurred. Check logs for details"

    # Handle the case when the method is GET or the form validation fails
    return render_template('create_product.html', form=create_product_form)



@app.route('/retrieve_product', methods=['GET'])
def retrieve_product():
    select_query = "SELECT idproducts, name, price, category, image, description, ingredients_info, is_recommended FROM products"
    mycursor.execute(select_query)
    rows = mycursor.fetchall()

    # Create instances of the Product class
    products = [Product(idproducts=row[0], name=row[1], price=row[2], category=row[3], image=row[4], description=row[5], ingredients_info=row[6], is_recommended=row[7]) for row in rows]

    # Calculate the count of products
    count = len(products)

    return render_template('retrieve_product.html', products=products, count=count)



@app.route('/update_product/<int:id>/', methods=['GET', 'POST'])
def update_product(id):
    update_product_form = CreateProductForm(request.form)

    if request.method == 'POST' and update_product_form.validate():
        try:
            # Fetch existing product details from the database
            select_query = "SELECT idproducts, name, price, category, image, description, ingredients_info, is_recommended FROM products WHERE idproducts = %s"
            mycursor.execute(select_query, (id,))
            product_details = mycursor.fetchone()

            if product_details:
                # Update product details
                name = update_product_form.name.data
                price = update_product_form.price.data
                category = update_product_form.category.data
                image = update_product_form.image.data
                description = update_product_form.description.data
                ingredients_info = update_product_form.ingredients_info.data
                is_recommended = update_product_form.is_recommended.data

                # Handle image upload
                if 'image' in request.files:
                    image = request.files['image']
                    if image.filename != '':
                        filename = secure_filename(image.filename)
                        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        image.save(image_path)
                        # Save the new image filename to the database
                        update_query = "UPDATE products SET name = %s, price = %s, category = %s, image = %s, description = %s, ingredients_info = %s, is_recommended = %s WHERE idproducts = %s"
                        data = (name, price, category, filename, description, ingredients_info, is_recommended, id)
                        mycursor.execute(update_query, data)
                        mydb.commit()
                    else:
                        # If no new image provided, update without changing the image
                        update_query = "UPDATE products SET name = %s, price = %s, category = %s, description = %s, ingredients_info = %s, is_recommended = %s WHERE idproducts = %s"
                        data = (name, price, category, description, ingredients_info, is_recommended, id)
                        mycursor.execute(update_query, data)
                        mydb.commit()

                return redirect(url_for('retrieve_product'))

            else:
                return "Product not found"

        except Exception as e:
            print("Error: ", e)
            mydb.rollback()
            return "Error occurred while updating product"

    else:
        try:
            # Fetch existing product details to prepopulate the form
            select_query = "SELECT idproducts, name, price, category, image, description, ingredients_info, is_recommended FROM products WHERE idproducts = %s"
            mycursor.execute(select_query, (id,))
            product_details = mycursor.fetchone()

            if product_details:
                update_product_form.name.data = product_details[1]
                update_product_form.price.data = product_details[2]
                update_product_form.image.data = product_details[4]
                update_product_form.category.data = product_details[3]
                update_product_form.description.data = product_details[5]
                update_product_form.ingredients_info.data = product_details[6]
                update_product_form.is_recommended.data = product_details[7]

                return render_template('update_product.html', form=update_product_form)
            else:
                return "Product not found"

        except Exception as e:
            print('Error:', e)
            return "Error occurred while fetching product details"




@app.route('/delete_product/<int:id>', methods=['GET', 'POST'])
def delete_product(id):
    try:
        select_query = "SELECT * FROM products WHERE idproducts = %s"
        mycursor.execute(select_query, (id,))
        product = mycursor.fetchone()

        if product:
            delete_query = "DELETE FROM products WHERE idproducts = %s"
            mycursor.execute(delete_query, (id,))
            mydb.commit()

            return redirect(url_for('retrieve_product'))
        else:
            return "Product not found"

    except Exception as e:
        print('Error: ', e)
        mydb.rollback()
        return "Error occurred while deleting product"

tableCheck = ['cart']
for a in tableCheck:
    mycursor.execute(f"SHOW TABLES LIKE 'cart'")
    tableExist = mycursor.fetchone()

    if not tableExist:
        mycursor.execute('''CREATE TABLE `ecoeatsusers`
              `cart`(
                id int NOT NULL AUTO_INCREMENT,
                product_name VARCHAR(100) DEFAULT NULL,
                product_price DECIMAL(10, 2) DEFAULT NULL,
                product_image VARCHAR(200) DEFAULT NULL,
                quantity INT DEFAULT NULL
            )
        ''')
        print(f"Table 'cart' Created")

mycursor.execute('SELECT * FROM cart')
print(f"Using table 'cart' ")

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if request.method == 'POST':
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='JYOSHNA2006!',
            port='3306',
            database='ecoeatsusers'
        )

        mycursor = mydb.cursor()
        # Fetch product details from the database
        select_query = "SELECT idproducts, name, price, image FROM products WHERE idproducts = %s"
        mycursor.execute(select_query, (product_id,))
        product_details = mycursor.fetchone()

        if product_details:
            product_name = product_details[1]
            product_price = product_details[2]
            product_image = product_details[3]

            quantity = int(request.form.get(f'quantity_{product_id}', 1))

            # Check if the product is already in the cart
            select_cart_query = "SELECT * FROM cart WHERE product_name = %s"
            mycursor.execute(select_cart_query, (product_name,))
            cart_item = mycursor.fetchone()

            if cart_item:
                # Update quantity if the product is already in the cart
                new_quantity = cart_item[4] + quantity  # existing quantity in the cart + new quantity
                update_cart_query = "UPDATE cart SET quantity = %s WHERE product_name = %s"
                mycursor.execute(update_cart_query, (new_quantity, product_name))
            else:
                # Add the product to the cart
                insert_cart_query = "INSERT INTO cart (product_name, product_price, quantity, product_image) VALUES (%s, %s, %s, %s)"
                mycursor.execute(insert_cart_query, (product_name, product_price, quantity, product_image))

            mydb.commit()
        else:
            flash('Product not found')

        total_quantity_query = "SELECT SUM(quantity) FROM cart"
        mycursor.execute(total_quantity_query)
        total_quantity = mycursor.fetchone()[0] or 0  # handle None result

        # Get the referring page (referer) or use a default page if not available
        referring_page = request.referrer or url_for('home')

        session['cart_quantity'] = total_quantity

        # Redirect to the referring page
        return redirect(referring_page)







@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if request.method == 'POST':
        product_name = request.form.get('product_id')

        # Remove the product from the cart
        delete_cart_query = "DELETE FROM cart WHERE product_name = %s"
        mycursor.execute(delete_cart_query, (product_name,))
        mydb.commit()
        flash('Product removed from cart')
        total_quantity_query = "SELECT SUM(quantity) FROM cart"
        mycursor.execute(total_quantity_query)
        total_quantity = mycursor.fetchone()[0] or 0  # handle None result
        session['cart_quantity'] = total_quantity


    return redirect(url_for('view_cart'))

@app.route('/update_cart', methods=['POST'])
def update_cart():
    if request.method == 'POST':
        product_name = request.form.get('product_id')

        # Fetch product details from the database
        select_query = "SELECT name, price FROM products WHERE name = %s"
        mycursor.execute(select_query, (product_name,))
        product_details = mycursor.fetchone()

        if product_details:
            new_quantity = int(request.form.get('quantity', 1))

            # Update the quantity in the cart
            update_cart_query = "UPDATE cart SET quantity = %s WHERE product_name = %s"
            mycursor.execute(update_cart_query, (new_quantity, product_name))
            mydb.commit()
            flash('Cart updated')

        else:
            flash('Product not found')

    return redirect(url_for('view_cart'))


def get_cart_items():
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='JYOSHNA2006!',
        port='3306',
        database='ecoeatsusers'
    )

    mycursor = mydb.cursor()
    select_cart_query = "SELECT product_name, product_price, quantity, product_image FROM cart WHERE product_name IS NOT NULL AND product_price IS NOT NULL AND product_image IS NOT NULL"
    mycursor.execute(select_cart_query)
    cart_items_data = mycursor.fetchall()
    # Create CartItem instances from the fetched data
    cart_items = [CartItem(item[0], item[1], item[3], quantity=item[2]) for item in cart_items_data]

    return cart_items

def calculate_total_price(cart_items):
    return sum(item.get_price() * item.get_quantity() if item.get_price() is not None and item.get_quantity() is not None else 0 for item in cart_items)

@app.route('/cart', methods=['GET'])
def view_cart():
    cart_items = get_cart_items()
    total_price = calculate_total_price(cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

# tableCheck = ['order_info']
# for a in tableCheck:
#     mycursor.execute(f"SHOW TABLES LIKE 'order_info'")
#     tableExist = mycursor.fetchone()
#
#     if not tableExist:
#         mycursor.execute('''
#             CREATE TABLE `ecoeatsusers`
#               `order_info`(
#                 order_id int NOT NULL AUTO_INCREMENT,
#                 order_type VARCHAR(45) DEFAULT NULL,
#                 dine_in_time VARCHAR(45) DEFAULT NULL,
#                 pax INT DEFAULT NULL,
#                 street VARCHAR(200) DEFAULT NULL,
#                 block VARCHAR(45) DEFAULT NULL,
#                 unit_no VARCHAR(45) DEFAULT NULL,
#                 postal_code VARCHAR(45) DEFAULT NULL
#             )
#         ''')
#         print(f"Table 'order_info' Created")
#
# mycursor.execute('SELECT * FROM order_info')
# print(f"Using table 'order_info' ")
#
# @app.route('/dine_in', methods=['GET', 'POST'])
# def dine_in():
#     cart_items = get_cart_items()
#     total_price = calculate_total_price(cart_items)
#
#     dine_in = DineIn(order_id=None, time="", pax="")
#
#     dine_in_form = DineInForm(request.form)
#
#     if request.method == 'POST' and dine_in_form.validate():
#         time = dine_in_form.time.data
#         pax = dine_in_form.pax.data
#
#         # Check if pax is not empty and is a valid integer
#         if pax and pax.isdigit():
#             dine_in = DineIn(time, int(pax))
#         else:
#             dine_in = DineIn(time, 0)  # Set a default value or handle it according to your needs
#
#
#         # Explicitly fetch any previous result sets before executing the INSERT query
#         mycursor.fetchall()
#
#         # Store the information in the database
#         order_id = dine_in_form.order_id.data
#
#         if order_id:
#             update_order_info_query = "UPDATE order_info SET dine_in_time=%s, pax=%s WHERE order_id=%s"
#             mycursor.execute(update_order_info_query, (dine_in.get_time(), dine_in.get_pax(), order_id))
#         else:
#             insert_order_info_query = "INSERT INTO order_info (order_type, dine_in_time, pax) VALUES (%s, %s, %s)"
#             mycursor.execute(insert_order_info_query, ('dine_in', dine_in.get_time(), dine_in.get_pax()))
#
#         mydb.commit()
#
#     return render_template('dine_in.html', cart_items=cart_items, total_price=total_price, dine_in=dine_in, form=dine_in_form)
#
#
#
#
#
# @app.route("/delivery", methods=['GET', 'POST'])
# def delivery():
#     # Fetch cart items
#     cart_items = get_cart_items()
#     delivery_fee = 5
#     total_price = calculate_total_price(cart_items)
#     new_total = total_price + delivery_fee
#
#     delivery_form = DeliveryForm(request.form)
#
#     if request.method == 'POST' and delivery_form.validate():
#         street = delivery_form.street.data
#         block = delivery_form.block.data
#         unit_no = delivery_form.unit_no.data
#         postal_code = delivery_form.postal_code.data
#
#
#
#         # Create a Delivery instance
#         delivery = Delivery(street, block, unit_no, postal_code)
#
#
#         # Store the information in the database
#         insert_order_info_query = "INSERT INTO order_info (order_type, street, block, unit_no, postal_code) VALUES (%s, %s, %s, %s, %s)"
#         mycursor.execute(insert_order_info_query,
#                          ('delivery', delivery.get_street(), delivery.get_block(), delivery.get_unit_no(), delivery.get_postal_code()))
#         mydb.commit()
#
#         # Redirect to a confirmation page or another relevant page
#         return render_template('delivery.html', cart_items=cart_items, new_total=new_total, total_price=total_price, delivery_fee=delivery_fee, delivery=delivery, form=delivery_form)
#
#     return render_template("delivery.html", cart_items=cart_items, new_total=new_total, total_price=total_price, delivery_fee=delivery_fee, form=delivery_form)
#
#
#
# @app.route("/collection", methods=['GET', 'POST'])
# def collection():
#     # Fetch cart items
#     cart_items = get_cart_items()
#     total_price = calculate_total_price(cart_items)
#
#     if request.method == 'POST':
#
#         # Store the information in the database
#         insert_order_info_query = "INSERT INTO order_info (order_type) VALUES ( %s)"
#         mycursor.execute(insert_order_info_query, 'collection')
#         mydb.commit()
#
#         return render_template('collection.html', cart_items=cart_items, total_price=total_price)
#
#     return render_template('collection.html', cart_items=cart_items, total_price=total_price)
#
# @app.route("/delivery_finished")
# def delivery_finished():
#     return render_template('delivery_finished.html')
#
# @app.route("/dine_in_finished")
# def dine_in_finished():
#     return render_template('dine_in_finished.html')


@app.route("/profile")
def profile():
    return render_template('profile.html')


@app.route('/reviews')
def reviews():
    return render_template('reviews.html')

# @app.route('/createReviews', methods=['GET', 'POST'])
# def create_reviews():
#     create_reviews_form = CreateReviewsForm(request.form)
#
#     if request.method == 'POST' and create_reviews_form.validate():
#         try:
#             # Create the reviews table if it doesn't exist
#             mycursor.execute(
#                 "CREATE TABLE IF NOT EXISTS `ecoeatsusers`.`reviews` ("
#                 "`user_id` INT AUTO_INCREMENT PRIMARY KEY,"
#                 "`name` VARCHAR(100) DEFAULT NULL,"
#                 "`email` VARCHAR(100) DEFAULT NULL,"
#                 "`stars` INT DEFAULT NULL,"
#                 "`feedback` VARCHAR(1000) DEFAULT NULL"
#                 ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;"
#             )
#
#             # Insert data into the reviews table
#             insert_query = "INSERT INTO reviews (name, email, stars, feedback) VALUES (%s, %s, %s, %s)"
#             reviews = ReviewUser.UserReview(create_reviews_form.name.data, create_reviews_form.email.data,
#                                             create_reviews_form.stars.data,
#                                             create_reviews_form.feedback.data)
#             reviews_data = (reviews.get_name(), reviews.get_email(), reviews.get_stars(), reviews.get_feedback())
#             mycursor.execute(insert_query, reviews_data)
#             mydb.commit()
#
#             return redirect(url_for('retrieve_reviews'))
#         except Exception as e:
#             print("Error:", e)
#             mydb.rollback()
#             return "Error occurred. Check logs for details."
#
#     return render_template('createReviews.html', form=create_reviews_form)
#
# @app.route('/retrieveReviews')
# def retrieve_reviews():
#     select_query = "SELECT * FROM reviews"
#     mycursor.execute(select_query)
#     reviews = mycursor.fetchall()
#
#     return render_template('retrieveReviews.html', reviews=reviews)
#
#
# @app.route('/updateReviews/<int:user_id>/', methods=['GET', 'POST'])
# def update_reviews(user_id):
#     update_reviews_form = CreateReviewsForm(request.form)
#
#     if request.method == 'POST' and update_reviews_form.validate():
#         try:
#             # retrieve user data from db
#             select_query = "SELECT name, email, stars, feedback FROM reviews WHERE user_id = %s"
#
#             mycursor.execute(select_query, (user_id,))
#             reviews = mycursor.fetchone()
#
#             if reviews:
#                 name = update_reviews_form.name.data
#                 email = update_reviews_form.email.data
#                 stars = update_reviews_form.stars.data
#                 feedback = update_reviews_form.feedback.data
#
#                 update_query = "UPDATE reviews SET name = %s, email = %s, stars = %s, feedback = %s WHERE user_id = %s"
#                 data = (user_id, name, email, stars, feedback)
#                 mycursor.execute(update_query, data)
#
#                 mydb.commit()
#
#                 print(f"USER ID: {user_id} updated successfully.")
#                 return redirect(url_for('retrieve_reviews'))
#             else:
#                 return "Reviews not found."
#         except Exception as e:
#             print("Error:", e)
#             mydb.rollback()
#             return "Error occurred while updating reviews."
#     else:
#         try:
#
#             select_query = "SELECT name, email, stars, feedback FROM reviews WHERE user_id = %s"
#             mycursor.execute(select_query, (user_id,))
#             reviews = mycursor.fetchone()
#
#             if reviews:
#
#                 update_reviews_form.name.data = reviews[0]
#                 update_reviews_form.email.data = reviews[1]
#                 update_reviews_form.stars.data = reviews[2]
#                 update_reviews_form.feedback.data = reviews[3]
#
#                 return render_template('createReviews.html', form=update_reviews_form)
#
#             else:
#                 return "Reviews not found."
#         except Exception as e:
#
#             print("Error:", e)
#
#             mydb.rollback()
#
#             return "Error occurred while updating reviews."
#
#
# @app.route('/deleteReviews/<int:user_id>/', methods=['GET', 'POST'])
# def delete_reviews(user_id):
#     try:
#         select_query = "SELECT * FROM reviews WHERE user_id = %s"
#         mycursor.execute(select_query, (user_id,))
#         reviews = mycursor.fetchone()
#
#         if reviews:
#             delete_query = "DELETE FROM reviews WHERE user_id = %s"
#             mycursor.execute(delete_query, (user_id,))
#             mydb.commit()
#
#             print(f"USER ID: {user_id} deleted successfully.")
#             return redirect(url_for('retrieve_reviews'))
#         else:
#             return "Reviews not found."
#     except Exception as e:
#         print("Error:", e)
#         mydb.rollback()
#         return "Error occurred while deleting reviews."




#checking if user is logged in to access their membership

# checking if user is logged in to access their membership
# @app.route("/membership")
# def membership(request):
#     #check if logged in, redirect to membership
#     if request.user.is_authenticated:
#         return redirect(url_for('membershipHome'))
#     else:
#        return redirect(url_for('create_user'))
#     #if not, redirect to create users/log in page
#
# #brings to membership home page
# @app.route('/membershipHome')
# def membershipHome():
#     return render_template('membershipHome.html')




# routing for all membership pages
@app.route('/membership')
def membership():
    return render_template('membershipHome.html')


@app.route('/membershipShop')
def membershipShop():
    return render_template('membershipShop.html')


@app.route('/membershipTerms')
def membershipTerms():
    return render_template('membershipTerms.html')


@app.route('/membershipRewardHist')
def membershipRewardHist():
    return render_template('membershipRewardHist.html')


@app.route('/membershipTiers')
def membershipTiers():
    return render_template('membershipTiers.html')


# Tables to check and create
tableCheck = ['memberships']
for a in tableCheck:
    mycursor.execute(f"SHOW TABLES LIKE 'memberships'")
    tableExist = mycursor.fetchone()

    if not tableExist:
        mycursor.execute(
            "CREATE TABLE `memberships` ("
          "`membership_id` int NOT NULL,"
          "`currentBalance` float DEFAULT '0',"
          "`totalBalance` float DEFAULT '0',"
          "`date_joined` date DEFAULT NULL,"
          "`address` varchar(45) DEFAULT NULL,"
          "`email` varchar(45) DEFAULT NULL,"
          "PRIMARY KEY (`membership_id`),"
          "CONSTRAINT `id` FOREIGN KEY (`membership_id`) REFERENCES `users` (`id`)"
          ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;")

        print(f"Table 'memberships' Created")

mycursor.execute('SELECT * FROM memberships')
print(f"Using table 'memberships' ")




@app.route('/retrieveMembershipAdmin')
def retrieve_membership_admin():
    # retrieve from membership table
    select_query = "SELECT * FROM memberships"
    mycursor.execute(select_query)
    memberships = mycursor.fetchall()

    return render_template('retrieveMembershipAdmin.html', memberships=memberships)


@app.route('/retrieveMembership/<int:user_id>', methods=['GET'])
def retrieve_membership(user_id):
    mycursor.execute("SELECT * FROM memberships WHERE membership_id = %s", (user_id,))
    membershipUser = mycursor.fetchall()
    print("membershipUser: ", membershipUser)

    return render_template('retrieveMembership.html', membershipUser=membershipUser)

@app.route('/createMembership', methods=['GET', 'POST'])
def create_membership():
    create_membership_form = CreateMembershipForm(request.form)
    # Check if a user is logged in
    # if 'user_id' not in session:
    #     return redirect(url_for('create_user'))  # Redirect to the login page if the user is not logged in
    #
    # user_id = session['user_id']
    #
    # # Check if the user already has a membership
    # mycursor.execute("SELECT * FROM memberships WHERE membership_id = %s", (user_id,))
    # membership = mycursor.fetchone()
    # # If the user already has a membership, redirect to retrieve_membershipInfo
    # if membership:
    #     return redirect(url_for('retrieve_membershipInfo', user_id=user_id))

    if request.method == 'POST' and create_membership_form.validate():
        try:
            mydb = mysql.connector.connect(
                host='localhost',
                user='root',
                password='JYOSHNA2006!',
                port='3306',
                database='ecoeatsusers'
            )

            mycursor = mydb.cursor()
            # Update or insert rewards into memberships table
            insert_query = "INSERT INTO ecoeatsusers.memberships (membership_id, currentBalance, totalBalance) VALUES (%s, %s, %s)"
            # Prepare membership data
            memberships = Membership.Membership(create_membership_form.date_joined.data,
                                                create_membership_form.address.data,
                                                create_membership_form.email.data)
            print(insert_query)
            now = datetime.datetime(2009, 5, 5)
            user_id = 1
            data = (user_id, 300, 0)

            mycursor.execute(insert_query, data)
            mydb.commit()
            print(f"{memberships.get_date_joined()} {memberships.get_address()} {memberships.get_email()} "
                  f"was stored in the database successfully.")
            return redirect(url_for('retrieve_membershipInfo', user_id=user_id))
            # print(f"{memberships.get_date_joined()} {memberships.get_address()} {memberships.get_email()} "
            #       f"was stored in the database successfully.")
            # return redirect(url_for('retrieve_membershipInfo', user_id=user_id))
        except Exception as e:
            print("Error:", e)
            mydb.rollback()
            return "Error occurred. Check logs for details."

    return render_template('createMembership.html', form=create_membership_form)


#to display membership info and getting user first name for membership home
@app.route('/membershipInfo/<int:user_id>', methods=['GET'])
def retrieve_membershipInfo(user_id):
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='JYOSHNA2006!',
        port='3306',
        database='ecoeatsusers'
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM memberships WHERE membership_id = %s", (user_id,))
    membershipUser = mycursor.fetchone()
    print("membershipUser: ", membershipUser)

    mycursor.execute("SELECT username FROM users WHERE id = %s", (user_id,))
    membershipUsername = mycursor.fetchone()
    print("membershipUsername: ", membershipUsername)

    return render_template('membershipHome.html', membershipUser=membershipUser, membershipUsername=membershipUsername)


@app.route('/updateMembership/<int:membership_id>/', methods=['GET', 'POST'])
def update_membership(membership_id):
    update_membership_form = CreateMembershipForm(request.form)

    if request.method == 'POST' and update_membership_form.validate():
        try:
            # retrieve user data from db
            select_query = "SELECT date_joined, address, email FROM memberships WHERE membership_id = %s"
            mycursor.execute(select_query, (membership_id,))
            membership_details = mycursor.fetchone()

            if membership_details:
                date_joined = create_membership.date_joined.data
                address = update_membership_form.address.data
                email = update_membership_form.email.data

                update_query = "UPDATE memberships SET date_joined = %s, address = %s, email = %s WHERE membership_id = %s"
                data = (date_joined, address, email, membership_id)

                mycursor.execute(update_query, data)
                mydb.commit()

                print(f"Reward ID: {membership_id} updated successfully.")
                return redirect(url_for('retrieve_membership'))
            else:
                return "User Membership not found."
        except Exception as e:
            print("Error:", e)
            mydb.rollback()
            return "Error occurred while updating User Membership."

    else:
        try:
            # retrieve user data from mysql db
            select_query = "SELECT address, email FROM memberships WHERE membership_id = %s"
            mycursor.execute(select_query, (membership_id,))
            reward_details = mycursor.fetchone()

            if reward_details:

                update_membership_form.address.data = reward_details[0]
                update_membership_form.email.data = reward_details[1]

                return render_template('updateMembership.html', form=update_membership_form)
            else:
                return "User Membership not found."
        except Exception as e:
            print("Error:", e)
            mydb.rollback()
            return "Error occurred while updating User Membership."


@app.route('/deleteMembership/<int:membership_id>/', methods=['GET', 'POST'])
def delete_membership(membership_id):
    try:
        # Check if the user exists before attempting deletion
        select_query = "SELECT * FROM memberships WHERE membership_id = %s"
        mycursor.execute(select_query, (membership_id,))
        membership = mycursor.fetchone()

        if membership:
            delete_query = "DELETE FROM memberships WHERE membership_id = %s"
            mycursor.execute(delete_query, (membership_id,))
            mydb.commit()

            print(f"MEMBERSHIP ID: {membership_id} deleted successfully.")
            return redirect(url_for('create_membership'))
        else:
            return "User Membership not found."
    except Exception as e:
        print("Error:", e)
        mydb.rollback()
        return "Error occurred while deleting User Membership."


@app.route('/redeemRewards/<int:user_id>', methods=['GET', 'POST'])
def redeem_rewards(user_id):
    redeem_rewards_form = RedeemForm(request.form)
    if request.method == 'POST' and redeem_rewards_form.validate():
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='JYOSHNA2006!',
            port='3306',
            database='ecoeatsusers'
        )

        mycursor = mydb.cursor()
        try:
            select_query = ("SELECT currentBalance from memberships WHERE membership_id = %s")
            mycursor.execute(select_query, (user_id,))
            currentBalance = mycursor.fetchone()[0]
            if redeem_rewards_form.rewards.data == 1:
                if currentBalance>=50:
                    newCurrentBalance = currentBalance - 50

                    update_query = "UPDATE memberships SET currentBalance = %s WHERE membership_id = %s"
                    mycursor.execute(update_query, (newCurrentBalance, user_id))
                    mydb.commit()
                    print(f"Membership ID: {user_id} redeemed $5 off voucher successfully.")
                    return redirect(url_for('display_reward1'))
                else:
                    return "Balance not sufficient to redeem '$5 off voucher'."
            elif redeem_rewards_form.rewards.data == 2:
                if currentBalance >= 100:
                    newCurrentBalance = currentBalance - 100

                    update_query = "UPDATE memberships SET currentBalance = %s WHERE membership_id = %s"
                    mycursor.execute(update_query, (newCurrentBalance, user_id))
                    mydb.commit()
                    print(f"Membership ID: {user_id} redeemed $10 off voucher successfully.")
                    return redirect(url_for('display_reward2'))
                else:
                    return "Balance not sufficient to redeem '$10 off voucher'."
            else:
                if currentBalance >= 150:
                    newCurrentBalance = currentBalance - 150

                    update_query = "UPDATE memberships SET currentBalance = %s WHERE membership_id = %s"
                    mycursor.execute(update_query, (newCurrentBalance, user_id))
                    mydb.commit()
                    print(f"Membership ID: {user_id} redeemed $15 off voucher successfully.")
                    return redirect(url_for('display_reward2'))
                else:
                    return "Balance not sufficient to redeem '$15 off voucher'."

        except Exception as e:
            print("Error:", e)
            mydb.rollback()
            return "Error occurred while redeeming reward."
    return render_template('redeemRewards.html', form=redeem_rewards_form)



if __name__ == '__main__':
    app.run()

