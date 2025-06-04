import socket
import threading
import pickle
import random
import time
from animal import Cat, Dog, Bird

HOST = '127.0.0.1'
PORT = 23456
MAX_CLIENTS = 3

animal_map = {}
active_clients = set()
lock = threading.Lock()

def init_animals():
    for i in range(1, 5):
        animal_map[f"cat_{i}"] = Cat(f"Cat{i}", i + 2)
        animal_map[f"dog_{i}"] = Dog(f"Dog{i}", i + 1)
        animal_map[f"bird_{i}"] = Bird(f"Bird{i}", i + 3)

def handle_client(conn, addr):
    try:
        client_id = int(conn.recv(1024).decode())
        with lock:
            if len(active_clients) >= MAX_CLIENTS:
                conn.send(b'REFUSED')
                print(f"To the client {client_id} denied")
                conn.close()
                return
            else:
                active_clients.add(client_id)
                conn.send(b'OK')
                print(f"Client {client_id} connected")

        for _ in range(3):
            class_name = conn.recv(1024).decode().lower()
            time.sleep(random.uniform(0.5, 1.5))

            result = [obj for key, obj in animal_map.items() if key.startswith(class_name)]

            if result:
                data = pickle.dumps(result)
                conn.sendall(data)
                print(f"Sent to customer {client_id}: {[str(o) for o in result]}")
            else:
                fallback = pickle.dumps([Dog("Reserve", 0)])
                conn.sendall(fallback)
                print(f"Sent to customer {client_id}: [Dog(Reserve, age=0)]")

    except Exception as e:
        print(f"Error with the client: {e}")
    finally:
        with lock:
            active_clients.discard(client_id)
        conn.close()

def start_server():
    init_animals()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print("The server is running...")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
