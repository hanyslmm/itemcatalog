#!/usr/bin/env python3
# This module defines classes for implementing HTTP web server.
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparsecd
import cgi # used to decipher the message from POST
# import all modules needed for configuration
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# === let program know which database engine we want to communicate===
engine = create_engine('sqlite:///restaurantmenu.db')
# bind the engine to the Base class corresponding tables
Base.metadata.bind = engine
# create session maker object
DBSession = sessionmaker(bind = engine)
session = DBSession()


# This class is used to handle the HTTP requests that arrive at the server.
class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(200) # send a 200 ok reponse.
                # then send headers
                self.send_header('Content-type', 'text/html; charset = utf-8')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method ='POST' enctype='multipart/form-data' action='/restaurants/new' >"
                output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restauarant Name' >"
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output.encode()) # Contains the output stream for writing a response back to the client
                print(output)
                return

            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                self.send_response(200) # send a 200 ok reponse.
                # then send headers
                self.send_header('Content-type', 'text/html; charset = utf-8')
                self.end_headers()
                output = ""
                output += "<a href = '/restaurants/new' > Make a New Restaurant Here </a><br></br>"
                output += "<html><body>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href ='#' >Edit</a>"
                    output += "</br>"
                    output += "<a href ='#' >Delete</a>"
                    output += "</br></br>"
                output += "</body></html>"
                self.wfile.write(output.encode()) # Contains the output stream for writing a response back to the client
                print(output)
                return
        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)
    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = [fields.get('newRestaurantName')]

                    # Create new Restaurant Object
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html; charset = utf-8')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
        except:
            pass

def main():
    try:
        port = 8008
        server = HTTPServer(('', port), WebServerHandler) # It creates and listens at the HTTP socket
        print("Web server running on port %s" % port)
        server.serve_forever()


    except KeyboardInterrupt:
        print("^C entered, stopping web server..")
        server.socket.close()
if __name__ == '__main__':
    main()
