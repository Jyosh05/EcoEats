# first file to run when starting the web application
from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateUserForm
import shelve, User

# pip install mysql-connector-python
import mysql.connector

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
# mycursor.execute('SELECT * FROM users')
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


@app.route('/createUser', methods = ['GET', 'POST'])
def create_user():
    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'c')
        try:
            users_dict = db['Users']
        except:
             print("Error in retrieving Users from user.db.")
        user = User.User(create_user_form.first_name.data, create_user_form.last_name.data,
                         create_user_form.gender.data, create_user_form.membership.data, create_user_form.remarks.data)
        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict
        # Test codes
        users_dict = db['Users']
        user = users_dict[user.get_user_id()]
        print(user.get_first_name(), user.get_last_name(), "was stored in user.db successfully with user_id ==",
              user.get_user_id())
        db.close()

        return redirect(url_for('home'))
    return render_template('createUser.html', form = create_user_form)



if __name__ == '__main__':
    app.run()


