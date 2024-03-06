import snap7
import time
import sys
import socket
import threading

# This python program is the server program that proccess all the commmuncation.

# FIELDS
PLCIP = '192.168.0.1'
print(PLCIP)
RACK = 0
SLOT = 1

outputOn = 1
outputOff = 0

# Adress from TIA Portal - dbCommunication
db_number = 2
start_offset = 2

# Static Bool - Run/Stop Process
sbRunProcess_bit_offset = 0

# Static Bool - Emergency Stop
sbEMGStop_bit_offset = 1


# Creating PLC connection
plc = snap7.client.Client()
plc.connect(PLCIP, RACK, SLOT)
plcStatus = plc.get_cpu_state()
print(plcStatus)

#serverIP = socket.gethostbyname(socket.gethostname())
serverIP = "192.168.0.3"
Port = 5151 #PORT nvidia jetson
ADDR = (serverIP,Port)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
print("Server started")
# ----------------------------------------------------------------------------------------------------------------------------- #

# FUNCTIONS

# Funksjon for å skrive ut boolsk verdi til PLS
def WriteBool(db_number, start_offset, bit_offset, value):
    reading = plc.db_read(db_number, start_offset,1 )
    snap7.util.set_bool(reading, 0, bit_offset, value)
    plc.db_write(db_number, start_offset, reading)
    return None


# Funksjon for å lese ut boolsk verdi fra PLS
def ReadBool(db_number, start_offset, bit_offset):
    reading =  plc.db_read(db_number, start_offset, 1)
    a = snap7.util.get_bool(reading, 0, bit_offset)
    # print('DB Number:' + str(db_number) + ' Bit: ' + str(start_offset) + '.' + str(bit_offset) + ' Value: ' + str(a))
    return a

def handle_client(conn, addr):
    print(f"NVIDIA Object detecion software running   {addr}")
    connected = True
    while connected:
        msg_length=conn.recv(64).decode('utf-8')
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode('utf-8')
            print(f"{msg}")
            
            if msg == "!DISCONNECT":
                WriteBool(db_number, start_offset,sbEMGStop_bit_offset, outputOn)
                connected = False
            if msg == "true":
                WriteBool(db_number, start_offset,sbRunProcess_bit_offset, outputOn)
            if msg == "false":
                WriteBool(db_number, start_offset,sbRunProcess_bit_offset, outputOff)
            
                


def start_client():
    print(f"[Listening] server is listening on {serverIP}")
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

# ----------------------------------------------------------------------------------------------------------------------------- #

# MAIN PROGRAM
        


start_client()



# WriteBool(db_number,start_offset, sbRunProcess_bit_offset, sbRunProcess_value)
# WriteBool(sbEMGStop_db_number,sbEMGStop_start_offset, sbEMGStop_bit_offset, sbEMGStop_value)
# WriteBool(sbStopProcess_db_number,sbStopProcess_start_offset, sbStopProcess_bit_offset, sbStopProcess_value)
    
# EMGStopPLC = ReadBool(db_number,start_offset, sbEMGStop_bit_offset)
