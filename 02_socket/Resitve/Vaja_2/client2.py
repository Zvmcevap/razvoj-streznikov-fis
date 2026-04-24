import socket

HEADER_LENGTH = 10
message1 = 'Prvo sporočilo'.encode()
message2 = 'Drugo sporočilo'.encode()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(('0.0.0.0', 1235))
    header1 = f"{len(message1):<{HEADER_LENGTH}}".encode('utf-8')
    header2 = f"{len(message2):<{HEADER_LENGTH}}".encode('utf-8')
    sock.sendall(header1+message1+header2+message2)
    message = sock.recv(1024)
    print(message.decode())
    
    
message1length = int(sock.recv(10))
message1 = sock.recv(messsage1length)

message2length = int(sock.recv(10))
message2 = sock.recv(messsage2length)