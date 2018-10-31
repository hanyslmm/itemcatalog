from BasedHTTPServer import BasedHTTPReuestHandler, HTTPServer

class webserverHandler(BasedHTTPReuestHandler):
    def do_GET(self):
        try:
            if self.path_response(200):
                self.senf_response(200)
                self.send_header('Conternt-type', 'text/html')
                self.send_headers()

                output = ""
                output += "<html><body>Hello!</body></html>"
                self.wfile.write(output)
                print(output)
                return
        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print("Web server running on port %s" % port)
        server.serve_forever()


    except KeyboardInterrupt:
        print("^C entered, stopping web server..")
        server.socket.close()
if __name__ == '__main__':
    main()
