# Restaurant Menu Web Application 

# Overview
The restaurant menu web app provides a list of items within a variety of restaurants, as well as provide a user registration and authentication system.
A user can add his own restaurant menu items and update or delete them.
The user does not need to be logged in in order to see the restaurant or items uploaded. However, users who created an item are the only users allowed to update or delete the item that they created.

This program uses third-party OAuth2 with Google. Some of the technologies used to build this application include Python, Flask, SQLALchemy, HTML, CSS and JavaScript.

# Run Project using Docker Container:
1- download and install docker from hub.docker.com

2- pull project images from terminal:

docker pull hanyslmm/crud_webapp

3- Run container with command override python3.6 project.py as following:

docker run -d -p 8009:5000 --name crudserver hanyslmm/crud_webapp python3.6 project.py

4- Open your browser and go to:

http://localhost:8009 to open home page


# JSON Endpoint:
1- To return JSON of all restaurant info in database:

http://localhost:8009/restaurant/JSON
or
http://localhost:5000/restaurant/JSON

2- To return JSON of all items in certin restaurant:

http://localhost:8009/restaurant/int:restaurant_id/menu/JSON
http://localhost:5000/restaurant/int:restaurant_id/menu/JSON


# Run Project using Ubuntu OS:

1- install git using apt-get install git

2- mkdir for your project 

3- run git init in the directory

4- run git clone https://github.com/hanyslmm/itemcatalog.git

5- run python3.7 project


mader by

hany salama
