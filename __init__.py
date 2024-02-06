# first file to run when starting the web application
import datetime

from flask import Flask, render_template, request, redirect, url_for, jsonify, session

from Forms import CreateUserForm, CreateMembershipForm, CreateReviewsForm, UpdateUserForm, RedeemForm
import User, Membership

# 1:56pm
# pip install mysql-connector-python
import mysql.connector
from flask import session
from functools import wraps
from flask import flash

import pandas as pd
import matplotlib.pyplot as plt

#
app = Flask(__name__)
app.secret_key = 'my_super_secret_key_123'

# # mySql Credentials
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='ecoeats',
    port='3306',
    database='ecoeatsusers'
)

mycursor = mydb.cursor()

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




@app.route('/createUser', methods=['GET', 'POST'])
def create_user():
    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        try:
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
        password='ecoeats',
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


@app.route('/recommended')
def recommended():
    return render_template("recommended.html")


@app.route('/appetizers')
def appetizers():
    return render_template('appetizers.html')


@app.route('/breakfast')
def breakfast():
    return render_template('breakfast.html')


@app.route('/lunch')
def lunch():
    return render_template('lunch.html')


@app.route('/dinner')
def dinner():
    return render_template('dinner.html')


@app.route('/dessert')
def dessert():
    return render_template('dessert.html')


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




@app.route("/cart")
def cart():
    return render_template('cart.html')

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
                password='ecoeats',
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
        password='ecoeats',
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
            password='ecoeats',
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

