from concurrent import futures
import grpc

import grpc1_pb2
import grpc1_pb2_grpc


# Implementation of the gRPC service
class Naloga1Servicer(grpc1_pb2_grpc.Naloga1Servicer):

    # This function receives a Sporocilo object
    # and returns the same text in uppercase
    def Uppercase(self, request, context):
        return grpc1_pb2.Sporocilo(
            text=request.text.upper()
        )


def serve():
    # Create gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Register our service implementation
    grpc1_pb2_grpc.add_Naloga1Servicer_to_server(
        Naloga1Servicer(),
        server
    )

    # Server listens on localhost:50051
    server.add_insecure_port("127.0.0.1:50051")

    print("Server running on 127.0.0.1:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()