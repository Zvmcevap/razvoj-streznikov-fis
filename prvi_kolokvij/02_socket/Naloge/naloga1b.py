import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    """ Handle naj sprejme sporočilo, in sporočilo pošlje nazaj"""
    def handle(self):

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 1234
    
    # Uporabite socketserver.TCPserver, handler MyTCPHandler, in server.serve_forever()
    with 