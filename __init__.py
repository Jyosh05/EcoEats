# # first file to run when starting the web application
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from werkzeug.utils import secure_filename
import os
# # from Forms import CreateUserForm
from Forms import CreateProductForm, DineInForm, DeliveryForm
from Product import Product
from cart import CartItem
from order_type import DineIn, Delivery
# import shelve, User
# import shelve, Product
import secrets

# pip install mysql-connector-python
import mysql.connector

app = Flask(__name__)
app.secret_key = 'ecoeats'
UPLOAD_FOLDER = 'static/img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif'])

# Dont run code below yet.

# mySql Credentials
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='JYOSHNA2006!',
    port=3306,
    database='products'
)

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='JYOSHNA2006!',
    port=3306,
    database='products'
)

my_db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='JYOSHNA2006!',
    port=3306,
    database='products'
)
#
# mycursor.execute('CREATE TABLE IF NOT EXISTS Images (id INTEGER(45) NOT NULL AUTO_INCREMENT PRIMARY KEY, '
#                  'Photo LONGBLOB NOT NULL)')
#
# def InsertBlob(FilePath):
#     with open(FilePath, 'rb') as File:
#         BinaryData = File.read()
#     SQLStatement = 'INSERT INTO Images (Photo) VALUES (%s)'
#     mycursor.execute(SQLStatement, (BinaryData, ))
#     mydb.commit()
#
# def RetrieveBlob(ID):
#     SQLStatement2 = "SELECT  * FROM Images WHERE id = '{0}'"
#     mycursor.execute(SQLStatement2.format(str(ID)))
#     MyResult = mycursor.fetchone()[1]
#     StoreFilePath = "Static/ImageOutputs/img{0}.png".format(str(ID))
#     print(MyResult)
#     with open(StoreFilePath, 'wb') as File:
#         File.write(MyResult)
#         File.close()
#
#
# print("1. Insert Image\n2. Read Image")
# MenuInput = input()
# if int(MenuInput) == 1:
#     UserFilePath = input('Enter File Path: ')
#     InsertBlob(UserFilePath)
# elif int(MenuInput) == 2:
#     UserIDChoice = input("Enter ID: ")
#     RetrieveBlob(UserIDChoice)



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

cursor = db.cursor()
cur = mydb.cursor()
mycursor = my_db.cursor()


tableCheck = ['products']
for a in tableCheck:
    cursor.execute(f"SHOW TABLES LIKE 'products'")
    tableExist = cursor.fetchone()

    if not tableExist:
        cursor.execute("CREATE TABLE `products`"
                       "`products` "
                       "(`idproducts` INT NOT NULL, `name` VARCHAR(100) NULL, "
                       "`price` DECIMAL(10,2) NULL, "
                       "`category` VARCHAR(45) NULL, "
                       "`image` VARCHAR(200) NULL,"
                       "`description` VARCHAR(400) NULL,"
                       "`ingredients_info` VARCHAR(1000) NULL"
                       "PRIMARY KEY (`idproducts`)); ")
        print(f"Table 'products' Created")

cursor.execute('SELECT * FROM products')
print(f"Using table 'products' ")

tableCheck = ['cart']
for a in tableCheck:
    cur.execute(f"SHOW TABLES LIKE 'cart'")
    tableExist = cur.fetchone()

    if not tableExist:
        cur.execute('''
            CREATE TABLE `product`
              `cart`(
                id int NOT NULL AUTO_INCREMENT,
                product_name VARCHAR(100) DEFAULT NULL,
                product_price DECIMAL(10, 2) DEFAULT NULL,
                product_image VARCHAR(200) DEFAULT NULL,
                quantity INT DEFAULT NULL
            )
        ''')
        print(f"Table 'cart' Created")

cur.execute('SELECT * FROM cart')
print(f"Using table 'cart' ")

tableCheck = ['order_info']
for a in tableCheck:
    mycursor.execute(f"SHOW TABLES LIKE 'order_info'")
    tableExist = mycursor.fetchone()

    if not tableExist:
        mycursor.execute('''
            CREATE TABLE `product`
              `order_info`(
                order_id int NOT NULL AUTO_INCREMENT,
                order_type VARCHAR(45) DEFAULT NULL,
                dine_in_time VARCHAR(45) DEFAULT NULL,
                pax INT DEFAULT NULL,
                street VARCHAR(200) DEFAULT NULL,
                block VARCHAR(45) DEFAULT NULL,
                unit_no VARCHAR(45) DEFAULT NULL,
                postal_code VARCHAR(45) DEFAULT NULL
            )
        ''')
        print(f"Table 'order_info' Created")

mycursor.execute('SELECT * FROM order_info')
print(f"Using table 'order_info' ")


products = cursor.fetchall()
cart = cur.fetchall()
order_info = mycursor.fetchall()
# index 0 is used for count / unique id
# for a in products:
#     print(a)
#     print('Name: ', a[1])
#     print('Price: ', a[2])
#     print('Category: ', a[3])

# Now you can use 'sql_statement' wherever you need it in your Python code




@app.route('/productBase/<category>')
def category(category):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM products WHERE category = %s', (category,))
    data = cursor.fetchall()
    cursor.close()

    return render_template('productBase.html', category=category, products=data)

@app.route('/recommended')
def recommended():
    # Define the number of products to fetch from each category
    products_per_category = 2

    # Fetch distinct category names from the products table
    cursor_categories = db.cursor()
    cursor_categories.execute('SELECT DISTINCT category FROM products')
    category_names = [category[0] for category in cursor_categories.fetchall()]
    cursor_categories.close()

    # Fetch recommended products for each category
    recommended_products = []

    for category_name in category_names:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM products WHERE category = %s LIMIT %s', (category_name, products_per_category))
        recommended_products.extend(cursor.fetchall())
        cursor.close()

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
            cursor.execute(existing_product_query, (create_product_form.name.data,))
            existing_product = cursor.fetchone()

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
                ingredients_info=create_product_form.ingredients_info.data
            )

            insert_query = "INSERT INTO products (name, price, category, image, description, ingredients_info) VALUES (%s, %s, %s, %s, %s, %s)"
            product_data = (product.get_name(), product.get_price(), product.get_category(), product.get_image(), product.get_description(), product.get_ingredients_info())
            cursor.execute(insert_query, product_data)

            db.commit()
            # Use url_for to generate the URL for the 'home' endpoint
            return redirect(url_for('home'))

        except Exception as e:
            print('Error:', e)
            db.rollback()
            return "Error Occurred. Check logs for details"

    # Handle the case when the method is GET or the form validation fails
    return render_template('create_product.html', form=create_product_form)



@app.route('/retrieve_product', methods=['GET'])
def retrieve_product():
    select_query = "SELECT idproducts, name, price, category, image, description, ingredients_info FROM products"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    # Create instances of the Product class
    products = [Product(idproducts=row[0], name=row[1], price=row[2], category=row[3], image=row[4], description=row[5], ingredients_info=row[6]) for row in rows]

    # Calculate the count of products
    count = len(products)

    return render_template('retrieve_product.html', products=products, count=count)



@app.route('/update_product/<int:id>/', methods=['GET', 'POST'])
def update_product(id):
    update_product_form = CreateProductForm(request.form)

    if request.method == 'POST' and update_product_form.validate():
        try:
            # Fetch existing product details from the database
            select_query = "SELECT idproducts, name, price, category, image, description, ingredients_info FROM products WHERE idproducts = %s"
            cursor.execute(select_query, (id,))
            product_details = cursor.fetchone()

            if product_details:
                # Update product details
                name = update_product_form.name.data
                price = update_product_form.price.data
                category = update_product_form.category.data
                image = update_product_form.image.data
                description = update_product_form.description.data
                ingredients_info = update_product_form.ingredients_info.data

                # Handle image upload
                if 'image' in request.files:
                    image = request.files['image']
                    if image.filename != '':
                        filename = secure_filename(image.filename)
                        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        image.save(image_path)
                        # Save the new image filename to the database
                        update_query = "UPDATE products SET name = %s, price = %s, category = %s, image = %s, description = %s, ingredients_info = %s WHERE idproducts = %s"
                        data = (name, price, category, filename, description, ingredients_info, id)
                        cursor.execute(update_query, data)
                        db.commit()

                return redirect(url_for('retrieve_product'))

            else:
                return "Product not found"

        except Exception as e:
            print("Error: ", e)
            db.rollback()
            return "Error occurred while updating product"

    else:
        try:
            # Fetch existing product details to prepopulate the form
            select_query = "SELECT idproducts, name, price, category, image, description, ingredients_info FROM products WHERE idproducts = %s"
            cursor.execute(select_query, (id,))
            product_details = cursor.fetchone()

            if product_details:
                update_product_form.name.data = product_details[1]
                update_product_form.price.data = product_details[2]
                update_product_form.image.data = product_details[4]
                update_product_form.category.data = product_details[3]
                update_product_form.description.data = product_details[5]
                update_product_form.ingredients_info.data = product_details[6]


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
        cursor.execute(select_query, (id,))
        product = cursor.fetchone()

        if product:
            delete_query = "DELETE FROM products WHERE idproducts = %s"
            cursor.execute(delete_query, (id,))
            db.commit()

            return redirect(url_for('retrieve_product'))
        else:
            return "Product not found"

    except Exception as e:
        print('Error: ', e)
        db.rollback()
        return "Error occurred while deleting product"



@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if request.method == 'POST':
        # Fetch product details from the database
        select_query = "SELECT idproducts, name, price, image FROM products WHERE idproducts = %s"
        cur.execute(select_query, (product_id,))
        product_details = cur.fetchone()

        if product_details:
            product_name = product_details[1]
            product_price = product_details[2]
            product_image = product_details[3]

            # Adjust the form field name to include the product ID
            quantity = int(request.form.get(f'quantity_{product_id}', 1))

            # Check if the product is already in the cart
            select_cart_query = "SELECT * FROM cart WHERE product_name = %s"
            cur.execute(select_cart_query, (product_name,))
            cart_item = cur.fetchone()

            if cart_item:
                # Update quantity if the product is already in the cart
                new_quantity = cart_item[3] + quantity #existing quantity in the cart + new quantity
                update_cart_query = "UPDATE cart SET quantity = %s WHERE product_name = %s"
                cur.execute(update_cart_query, (new_quantity, product_name))
            else:
                # Add the product to the cart
                insert_cart_query = "INSERT INTO cart (product_name, product_price, quantity, product_image) VALUES (%s, %s, %s, %s)"
                cur.execute(insert_cart_query, (product_name, product_price, quantity, product_image))

            mydb.commit()
        else:
            flash('Product not found')

        total_quantity_query = "SELECT SUM(quantity) FROM cart"
        cur.execute(total_quantity_query)
        total_quantity = cur.fetchone()[0] or 0  # handle None result

        return render_template('home.html', cart_quantity=total_quantity)




@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if request.method == 'POST':
        product_name = request.form.get('product_id')

        # Remove the product from the cart
        delete_cart_query = "DELETE FROM cart WHERE product_name = %s"
        cur.execute(delete_cart_query, (product_name,))
        mydb.commit()
        flash('Product removed from cart')

    return redirect(url_for('view_cart'))

@app.route('/update_cart', methods=['POST'])
def update_cart():
    if request.method == 'POST':
        product_name = request.form.get('product_id')

        # Fetch product details from the database
        select_query = "SELECT name, price FROM products WHERE name = %s"
        cur.execute(select_query, (product_name,))
        product_details = cur.fetchone()

        if product_details:
            new_quantity = int(request.form.get('quantity', 1))

            # Update the quantity in the cart
            update_cart_query = "UPDATE cart SET quantity = %s WHERE product_name = %s"
            cur.execute(update_cart_query, (new_quantity, product_name))
            mydb.commit()
            flash('Cart updated')

        else:
            flash('Product not found')

    return redirect(url_for('view_cart'))


def get_cart_items():
    select_cart_query = "SELECT product_name, product_price, quantity, product_image FROM cart WHERE product_name IS NOT NULL AND product_price IS NOT NULL AND product_image IS NOT NULL"
    cur.execute(select_cart_query)
    cart_items_data = cur.fetchall()
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

    # dine_in_form = DineInForm(request.form)
    #
    # if request.method == 'POST' and dine_in_form.validate():
    #     # Fetch cart items
    #     select_cart_query = "SELECT product_name, product_price, quantity, product_image FROM cart WHERE product_name IS NOT NULL AND product_price IS NOT NULL AND product_image IS NOT NULL"
    #     cur.execute(select_cart_query)
    #     cart_items_data = cur.fetchall()
    #
    #     # Create CartItem instances from the fetched data
    #     cart_items = [CartItem(item[0], item[1], item[3], quantity=item[2]) for item in cart_items_data]
    #
    #     # Calculate total price
    #     total_price = sum(
    #         item.get_price() * item.get_quantity() if item.get_price() is not None and item.get_quantity() is not None else 0
    #         for item in cart_items)
    #
    #     dine_in_time = dine_in_form.time.data
    #     pax = dine_in_form.pax.data
    #
    #     # Store the information in the database (you need to modify this part based on your database structure)
    #     insert_order_info_query = "INSERT INTO order_info (order_type, dine_in_time, pax) VALUES (%s, %s, %s)"
    #     mycursor.execute(insert_order_info_query, ('dine_in', dine_in_time, pax))
    #     mydb.commit()
    #
    #     return render_template('dine_in.html', cart_items=cart_items, total_price=total_price, form=dine_in_form)
    #
    # return render_template('dine_in.html', form=dine_in_form)
@app.route('/dine_in', methods=['GET', 'POST'])
def dine_in():
    cart_items = get_cart_items()
    total_price = calculate_total_price(cart_items)

    dine_in = DineIn(time="", pax="")

    dine_in_form = DineInForm(request.form)

    if request.method == 'POST' and dine_in_form.validate():
        time = dine_in_form.time.data
        pax = dine_in_form.pax.data


        dine_in = DineIn(time, pax)

        # Store the information in the database (modify this part based on your database structure)
        insert_order_info_query = "INSERT INTO order_info (order_type, dine_in_time, pax) VALUES (%s, %s, %s)"
        mycursor.execute(insert_order_info_query, ('dine_in', dine_in.get_time(), dine_in.get_pax()))
        my_db.commit()

        return render_template('dine_in.html', cart_items=cart_items, total_price=total_price, dine_in=dine_in, form=dine_in_form)

    return render_template('dine_in.html', cart_items=cart_items, total_price=total_price, dine_in=dine_in,form=dine_in_form)



@app.route("/delivery", methods=['GET', 'POST'])
def delivery():
    # Fetch cart items
    cart_items = get_cart_items()
    delivery_fee = 5
    total_price = calculate_total_price(cart_items)
    new_total = total_price + delivery_fee

    delivery_form = DeliveryForm(request.form)

    if request.method == 'POST' and delivery_form.validate():
        street = delivery_form.street.data
        block = delivery_form.block.data
        unit_no = delivery_form.unit_no.data
        postal_code = delivery_form.postal_code.data



        # Create a Delivery instance
        delivery = Delivery(street, block, unit_no, postal_code)


        # Store the information in the database
        insert_order_info_query = "INSERT INTO order_info (order_type, street, block, unit_no, postal_code) VALUES (%s, %s, %s, %s, %s)"
        mycursor.execute(insert_order_info_query,
                         ('delivery', delivery.get_street(), delivery.get_block(), delivery.get_unit_no(), delivery.get_postal_code()))
        my_db.commit()

        # Redirect to a confirmation page or another relevant page
        return render_template('delivery.html', cart_items=cart_items, new_total=new_total, total_price=total_price, delivery_fee=delivery_fee, delivery=delivery, form=delivery_form)

    return render_template("delivery.html", cart_items=cart_items, new_total=new_total, total_price=total_price, delivery_fee=delivery_fee, form=delivery_form)



@app.route("/collection", methods=['GET', 'POST'])
def collection():
    # Fetch cart items
    cart_items = get_cart_items()
    total_price = calculate_total_price(cart_items)

    if request.method == 'POST':

        # Store the information in the database
        insert_order_info_query = "INSERT INTO order_info (order_type) VALUES ( %s)"
        mycursor.execute(insert_order_info_query, 'collection')
        my_db.commit()

        return render_template('collection.html', cart_items=cart_items, total_price=total_price)

    return render_template('collection.html', cart_items=cart_items, total_price=total_price)

@app.route("/delivery_finished")
def delivery_finished():
    return render_template('delivery_finished.html')

@app.route("/dine_in_finished")
def dine_in_finished():
    return render_template('dine_in_finished.html')

@app.route("/profile")
def profile():
    return render_template('profile.html')


@app.route('/reviews')
def reviews():
    return render_template('reviews.html')




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


if __name__ == '__main__':
    app.run()


