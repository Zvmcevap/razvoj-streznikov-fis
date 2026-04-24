import socket
import select
import sys

HEADER_LENGTH = 10

IP = "0.0.0.0"
PORT = 1234
my_username = input("Username: ")

# Naredimo TCP socket
client_socket = 

# Povežemo se


# Set connection to non-blocking state, sicer recv() blokira in je potrebno čakati, da kaj sprejme

client_socket.setblocking(False)


# Zakodiramo svoj username (in header) ter ju pošljemo

# Ko smo poslali username, lahko ponavljamo zanko s sporočili med uporabniki
while True:

    # Čakamo, da uporabnik napiše sporočilo
    message = input(f'{my_username} > ')

    # Če sporočilo ni prazno, ga pošljemo

        # Zakodiramo sporočilo (in header) ter ju pošljemo

    try:
        # Iteriramo čez prejeta sporočila
        while True:
            # Prejeta sporočila so v obliki (username_header username message_header message)
            # Prejmemo header uporabniškega imena, ki pove dolžino prejetega sporočila

            # Če nismo ničesar prejeli, to pomeni, da je strežnik zaprl povezavo in zato zapremo program
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Dekodiramo dolžino uporabniškega imena

            # Sprejmemo in dekodiramo 

            # Postopek ponovimo za vsebino sporočila

            # Prikažemo pošiljatelja in sporočilo
            print(f'{username} > {message}')
            
    except:
        continue

