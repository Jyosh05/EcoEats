

# # first file to run when starting the web application
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from werkzeug.utils import secure_filename
import os
# # from Forms import CreateUserForm
from Forms import CreateProductForm


import mysql.connector

app = Flask(__name__)

db_config = {
    'host':'localhost',
    'user':'root',
    'password':'JYOSHNA2006!',
    'database':'products'
}


@app.route('/create_product', methods=['GET', 'POST'])
def create_product():
    create_product_form = None  # Initialize create_product_form

    if request.method == 'POST':
        create_product_form = CreateProductForm(request.form)
        if create_product_form.validate():
            name = request.form['name']
            price = request.form['price']

            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (name, price))
                conn.commit()

                cursor.close()
                conn.close()

                return redirect("recommended.html")

            except Exception as e:
                # Handle exceptions, e.g., log the error or return an error response
                return f"An error occurred: {str(e)}"

    # Handle the case when the method is GET or the form validation fails
    return render_template('create_product.html', form=create_product_form)


