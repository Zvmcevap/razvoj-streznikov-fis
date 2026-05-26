import grpc

import naloga2_pb2
import naloga2_pb2_grpc


# Generator used for client-side streaming
def number_generator():
    raw = input("Enter numbers separated by spaces: ")

    for item in raw.split():
        yield naloga2_pb2.Number(value=float(item))


def run():
    channel = grpc.insecure_channel("127.0.0.1:50052")
    stub = naloga2_pb2_grpc.Naloga2Stub(channel)

    while True:
        print("\n1 - SendOne")
        print("2 - GetOne")
        print("3 - SendMore")
        print("4 - GetAll")
        print("0 - Exit")

        choice = input("Choose: ")

        if choice == "1":
            value = float(input("Number: "))
            stub.SendOne(naloga2_pb2.Number(value=value))
            print("Number sent.")

        elif choice == "2":
            index = int(input("Index: "))
            response = stub.GetOne(naloga2_pb2.Index(index=index))
            print("Number at index:", response.value)

        elif choice == "3":
            stub.SendMore(number_generator())
            print("Numbers sent.")

        elif choice == "4":
            print("All stored numbers:")
            for response in stub.GetAll(naloga2_pb2.Empty()):
                print(response.value)

        elif choice == "0":
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    run()