###############################################################################
# File Name: mini_project_02.py
#
# Description: This program implements a Flask-based web application that 
# allows users to add, store, and search products in an SQLite database with 
# form validation, dynamic querying, and HTML template rendering.
#
# Record of Revisions (Date | Author | Change):
# 05/03/2024 | Rhys DeLoach | Initial creation
###############################################################################

# Import Libraries
from flask import Flask, render_template, request
import sqlite3
import pandas as pd

app = Flask(__name__)

# Home Page Route
@app.route('/')
def home():
    return render_template('home.html')

# Add Product Page Route
@app.route('/add', methods = ['POST', 'GET'])
def add():
        if request.method == 'POST':
            category = request.form.get('category').upper().strip() # Get Category from Form
            description = request.form.get('description').upper().strip() # Get Description from Form
            price = request.form.get('price').strip() # Get Price from Form

            if category == '' or price == '' or description == '': # Tests for Empty Entries and Loads Error Message if there are
                return render_template('add_null_error.html')
            
            else: # Tests that price is a number
                try:
                    price = float(price)
                except ValueError:
                    return render_template('price_error.html')  
                
                else: # Initializes and connects to sqlite 
                    with sqlite3.connect("data/CommerceDatabase.db") as con:
                        with open("data/CommerceDatabase.sql") as file:
                            con.executescript(file.read())

                        table = pd.read_sql("SELECT * FROM items", con) # Sets the Database as a Table
                        if category in table['CATEGORY'].values: # Determines Whether the Category is in the Database     
                            category_count = table[table['CATEGORY'] == category].shape[0] + 1
                        else:
                            category_count = 1
                        id = category + str(category_count) # Creates Unique ID for the Entry
                        
                        price = f'${price:.2f}' # Putting Price in Money Format

                        insert = [(category,description,price,id)] # Insert into Database
                        con.executemany("INSERT INTO items VALUES (?,?,?,?)",insert)
                        con.commit()                         
                return render_template('home.html')
        return render_template('add.html')


#Search Product Route
@app.route('/search', methods = ['POST', 'GET'])
def search():
    if request.method == 'POST':
            search = request.form.get('search').upper().strip() # Get Category Search from Form

            with sqlite3.connect("data/CommerceDatabase.db") as con: # Initializes and connects to sqlite 
                with open("data/CommerceDatabase.sql") as file:
                     con.executescript(file.read())
                table = pd.read_sql("SELECT * FROM items", con)

                if search in table['CATEGORY'].values: # Verifies Category Exists in Database
                    return render_template('result.html', data=table[table['CATEGORY'] == search].to_records())
                elif search == '': # Loads Whole Database upon No Entry
                    return render_template('result.html', data=table.to_records())
                else: # Enters Error Message if Category Doesn't Exist
                    return render_template('invalid_search.html')                                               
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)