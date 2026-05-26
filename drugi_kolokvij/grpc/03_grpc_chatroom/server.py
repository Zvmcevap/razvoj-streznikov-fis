from concurrent import futures
import time
import grpc

import chat_pb2
import chat_pb2_grpc


notes = []


class ChatServerServicer(chat_pb2_grpc.ChatServerServicer):

    # Client sends one chat message
    def SendNote(self, request, context):
        notes.append(request)
        print(f"{request.name}: {request.message}")
        return chat_pb2.Empty()

    # Server streams new chat messages to the client
    def ChatStream(self, request, context):
        last_index = 0

        while True:
            while last_index < len(notes):
                note = notes[last_index]
                last_index += 1
                yield note

            time.sleep(1)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    chat_pb2_grpc.add_ChatServerServicer_to_server(
        ChatServerServicer(),
        server
    )

    server.add_insecure_port("127.0.0.1:50053")
    print("Chat server running on 127.0.0.1:50053")

    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()