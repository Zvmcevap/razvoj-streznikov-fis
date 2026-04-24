import socket
import select

HEADER_LENGTH = 10

IP = "0.0.0.0"
PORT = 1234

# Naredimo socket - TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# SOL_ - socket option level. S tem SO_REUSEADDR postavimo na 1, address lahko uporabljamo večkrat
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind

server_socket.bind((IP, PORT))

# Socket nastavimo na listen

server_socket.listen()

# Seznam vseh socketov
sockets_list = [server_socket]

# Seznam vseh uporabnikov. {} je v pythonu slovar, ki bo oblike {socketobjekt : username}
clients = {}

print(f'Listening for connections on {IP}:{PORT}...')

# Sprejme sporočilo
def receive_message(client_socket):
    """ Ta funkcija bo iz željenega socketa sprejela sporočilo oblike [header sporočilo] """
    try:
        # Preberi header, ki je vedno enako dolg (pove dolžino sporočila)
        
        # Napaka - ni sporočila
        if not len(message_header):
            return False

        # Preberi dolžino sporočila

        # Vrnemo objekt, ki vsebuje 'header' in samo sporočilo ('data')
        return {'header' : header, 'data' : message}
    except:
        return False # Napaka

while True:
    # Z naslednjo vrstico čakamo na dogodek. Dobimo read_sockets seznam socketov, kjer se je nekaj zgodilo.
    read_sockets, _, _ = select.select(sockets_list, [], sockets_list) # Blokira, dokler nečesa ne sprejme

    # Iteriramo čez sockete, kjer se je kaj zgodilo
    for notified_socket in read_sockets
        
        # if "imamo novega uporabnika":
        if notified_socket == server_socket:


            # Sprejmimo povezavo (funkcija accept()), imamo nov socket client_socket za novega uporabnika.
            
            client_socket, client_address = server_socket.accept()

            # Po povezavi uporanik sporoči Uporabniško ime

            # Če je uporabnik prekinil povezavo, ni poslal imena
            if user is False:
                continue

            # Sicer socket dodamo na seznam socketov

            # In shranimo uporabniško ime v slovar clients

            # Print
            print('Sprejeta povezava od {}:{}, uporabniško ime: {}'.format(*client_address, user['data'].decode('utf-8')))

        # if "nimamo novega uporabnika", smo dobili sporočilo!
        else:

            # Sprejmemo sporočilo

            # If False: v tem primeru je uporabnik zaprl povezavo, za njim "počistimo"
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                # Odstranimo socket (list.remove)
                sockets_list.remove(notified_socket)

                # Odstranimo uporabniško ime (del iz dictionary)
                del clients[notified_socket]

                continue

            # Poiščemo uporabniško ime preko socketa, ki je aktiven

            print(f'Prejeto sporočilo od {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            # Sporočilo pošljemo vsem uporabnikom, razen...

                # Razen tistemu, ki je sporočilo poslal

                    # Uporabnikom pošljemo sporočilo in ime uporabnika, ki ga je poslal. Oblika sporočila: username header, username, sporočilo header, sporočilo
                    