#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect
from flask import url_for, flash, jsonify
from flask import session as login_session  # dictionary store values in it
import random  # to create a pseudo-random string identify each login session
import string
# import all modules needed for sqlalchemy configuration
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Base, User, Restaurant, MenuItem
# google OAuth
from oauth2client.client import flow_from_clientsecrets  # creates flow object
from oauth2client.client import FlowExchangeError
# occured during exchange an authorization code for an access token

import httplib2
import json
from flask import make_response
import requests  # to use args.get function

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu App"

# initializes an app variable, using the __name__ attribute
app = Flask(__name__)

# let program know which database engine we want to communicate
engine = create_engine('sqlite:///restaurantmenuwithusers.db',
                       connect_args={'check_same_thread': False},
                       echo=True, convert_unicode=True)
# bind the engine to the Base class corresponding tables
Base.metadata.bind = engine

# create session maker object
DBSession = scoped_session(sessionmaker(autocommit=False, autoflush=False,
                           bind=engine))
session = DBSession()


# User helper functions
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'],
                   user_type=1)
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user  # user object associated with his ID number


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# 1 login: Create anti-forgery state token
@app.route('/login')
def showLogin():
    choices = string.ascii_uppercase + string.digits
    state = ""
    for i in range(32):
        state += random.choice(choices)
    print(state)
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/callback', methods=['POST'])
def callback():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        # creates an OAuth flow object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        # specigy with post message one time flow
        oauth_flow.redirect_uri = 'postmessage'
        # initiate the exchange passing one time code as input
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        # send response as JSON object
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    # json GET request containing the URL and access token
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info,
    # abort and send internal server error to the client
    if result.get('error') is not None:  # result contains any error
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    google_id = credentials.id_token['sub']  # gplus_id
    if result['user_id'] != google_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check if user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_google_id = login_session.get('google_id')
    if stored_access_token is not None and google_id == stored_google_id:
        response = make_response(
                       json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['google_id'] = google_id

    # Use google plus API to get more user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    # Store data that we are intersted in
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't create new owner
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    # to make interaction with user
    flash("you are now logged in as {}".format(login_session['username']))
    print ("done!")
    return output


# Revoke current user and reset their login_session.
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    print (access_token)
    if access_token is None:
        print ('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # use acces token and pass it into Google's url
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    print ('shaghaaaaaal')
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print ('result is ')
    print (result)
    if result['status'] == '200' or result['status'] == '400':  # review
        username = login_session['username']
        del login_session['access_token']
        del login_session['google_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
    # response = make_response(json.dumps('Successfully disconnected.'), 200)
    # response.headers['Content-Type'] = 'application/json'
        # using flash to make interaction with user
        flash("{} logged out!".format(username))
        return redirect(url_for('restaurantName'))
    else:
        response = make_response(
                    json.dumps('Failed to revoke token for given user.', 401))
        response.headers['Content-Type'] = 'application/json'
        return response


# 2 list all restaurant Name
@app.route('/')
@app.route('/restaurant')
def restaurantName():
    restaurant = session.query(Restaurant).all()
    if 'username' not in login_session:
        return render_template('publicmain.html', restaurant=restaurant)
    else:
        return render_template('main.html', restaurant=restaurant)


# delete restaurant
@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def restaurantDelete(restaurant_id):
    deletedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    # verify that a user is logged in
    if 'username' not in login_session:
        return redirect('/login')
    if deletedRestaurant.user_id != login_session['user_id']:
        output = "<script>{alert('You are not authorized"
        output += " to delete this Restaurant.');}</script>"
        return output
    deletedItems = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    if request.method == 'POST':
        session.delete(deletedRestaurant)
        for deletedItem in deletedItems:
            session.delete(deletedItem)
        session.commit()
        # using flash to make interaction with user
        flash("{} Restaurant Deleted!".format(deletedRestaurant.name))
        return redirect(url_for('restaurantName'))
    else:
        return render_template('deleterestaurant.html',
                               restaurant_id=restaurant_id,
                               restaurant=deletedRestaurant)


# 1: create new restaurant
@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    # verify that a user is logged in
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newrestaurant = Restaurant(name=request.form['name'],
                                   user_id=login_session['user_id'])
        session.add(newrestaurant)
        session.commit()
        return redirect(url_for('restaurantName'))
    else:
        return render_template('newrestaurant.html')


# 3: list menu items in restaurant using its id
@app.route('/restaurant/<int:restaurant_id>/menu')
@app.route('/restaurant/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    creator = getUserInfo(restaurant.user_id)
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicmenu.html', restaurant=restaurant,
                               items=items, creator=creator)
    else:
        return render_template('menu.html', restaurant=restaurant,
                               items=items, creator=creator)


# 4: Create route for newMenuItem Function
@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    # verify that a user is logged in
    if 'username' not in login_session:
        return redirect('/login')
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        newItem = MenuItem(restaurant_id=restaurant_id,
                           user_id=restaurant.user_id)
        if request.form['name']:
            newItem.name = request.form['name']
        if request.form['price']:
            newItem.price = request.form['price']
        if request.form['course']:
            newItem.course = request.form['course']
        if request.form['description']:
            newItem.description = request.form['description']
        session.add(newItem)
        session.commit()
        flash("{} menu item Created!".format(newItem.name))
        return redirect(url_for('restaurantMenu',
                        restaurant_id=restaurant_id, restaurant=restaurant))
    else:
        return render_template('newmenuitem.html',
                               restaurant_id=restaurant_id,
                               restaurant=restaurant)


# 5: Create route for editMenuItem function
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    # verify that a user is logged in
    if 'username' not in login_session:
        return redirect('/login')
    if editedItem.user_id != login_session['user_id']:
        return
        "<script>{alert('You are not authorized to edit this');}</script>"
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['course']:
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        # to make interaction with user
        flash("{} menu item Edited!".format(editedItem.name))
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id,
            menu_id=menu_id, item=editedItem)


# 6: Create a route for deleteMenuItem function
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    # verify that a user is logged in
    if 'username' not in login_session:
        return redirect('/login')
    if deletedItem.user_id != login_session['user_id']:
        return
        "<script>{alert('You're not authorized to delete this');}</script>"
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        # to make interaction with user
        flash("{} menu item Deleted!".format(deletedItem.name))
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html',
                               restaurant_id=restaurant_id,
                               menu_id=menu_id, item=deletedItem)


# 7: Create JSON file for restaurant menu
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    # verify that a user is logged in
    if 'username' not in login_session:
        return redirect('/login')
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


# 8: Create JSON file for all restaurant
@app.route('/restaurant/JSON')
def restaurantJSON():
    restaurant = session.query(Restaurant).all()
    return jsonify(Restaurant=[i.serialize for i in restaurant])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
