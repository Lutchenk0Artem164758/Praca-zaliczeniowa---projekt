import socket
import pickle
import random
from animal import Cat, Dog, Bird

HOST = '127.0.0.1'
PORT = 23456

def main():
    client_id = random.randint(1000, 9999)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.send(str(client_id).encode())

        status = sock.recv(1024).decode()
        if status == "REFUSED":
            print(f"Client {client_id}: connection refused.")
            return

        print(f"Client {client_id}: connected.")

        class_requests = ["cat", "dog", "unicorn"]

        for class_name in class_requests:
            sock.send(class_name.encode())

            data = sock.recv(4096)
            try:
                objs = pickle.loads(data)

                if isinstance(objs, list):
                    for obj in objs:
                        print(f"Client {client_id} received: {obj}")
                else:
                    raise TypeError("Invalid object type")

            except Exception as e:
                print(f"Client {client_id}: failed to read objects ({e})")

if __name__ == "__main__":
    main()
