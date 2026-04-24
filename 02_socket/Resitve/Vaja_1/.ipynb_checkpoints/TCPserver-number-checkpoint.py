import socketserver

class TCPHandler(socketserver.BaseRequestHandler):


    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("{} wrote: ".format(self.client_address[0]))
        print(self.data.decode())
        
        try:
            stevilo = int(self.data.decode('UTF-8'))
            self.request.sendall(bytes('Poslali ste število ', "utf-8") + self.data)
        except:
            self.request.sendall(bytes('Pošljite število', "utf-8"))

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 1234

    with socketserver.TCPServer((HOST, PORT), TCPHandler) as server: # Ustvari strežnik z imenom server

        server.serve_forever() # Sam se ne ugasne