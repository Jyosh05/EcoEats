# first file to run when starting the web application
from flask import Flask, render_template, request, redirect, url_for

from Forms import CreateUserForm, CreateMembershipForm, CreateReviewsForm, UpdateUserForm
import shelve, User, Membership

# 1:56pm
# pip install mysql-connector-python
# import mysql.connector

app = Flask(__name__)

# Dont run code below yet.

# # mySql Credentials
# mydb= mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='ecoeats',
#     port='3306',
#     database='ecoeatsusers'
# )
#
# mycursor = mydb.cursor()
#
# tableCheck = ['users']
# for a in tableCheck:
#     mycursor.execute(f"SHOW TABLES LIKE 'users'")
#     tableExist = mycursor.fetchone()
#
#     if not tableExist:
#         mycursor.execute("CREATE TABLE `ecoeatsusers`.`users` (`id` INT NOT NULL, `username` VARCHAR(45) NULL, `password` VARCHAR(45) NULL, PRIMARY KEY (`id`)); ")
#         print(f"Table 'users' Created")
#
# mycursor.execute('SELECT * FROM users')
# print(f"Using table 'users' ")
#
# users = mycursor.fetchall()
# # index 0 is used for count / unique id
# for a in users:
#     print(a)
#     print('Username: ', a[1])
#     print('Password: ', a[2])
#
# # ecoeatsusers file is MySql DB file, if u want to put onto ur local disk >
# # WIN + R, type in '%programdata%', find MySQL > MySQL Server 8.0 > Data
# # Then throw the ecoeatsusers into that folder.
#
#
# @app.route('/createUser', methods=['GET', 'POST'])
# def create_user():
#     create_user_form = CreateUserForm(request.form)
#     if request.method == 'POST' and create_user_form.validate():
#         try:
#             mycursor.execute("SELECT COUNT(*) FROM users")
#             id = mycursor.fetchone()[0]
#             print(id)
#             insert_query = "INSERT INTO users (id, username, password) " \
#                            "VALUES (%s, %s, %s)"
#             user = User.User(create_user_form.username.data, create_user_form.password.data)
#             user_data = (id + 1,user.get_username(),user.get_password())
#             mycursor.execute(insert_query, user_data)
#             mydb.commit()
#
#             print(f"{user.get_userCount()}{user.get_username()} {user.get_password()} was stored in the database successfully.")
#             return redirect(url_for('home'))
#         except Exception as e:
#             print("Error:", e)
#             mydb.rollback()
#             return "Error occurred. Check logs for details."
#     return render_template('createUser.html', form=create_user_form)
#
# @app.route('/retrieveUser')
# def retrieve_user():
#     select_query = "SELECT * FROM users"
#     mycursor.execute(select_query)
#     users = mycursor.fetchall()
#     return render_template('retrieveUser.html', users=users)
#
# @app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
# def update_user(id):
#     update_user_form = CreateUserForm(request.form)
#
#     if request.method == 'POST' and update_user_form.validate():
#         try:
#             # Retrieve user data from MySQL database
#             select_query = "SELECT username, password FROM users WHERE id = %s"
#             mycursor.execute(select_query, (id,))
#             user_details = mycursor.fetchone()
#
#             if user_details:
#                 username = update_user_form.username.data
#                 password = update_user_form.password.data
#
#
#                 # Update query for first_name, last_name, gender, membership, remarks
#                 update_query = "UPDATE users SET username = %s, password = %s WHERE id = %s"
#                 data = (username, password, id)
#                 mycursor.execute(update_query, data)
#                 mydb.commit()
#
#                 print(f"User ID: {id} updated successfully.")
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
#             # Retrieve user data from MySQL database
#             select_query = "SELECT username, password FROM users WHERE id = %s"
#             mycursor.execute(select_query, (id,))
#             user_details = mycursor.fetchone()
#
#             if user_details:
#                 update_user_form.username.data = user_details[0]
#                 update_user_form.password.data = user_details[1]
#
#
#                 return render_template('updateUser.html', form=update_user_form)
#             else:
#                 return "User not found."
#         except Exception as e:
#             print("Error:", e)
#             return "Error occurred while fetching user details."












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


@app.route('/')
def home():
    return render_template("home.html")


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

@app.route("/cart")
def cart():
    return render_template('cart.html')

#checking if user is logged in to access their membership
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


@app.route('/createReviews', methods=['GET', 'POST'])
def create_reviews():
    create_reviews_form = CreateReviewsForm(request.form)
    if request.method == 'POST' and create_reviews_form.validate():
        db = shelve.open('reviews.db', 'c')
        try:
            reviews_dict = db['Review']
        except:
            print("Error in retrieving Users from user.db.")

@app.route('/createMembership', methods=['GET', 'POST'])
def create_membership():
    create_membership_form = CreateMembershipForm(request.form)
    if request.method == 'POST' and create_membership_form.validate():
        db = shelve.open('membership.db', 'c')
        try:
            memberships_dict = db['Membership']
        except:
            print("Error in retrieving Users from user.db.")

        # + Membership.Membership(get_currentBalance), Membership.get_totalPoints(), Membership.get_Buyrewards(),) #find a way to retrieve the store_reward variable, and the other non-form data

        membershipFormData = Membership.Membership(create_membership_form.email.data, create_membership_form.date_joined.data, create_membership_form.address.data)


        memberships_dict[membershipFormData.get_membership_id()] = membershipFormData
        db['Membership'] = memberships_dict

        db.close()

        return redirect(url_for('membership'))
    return render_template('createMembership.html', form=create_membership_form)

#retrieving membership
@app.route('/retrieveMembership')
def retrieve_membership():
    memberships_dict = {}
    db = shelve.open('membership.db', 'r')
    memberships_dict = db['Membership']
    db.close()

    membership_list = []
    for key in memberships_dict:
        membership = memberships_dict.get(key)
        membership_list.append(membership)

    return render_template('membership.html', count=len(membership_list), customers_list=membership_list)

#updating membership
@app.route('/updateMembership/<int:id>/', methods=['GET', 'POST'])
def update_membership(id):
    update_membership_form = CreateMembershipForm(request.form)
    if request.method == 'POST' and update_membership_form.validate():
        memberships_dict = {}
        db = shelve.open('membership.db', 'w')
        membership_dict = db['Membership']

        membershipUser = membership_dict.get(id)
        membershipUser.set_first_name(update_membership_form.first_name.data)
        membershipUser.set_last_name(update_membership_form.last_name.data)
        membershipUser.set_gender(update_membership_form.gender.data)
        membershipUser.set_email(update_membership_form.email.data)
        membershipUser.set_date_joined(update_membership_form.date_joined.data)
        membershipUser.set_address(update_membership_form.address.data)

        db['Membership'] = membership_dict
        db.close()

        return redirect(url_for('retrieve_membership'))
    else:
        memberships_dict = {}
        db = shelve.open('membership.db', 'r')
        memberships_dict = db['Membership']
        db.close()

        MembershipUser = memberships_dict.get(id)
        update_membership_form.first_name.data = MembershipUser.get_first_name()
        update_membership_form.last_name.data = MembershipUser.get_last_name()
        update_membership_form.gender.data = MembershipUser.get_gender()
        update_membership_form.email.data = MembershipUser.get_email()
        update_membership_form.date_joined.data = MembershipUser.get_date_joined()
        update_membership_form.address.data = MembershipUser.get_address()


        return render_template('updateMembership.html', form=update_membership_form)

@app.route('/deleteMembership/<int:id>', methods=['POST'])
def delete_membership(id):
    memberships_dict = {}
    db = shelve.open('membership.db', 'w')
    memberships_dict = db['Membership']
    memberships_dict.pop(id)

    db['Membership'] = memberships_dict
    db.close()

    return redirect(url_for('retrieve_membership'))


    reviewsFormData = reviews.reviews(create_reviews_form.email.data, create_reviews_form.date_joined.data, create_reviews_form.address.data)


    reviews_dict[reviewsFormData.get_reviews_id()] = reviewsFormData
    db['Review'] = reviews_dict

    db.close()

    return redirect(url_for('reviews'))
    return render_template('createReviews.html', form=create_reviews_form)

@app.route('/retrieveReviews')
def retrieve_reviews():
    reviews_dict = {}
    db = shelve.open('reviews.db', 'r')
    reviews_dict = db['Review']
    db.close()

    reviews_list = []
    for key in reviews_dict:
        reviews_dict = reviews_dict.get(key)
        reviews_list.append(membership)

    return render_template('reviews.html', count=len(reviews_list), customers_list=reviews_list)



    return redirect(url_for('retrieve_reviews'))




if __name__ == '__main__':
    app.run()


