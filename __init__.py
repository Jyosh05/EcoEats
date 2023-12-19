# first file to run when starting the web application
from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateUserForm
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


