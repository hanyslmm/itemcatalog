#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, flash
# import all modules needed for configuration
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Base, Restaurant, MenuItem
# initializes an app variable, using the __name__ attribute
app = Flask(__name__)
# === let program know which database engine we want to communicate===
engine = create_engine('sqlite:///restaurantmenu.db', connect_args={'check_same_thread': False}, echo=True, convert_unicode=True)
# bind the engine to the Base class corresponding tables
Base.metadata.bind = engine
# create session maker object
DBSession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind = engine))
session = DBSession()

# list all restaurant Name
@app.route('/')
@app.route('/restaurant')
def restaurantName():
    restaurant = session.query(Restaurant).all()
    return render_template('main.html', restaurant=restaurant)

# 1 create new restaurant
@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newrestaurant = Restaurant(name=request.form['name'])
        session.add(newrestaurant)
        session.commit()
        return redirect(url_for('restaurantName'))
    else:
        return render_template('newrestaurant.html')

# 2 list item in restaurant using its id
@app.route('/restaurant/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)

# 3: Create route for newMenuItem Function
@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("{} menu item Created!".format(newItem.name))
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

# 4: Create route for editMenuItem function
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash("{} menu item Edited!".format(editedItem.name)) # to make interaction with user
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)

# 5: Create a route for deleteMenuItem function
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash("{} menu item Deleted!".format(deletedItem.name)) # to make interaction with user
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR DELETEMENUITEM TEMPLATE
        return render_template(
            'deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=deletedItem)
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
