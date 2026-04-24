import socket
import select

HEADER_LENGTH = 10

IP = "0.0.0.0"
PORT = 1234

# Naredimo socket - TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# SOL_ - socket option level
# S tem SO_REUSEADDR postavimo na 1, address lahko uporabljamo večkrat
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind
server_socket.bind((IP, PORT))

# Socket nastavimo na listen
server_socket.listen()

# Seznam vseh socketov
sockets_list = [server_socket]

# Seznam vseh uporabnikov
clients = {}

print(f'Listening for connections on {IP}:{PORT}...')

# Sprejme sporočilo
def receive_message(client_socket):

    try:
        # Preberi header, ki je vedno enako dolg (pove dolžino sporočila)
        message_header = client_socket.recv(HEADER_LENGTH)
        
        # Napaka - ni sporočila
        if not len(message_header):
            return False

        # Preberi dolžino sporočila
        message_length = int(message_header.decode('utf-8').strip())

        # Vrnemo objekt, ki vsebuje header in samo sporočilo ('data')
        return {'header': message_header, 'data': client_socket.recv(message_length)}
    except:
        return False # Napaka

while True:
    # Z naslednjo vrstico čakamo na dogodek. Dobimo read_sockets seznam socketov, kjer se je nekaj zgodilo.
    read_sockets, _, _ = select.select(sockets_list, [], sockets_list) # Blokira, dokler nečesa ne sprejme

    # Iteriramo čez sockete, kjer se je kaj zgodilo
    for notified_socket in read_sockets:
        
        # if "imamo novega uporabnika":
        if notified_socket == server_socket:

            # Sprejmimo povezavo, imamo nov socket client_socket za novega uporabnika.
            client_socket, client_address = server_socket.accept()

            # Po povezavi uporanik sporoči Uporabniško ime
            user = receive_message(client_socket)

            # Če je uporabnik prekinil povezavo, ni poslal imena
            if user is False:
                continue

            # Sicer socket dodamo na seznam socketov
            sockets_list.append(client_socket)

            # In shranimo uporabniško ime
            clients[client_socket] = user
            print('Sprejeta povezava od {}:{}, uporabniško ime: {}'.format(*client_address, user['data'].decode('utf-8')))

        # if "nimamo novega uporabnika", smo dobili sporočilo!
        else:

            # Sprejmemo sporočilo
            message = receive_message(notified_socket)

            # If False: v tem primeru je uporabnik zaprl povezavo, za njim "počistimo"
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                # Odstranimo socket
                sockets_list.remove(notified_socket)

                # Odstranimo uporabniško ime
                del clients[notified_socket]

                continue

            # Poiščemo uporabniško ime preko socketa, ki je aktiven
            user = clients[notified_socket]

            print(f'Prejeto sporočilo od {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            # Sporočilo pošljemo vsem uporabnikom, razen...
            for client_socket in clients:

                # Razen tistemu, ki je sporočilo poslal
                if client_socket != notified_socket:

                    # Uporabnikom pošljemo sporočilo in ime uporabnika, ki ga je poslal
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
