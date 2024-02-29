import snap7
import time

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
    print('DB Number:' + str(db_number) + ' Bit: ' + str(start_offset) + '.' + str(bit_offset) + ' Value: ' + str(a))
    return a

IP = '192.168.0.1'
print(IP)
RACK = 0
SLOT = 1

# Static Bool - Run Process
sbRunProcess_db_number = 2
sbRunProcess_start_offset = 2
sbRunProcess_bit_offset = 0
sbRunProcess_value = 0  # 1 = True & 0 = False

# Static Bool - Emergency Stop
sbEMGStop_db_number = 2
sbEMGStop_start_offset = 2
sbEMGStop_bit_offset = 1
sbEMGStop_value = 0  # 1 = True & 0 = False
# Static Bool - Stop Process
sbStopProcess_db_number = 2
sbStopProcess_start_offset = 2
sbStopProcess_bit_offset = 2
sbStopProcess_value = 0  # 1 = True & 0 = False

plc = snap7.client.Client()
plc.connect(IP, RACK, SLOT)

plcStatus = plc.get_cpu_state()
print(plcStatus)

while plcStatus == "S7CpuStatusRun":
    ReadBool(db_number2, start_offset2, bit_offset2)
#    if input() == "y":
#       WriteBool(db_number2, start_offset2, bit_offset2, value2)
    if ReadBool(db_number2, start_offset2, bit_offset2) == True:
       break
