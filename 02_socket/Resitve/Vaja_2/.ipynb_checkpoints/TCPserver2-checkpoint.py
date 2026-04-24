import socketserver
HEADER_LENGTH = 10

class handler(socketserver.BaseRequestHandler):
    def handle(self):
        header1 = self.request.recv(HEADER_LENGTH)
        message1 = self.request.recv(int(header1)).decode()
        
        header2 = self.request.recv(HEADER_LENGTH)
        message2 = self.request.recv(int(header2)).decode()
        
        print('Sporočilo 1 je {} in sporočilo 2 je {}'.format(message1, message2))
        
        if int(header1) > int(header2):
            self.request.sendall(message1.encode())
        else:
            self.request.sendall(message2.encode())
        
server = socketserver.TCPServer(('0.0.0.0',1235), handler)
server.serve_forever()
