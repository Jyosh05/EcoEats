# first file to run when starting the web application
from flask import Flask, render_template, request, redirect, url_for, jsonify

from Forms import CreateUserForm, CreateMembershipForm, CreateReviewsForm, UpdateUserForm, CreateRewardsForm, UpdateMembershipForm
import shelve, User, Membership, Rewards

# 1:56pm
# pip install mysql-connector-python
import mysql.connector
#
app = Flask(__name__)
#
# # Dont run code below yet.
#
#
# # mySql Credentials
mydb= mysql.connector.connect(
    host='localhost',
    user='root',
    password='ecoeats',
    port='3306',
    database='ecoeatsusers'
)

mycursor = mydb.cursor()
#
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

# ecoeatsusers file is MySql DB file, if u want to put onto ur local disk >
# WIN + R, type in '%programdata%', find MySQL > MySQL Server 8.0 > Data
# Then throw the ecoeatsusers into that folder.


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
            # print(id)
            insert_query = "INSERT INTO users ( username, password) " \
                           "VALUES (%s, %s)"
            user = User.User(create_user_form.username.data, create_user_form.password.data)
            user_data = (user.get_username(),user.get_password())
            mycursor.execute(insert_query, user_data)
            mydb.commit()

            lastest_id = mycursor.lastrowid

            print(f"{user.get_userCount()} {lastest_id} {user.get_username()} {user.get_password()} was stored in the database successfully.")
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
    return render_template('retrieveUser.html', users=users)

@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_user_form = CreateUserForm(request.form)

    if request.method == 'POST' and update_user_form.validate():
        try:
            #reetrieve user data from db
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
            #retrieve user data from mysql db
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
                #delete all the selected users from db
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

        #query to fetch user by username and password
        select_query = "SELECT * FROM users WHERE username = %s AND password = %s"
        mycursor.execute(select_query, (username, password))
        user = mycursor.fetchone()
        id = user[0] #retrieve id of user


        if user:
            #logged in, redirect  back to website
            print(f"User ID: {id} , Username: {username} Password:wont display but possible logged in successfully.  ")
            return redirect(url_for('profile'))

        else:
            #invalid login error msg
            return "Invalid credentials. Please try again or sign up."

    return render_template('login.html', form=loginForm)

    #     #query to fetch user by username and password
    #     select_query = "SELECT * FROM users WHERE username = %s AND password = %s"
    #     mycursor.execute(select_query, (username, password))
    #     user = mycursor.fetchone()
    #     id = user[0] #retrieve id of user
    #
    #
    #     if user:
    #         #logged in, redirect  back to website
    #         print(f"User ID: {id} , Username: {username} Password:wont display but possible logged in successfully.  ")
    #         return redirect(url_for('profile'))
    #
    #     else:
    #         #invalid login error msg
    #         return "Invalid credentials. Please try again or sign up."
    #
    # return render_template('login.html', form=loginForm)
#
#
# # previous /createUser, only left here for reference. do not use.
# # @app.route('/createUser', methods = ['GET', 'POST'])
# # def create_user():
# #     create_user_form = CreateUserForm(request.form)
# #     if request.method == 'POST' and create_user_form.validate():
# #         users_dict = {}
# #         db = shelve.open('user.db', 'c')
# #         try:
# #             users_dict = db['Users']
# #         except:
# #              print("Error in retrieving Users from user.db.")
# #         user = User.User(create_user_form.first_name.data, create_user_form.last_name.data,
# #                          create_user_form.gender.data, create_user_form.membership.data, create_user_form.remarks.data)
# #         users_dict[user.get_user_id()] = user
# #         db['Users'] = users_dict
# #         # Test codes
# #         users_dict = db['Users']
# #         user = users_dict[user.get_user_id()]
# #         print(user.get_first_name(), user.get_last_name(), "was stored in user.db successfully with user_id ==",
# #               user.get_user_id())
# #         db.close()
# #
# #         return redirect(url_for('home'))
# #     return render_template('createUser.html', form = create_user_form)
#
#
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


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



#routing for all membership pages

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
tables_to_check = ['storerewards', 'memberships']

for table_name in tables_to_check:
    mycursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    table_exist = mycursor.fetchone()



    if not table_exist:
        if table_name == 'storerewards':
            mycursor.execute("CREATE TABLE `ecoeatsusers`.`storerewards` ("
                             "`reward_id` int NOT NULL AUTO_INCREMENT,"
                             "`reward_name` VARCHAR(100) NULL,"
                             "`reward_value` DECIMAL NULL DEFAULT 0.00,"
                             "`reward_type` enum('promotional', 'fixed', 'storewide'),"
                             "PRIMARY KEY (`reward_id`)"
                             ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;")
        elif table_name == 'memberships':
            mycursor.execute("CREATE TABLE `ecoeatsusers`.`memberships` ("
                             "`membership_id` INT NOT NULL,"
                             "`rewards` VARCHAR(100) NULL,"
                             "`currentBalance` FLOAT DEFAULT 0.00,"
                             "`totalBalance` FLOAT DEFAULT 0.00,"
                             "`date_joined` DATE DEFAULT NULL,"
                             "`address` varchar(45) DEFAULT NULL,"
                             "`email` varchar(45) DEFAULT NULL,"
                             "PRIMARY KEY (`membership_id`),"
                             "CONSTRAINT id FOREIGN KEY (`membership_id`) REFERENCES `users` (`id`)"
                             ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;")



        print(f"Table '{table_name}' Created")

for _ in mycursor:
    pass

@app.route('/retrieveMembership')
def retrieve_membership():
    #retrieve from membership table
    select_query = "SELECT * FROM memberships"
    mycursor.execute(select_query)
    memberships = mycursor.fetchall()

    return render_template('membershipHome.html', memberships=memberships)

@app.route('/createMembership', methods=['GET', 'POST'])
def create_membership():
    create_membership_form = CreateMembershipForm(request.form)
    if request.method == 'POST' and create_membership_form.validate():
        try:
            insert_query = "INSERT INTO memberships (membership_id, rewards, currentBalance, totalBalance, date_joined, address, email)" \
                           "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            memberships = Membership.Membership(create_membership_form.date_joined.data, create_membership_form.address.data, create_membership_form.email.data)
            reward_data = (1, 'NULL', 0.00, 0.00, memberships.get_date_joined(), memberships.get_address(), memberships.get_email())

            mycursor.execute(insert_query, reward_data)
            mydb.commit()
            print(
                f"{memberships.get_date_joined()} {memberships.get_address()} {memberships.get_email()} "
                f"was stored in the database successfully.")
            return redirect(url_for('retrieve_membership'))
        except Exception as e:
            print("Error:", e)
            mydb.rollback()
            return "Error occurred. Check logs for details."
    return render_template('createMembership.html', form=create_membership_form)

@app.route('/updateMembership/<int:membership_id>/', methods=['GET', 'POST'])
def update_membership(membership_id):
    update_membership_form = CreateMembershipForm(request.form)

    if request.method == 'POST' and update_membership_form.validate():
        try:
            #retrieve user data from db
            select_query = "SELECT date_joined, address, email FROM memberships WHERE membership_id = %s"
            mycursor.execute(select_query, (membership_id,))
            membership_details = mycursor.fetchone()

            if membership_details:
                date_joined = update_membership_form.date_joined.data
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
            #retrieve user data from mysql db
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

#rewards are all in staff section
#creating rewards
@app.route('/createRewards', methods=['GET', 'POST'])
def create_rewards():
    create_reward_form = CreateRewardsForm(request.form)
    if request.method == 'POST' and create_reward_form.validate():
        try:
            # insert_query = "INSERT INTO storerewards (reward_name, reward_value, reward_type ) " \
            #                "VALUES (%s, %.2f, %s)"
            insert_query = "INSERT INTO storerewards (reward_name, reward_value, reward_type) " \
                           "VALUES (%s, %s, %s)"
            reward = Rewards.Rewards(create_reward_form.reward_name.data, create_reward_form.reward_value.data,
                                     create_reward_form.reward_type.data)
            reward_data = (reward.get_reward_name(), reward.get_reward_value(), reward.get_reward_type())
            mycursor.execute(insert_query, reward_data)
            mydb.commit()
            print(
                f"{reward.get_reward_name()} {reward.get_reward_value()} {reward.get_reward_type()} "
                f"was stored in the database successfully.")
            return redirect(url_for('retrieve_rewards'))
        except Exception as e:
            print("Error:", e)
            mydb.rollback()
            return "Error occurred. Check logs for details."
    return render_template('createRewards.html', form=create_reward_form)

@app.route('/retrieveRewards')
def retrieve_rewards():
    # retrieve from membership table
    select_query = "SELECT * FROM storerewards"
    mycursor.execute(select_query)
    rewards = mycursor.fetchall()

    return render_template('retrieveRewards.html', rewards=rewards)

@app.route('/updateReward/<int:reward_id>/', methods=['GET', 'POST'])
def update_reward(reward_id):
    update_reward_form = CreateRewardsForm(request.form)

    if request.method == 'POST' and update_reward_form.validate():
        try:
            #retrieve user data from db
            select_query = "SELECT reward_name, reward_value, reward_type FROM storerewards WHERE reward_id = %s"

            mycursor.execute(select_query, (reward_id,))
            reward_details = mycursor.fetchone()

            if reward_details:
                reward_name = update_reward_form.reward_name.data
                reward_value = update_reward_form.reward_value.data
                reward_type = update_reward_form.reward_type.data


                # update_query = "UPDATE storerewards SET reward_name = %s, reward_value = %.2f, reward_type = %s WHERE reward_id = %s"
                # data = (reward_name, reward_value, reward_type, reward_id)
                # mycursor.execute(update_query, data)
                update_query = "UPDATE storerewards SET reward_name = %s, reward_value = %s, reward_type = %s WHERE reward_id = %s"
                data = (reward_name, reward_value, reward_type, reward_id)
                mycursor.execute(update_query, data)

                mydb.commit()

                print(f"Reward ID: {reward_id} updated successfully.")
                return redirect(url_for('retrieve_rewards'))
            else:
                return "Reward not found."
        except Exception as e:
            print("Error:", e)
            mydb.rollback()
            return "Error occurred while updating reward."
    else:
        try:

            # Retrieve user data from the 'storerewards' table
            select_query = "SELECT reward_name, reward_value, reward_type FROM storerewards WHERE reward_id = %s"
            mycursor.execute(select_query, (reward_id,))
            reward_details = mycursor.fetchone()

            if reward_details:

                update_reward_form.reward_name.data = reward_details[0]
                update_reward_form.reward_value.data = reward_details[1]
                update_reward_form.reward_type.data = reward_details[2]

                return render_template('createRewards.html', form=update_reward_form)

            else:
                return "Reward not found."
        except Exception as e:

            print("Error:", e)

            mydb.rollback()

            return "Error occurred while updating reward."


@app.route('/deleteReward/<int:reward_id>/', methods=['GET', 'POST'])
def delete_reward(reward_id):
    try:
        # Check if the user exists before attempting deletion
        select_query = "SELECT * FROM storerewards WHERE reward_id = %s"
        mycursor.execute(select_query, (reward_id,))
        reward = mycursor.fetchone()

        if reward:
            delete_query = "DELETE FROM storerewards WHERE reward_id = %s"
            mycursor.execute(delete_query, (reward_id,))
            mydb.commit()

            print(f"REWARD ID: {reward_id} deleted successfully.")
            return redirect(url_for('retrieve_rewards'))
        else:
            return "Reward not found."
    except Exception as e:
        print("Error:", e)
        mydb.rollback()
        return "Error occurred while deleting reward."

#adding rewards to membership:
@app.route('/membershipRewards/<int:membership_id>', methods=['GET', 'POST'])
def membership_rewards(membership_id):
    try:
        # Execute the SQL query to update the rewards in memberships
        update_query = "UPDATE 'memberships' SET 'rewards' = (SELECT GROUP_CONCAT('reward_name' SEPARATOR ', ')" \
                       "FROM 'storerewards') WHERE membership_id = %s;"
        mycursor.execute(update_query, (membership_id,))
        # Commit the changes to the database
        mydb.commit()

        print(f"Rewards updated successfully for membership ID: {membership_id}")
        return redirect(url_for('retrieve_memberships'))  # Replace with your actual route for retrieving memberships
    except Exception as e:
        print("Error:", e)
        mydb.rollback()
        return "Error occurred while updating rewards."

#redeeming rewards
@app.route('/redeemRewards', methods=['GET', 'POST'])
def redeem_rewards():
    try:
        id = int(request.args.get("'ecoeatsusers'.'memberships'.'id'"))
        reward_name = request.args.get("'ecoeatsusers'.'storeRewards'.'reward_name'")

    #query to get user data from users table
        mycursor.execute(f"SELECT * FROM `ecoeatsusers`.`memberships` WHERE id = '{id}'")
        user_data = mycursor.fetchone()

        if user_data is None:
            return jsonify({'error': 'User not found'}), 404

        mycursor.execute(f"SELECT * FROM storeRewards WHERE reward_name = '{reward_name}'")
        reward_data = mycursor.fetchone()

        if reward_data is None:
            return jsonify({'error': 'Reward not found'}), 404

    #check if user points sufficient
        if user_data[3] < reward_data[2]:
            return jsonify({'error': 'Points not sufficient'}), 404

    #deducting points
        mycursor.execute(f"UPDATE memberships SET currentBalance = currentBalance - {reward_data[2]},"
                         f"rewards = CONCAT(rewards, ',{reward_name}') WHERE id = {id}")
        'ecoeatsusers'.commit()

        return jsonify({'message': 'f"Reward successfully redeemed!"'}), 200
    except Exception as e:
        print("Error:", e)
        mydb.rollback()
        return "Error occurred while redeeming reward."


app.route('/createReviews', methods=['GET', 'POST'])
def create_reviews():
    create_reviews_form = CreateReviewsForm(request.form)
    if request.method == 'POST' and create_reviews_form.validate():
        db = shelve.open('reviews.db', 'c')
        try:
            reviews_dict = db['Review']
        except:
            print("Error in retrieving Users from user.db.")
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


