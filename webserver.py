#!/usr/bin/env python3


# This module defines classes for implementing HTTP web server.
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi # used to decipher the message from POST
import cgitb
cgitb.enable()
# This class is used to handle the HTTP requests that arrive at the server.
class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200) # send a 200 ok reponse.
                # then send headers
                self.send_header('Content-type', 'text/html; charset = utf-8')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>"
                output += "<a href = '/hola'>go to Hola</a></body></html>"
                self.wfile.write(output.encode()) # Contains the output stream for writing a response back to the client
                print(output)
                return
            if self.path.endswith("/hola"):
                self.send_response(200) # send a 200 ok reponse.
                # then send headers
                self.send_header('Content-type', 'text/html; charset = utf-8')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>&#161Hola!!</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>"
                output += "<a href = /hello>Back to Hello</a></body></html>"

                self.wfile.write(output.encode()) # Contains the output stream for writing a response back to the client
                print(output)
        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)
    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html; charset = utf-8')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type', 'text/html; charset = utf-8'))
            #pdict['boundary'] = bytes(pdict['boundary'], "utf-8")

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

            output = ""
            output += "<html><body>"
            output += "<h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messageconten[0]
            output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>"
            output += "</body></html>"
            self.wfile.write(output.encode())
            print(output)
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
