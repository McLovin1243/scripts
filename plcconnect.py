import snap7
import time
import sys
import socket
import threading

#This python program is the server program that proccess all the commmuncation.

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

def handle_client(conn,addr):
    print("NVIDIA Object detecion software running")
    connected = True
    while connected:
        msg_length=conn.recv(64).decode('utf-8')
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode('utf-8')

        if msg == "!DISCONNECT":
            connected = False

def start_client():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()





serverIP ='192.168.0.3' #NVIDIA JETSON LOCAL IP ADRESS
Port = 5025 #PORT nvidia jetson

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((serverIP,Port))



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

# Creating PLC client and connecting to registred info
plc = snap7.client.Client()
plc.connect(PLCIP, RACK, SLOT)

plcStatus = plc.get_cpu_state()
print(plcStatus)
start_client() #Starting connection with docker container


stateNvidia = True

while plcStatus == "S7CpuStatusRun":
    time.sleep(1)
    statePLC = ReadBool(db_number,start_offset, sbRunProcess_bit_offset)
    EMGStopPLC = ReadBool(db_number,start_offset, sbEMGStop_bit_offset)

    if stateNvidia == True:
        WriteBool(db_number,start_offset, sbRunProcess_bit_offset, outputOn)
        statePLC = ReadBool(db_number,start_offset, sbRunProcess_bit_offset)
        
    if stateNvidia == False:
        WriteBool(db_number,start_offset, sbRunProcess_bit_offset,outputOff)
        statePLC = ReadBool(db_number,start_offset, sbRunProcess_bit_offset)

    if EMGStopPLC == True:
        print("EMERGENCY STOP")
        time.sleep(2)
        print("3")
        time.sleep(2)
        print("2")
        time.sleep(2)
        print("1")
        time.sleep(1)
        print("SHUTDOWN")
        time.sleep(1)
        sys.exit()
        break


#WriteBool(db_number,start_offset, sbRunProcess_bit_offset, sbRunProcess_value)
#WriteBool(sbEMGStop_db_number,sbEMGStop_start_offset, sbEMGStop_bit_offset, sbEMGStop_value)
#WriteBool(sbStopProcess_db_number,sbStopProcess_start_offset, sbStopProcess_bit_offset, sbStopProcess_value)