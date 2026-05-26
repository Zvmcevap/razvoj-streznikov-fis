import grpc

import grpc1_pb2
import grpc1_pb2_grpc


def run():
    # Connect to the gRPC server
    channel = grpc.insecure_channel("127.0.0.1:50051")

    # Create client stub
    stub = grpc1_pb2_grpc.Naloga1Stub(channel)

    # Read message from user
    text = input("Vnesi sporocilo: ")

    # Create request object
    request = grpc1_pb2.Sporocilo(text=text)

    # Send request to server
    response = stub.Uppercase(request)

    # Print server response
    print("Odgovor serverja:", response.text)


if __name__ == "__main__":
    run()