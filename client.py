import socket
HEADER = 64
port =5050
FORMAT = 'utf-8'
SERVER =  '192.168.1.28'
ADDR = (SERVER,port)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length =str(msg_length).encode(FORMAT)
    send_length += b' '*(HEADER-len(send_length))
    client.send(send_length)
    client.send(message)
    
send("true")