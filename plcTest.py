import snap7
import time
import sys
import socket
import threading

#This python program is the server program that proccess all the commmuncation.

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
