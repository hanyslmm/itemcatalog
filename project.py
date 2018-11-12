#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for
# import all modules needed for configuration
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)
# === let program know which database engine we want to communicate===
engine = create_engine('sqlite:///restaurantmenu.db', connect_args={'check_same_thread': False}, echo=True, convert_unicode=True)
# bind the engine to the Base class corresponding tables
Base.metadata.bind = engine
# create session maker object
DBSession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind = engine))
session = DBSession()

# list item in restaurant using its id
@app.route('/restaurant/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)

# Task 1: Create route for newMenuItem Function
@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


# Task 2: Create route for editMenuItem function


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item."

# Task 3: Create a route for deleteMenuItem function


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item."


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
