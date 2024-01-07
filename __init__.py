# first file to run when starting the web application
from flask import Flask, render_template, request, redirect, url_for

import Membership
from Forms import CreateUserForm, CreateMembershipForm
import shelve, User

app = Flask(__name__)


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

@app.route("/reviews")
def reviews():
    return render_template('reviews.html')

@app.route("/profile")
def profile():
    return render_template('profile.html')

@app.route('/reviews')
def reviews():
    return render_template('reviews.html')




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

#checking if user is logged in to access their membership
# @app.route("/membership")
# def membership(id):
#     #check if logged in, redirect to membership
#     if request.user.is_authenticated:

#         return redirect(url_for('membershipHome'))
#     else:
#        return redirect(url_for('create_membership'))
#     #if not, redirect to create users/log in page
#


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


#creating membership
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

#points system

if __name__ == '__main__':
    app.run()


#COMBINE MEMBERSHIP FORM INTO SIGN UP
#option for membership: Y or N
#   if Y selected, open a new part of the form with all the extra membership qns
#when click on membership page, check if user had selected Y, if so, bring them to home
#if user selected N, bring them to membership signup page