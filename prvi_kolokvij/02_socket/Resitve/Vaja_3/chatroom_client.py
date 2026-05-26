import socket
import select
import sys

HEADER_LENGTH = 10

IP = "149.62.71.186"
PORT = 1234
my_username = input("Username: ")

# Naredimo TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Povežemo se
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, sicer recv() blokira in je potrebno čakati, da kaj sprejme
client_socket.setblocking(False)

# Zakodiramo svoj username (in header) ter ju pošljemo
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

# Ko smo poslali username, lahko ponavljamo zanko s sporočili med uporabniki
while True:

    # Čakamo, da uporabnik napiše sporočilo
    message = input(f'{my_username} > ')

    # Če sporočilo ni prazno, ga pošljemo
    if message:

        # Zakodiramo sporočilo (in header) ter ju pošljemo
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        # Iteriramo čez prejeta sporočila
        while True:
            # Prejeta sporočila so v obliki (username_header username message_header message)
            # Prejmemo header uporabniškega imena, ki pove dolžino prejetega sporočila
            username_header = client_socket.recv(HEADER_LENGTH)

            # Če nismo ničesar prejeli, to pomeni, da je strežnik zaprl povezavo in zato zapremo program
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Dekodiramo dolžino uporabniškega imena
            username_length = int(username_header.decode('utf-8').strip())

            # Sprejmemo in dekodiramo 
            username = client_socket.recv(username_length).decode('utf-8')

            # Postopek ponovimo
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            # Prikažemo pošiljatelja in sporočilo
            print(f'{username} > {message}')
            
    except:
        continue

