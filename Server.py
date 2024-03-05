import socket
import threading
serverIP = socket.gethostbyname(socket.gethostname())
Port = 5050 #PORT nvidia jetson
ADDR = (serverIP,Port)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
serverIP = socket.gethostbyname(socket.gethostname())
Port = 5050 #PORT nvidia jetson
ADDR = (serverIP,Port)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"NVIDIA Object detecion software running   {addr}")
    connected = True
    while connected:
        msg_length=conn.recv(64).decode('utf-8')
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode('utf-8')
            if msg == "!DISCONNECT":
                connected = False

    conn.close()

def start_client():
    print(f"[Listening] server is listening on {serverIP}")
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()



print("[Starting] server is starting...")
start_client()