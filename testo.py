#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, escape
from flask import session as login_session # works like a dictionary store values in it
import random, string # to create a pseudo-random string identify eachh login session
# import all modules needed for sqlalchemy configuration
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Base, Restaurant, MenuItem
# google OAuth
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


# initializes an app variable, using the __name__ attribute
app = Flask(__name__)

# let program know which database engine we want to communicate
engine = create_engine('sqlite:///restaurantmenu.db', connect_args={'check_same_thread': False}, echo=True, convert_unicode=True)
# bind the engine to the Base class corresponding tables
Base.metadata.bind = engine

# create session maker object
DBSession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind = engine))
session = DBSession()

app.secret_key = '31sasd'

@app.route('/home')
def home():
    if 'username' in login_session:
        return "LOGGED IN AS {}".format(escape(login_session['username']))
    return "you are not logged in"

@app.route('/loginn', methods=['GET', 'POST'])
def loginn():
    if request.method == 'POST':
        login_session['username'] = request.form['username']
        return redirect(url_for('home'))
    return '''
            <form method='post'>
                <p><input type=text name=username>
                <p><input type=submit value=login>
            </form>
            '''
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    login_session.pop('username', None)
    return redirect(url_for('home'))



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
@app.route('/restaurant/<int:restaurant_id>/menu')
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
        return render_template(
            'deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=deletedItem)

# 6: Create JSON file for restaurant menu
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


# ADD JSON ENDPOINT HERE
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.development = True
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
