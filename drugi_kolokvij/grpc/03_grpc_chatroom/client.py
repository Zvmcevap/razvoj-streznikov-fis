import threading
import grpc

import chat_pb2
import chat_pb2_grpc


# This function constantly listens for new chat messages
def listen_for_messages(stub):
    for note in stub.ChatStream(chat_pb2.Empty()):
        print(f"\n{note.name}: {note.message}")


def run():
    name = input("Enter your username: ")

    channel = grpc.insecure_channel("127.0.0.1:50053")
    stub = chat_pb2_grpc.ChatServerStub(channel)

    # Start listener thread, so receiving and sending can happen at the same time
    listener = threading.Thread(
        target=listen_for_messages,
        args=(stub,),
        daemon=True
    )
    listener.start()

    print("Type messages. Use /exit to quit.")

    while True:
        text = input("> ")

        if text == "/exit":
            break

        note = chat_pb2.Note(
            name=name,
            message=text
        )

        stub.SendNote(note)


if __name__ == "__main__":
    run()