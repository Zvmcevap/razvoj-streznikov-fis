from concurrent import futures
import grpc

import naloga2_pb2
import naloga2_pb2_grpc


numbers = []


class Naloga2Servicer(naloga2_pb2_grpc.Naloga2Servicer):

    # Client sends one number, server stores it
    def SendOne(self, request, context):
        numbers.append(request.value)
        print("Stored:", request.value)
        return naloga2_pb2.Empty()

    # Client sends index, server returns number at that index
    def GetOne(self, request, context):
        if request.index < 0 or request.index >= len(numbers):
            context.abort(grpc.StatusCode.OUT_OF_RANGE, "Index out of range")

        return naloga2_pb2.Number(value=numbers[request.index])

    # Client sends a stream of numbers, server stores all of them
    def SendMore(self, request_iterator, context):
        for number in request_iterator:
            numbers.append(number.value)
            print("Stored:", number.value)

        return naloga2_pb2.Empty()

    # Server streams all stored numbers back to client
    def GetAll(self, request, context):
        for number in numbers:
            yield naloga2_pb2.Number(value=number)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    naloga2_pb2_grpc.add_Naloga2Servicer_to_server(
        Naloga2Servicer(),
        server
    )

    server.add_insecure_port("127.0.0.1:50052")
    print("Naloga 2 server running on 127.0.0.1:50052")

    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()