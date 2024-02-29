import snap7

IP = '192.168.0.1'
print(IP)
RACK = 0
SLOT = 1

db_number = 2
start_offset = 2
bit_offset = 0
value = 1

plc = snap7.client.Client()
plc.connect(IP, RACK, SLOT)

print(plc.get_cpu_state())

# data = plc.dbCommunication(1, 0, 4)
# print(data)

# Funksjon for å skrive ut boolsk verdi til PLS
def WriteBool(db_number, start_offset, bit_offset):
    reading = plc.db_read(db_number, start_offset,1)
    a = snap7.util.get_bool(reading, 0, bit_offset)
    plc.db_write(db_number, start_offset, reading)
    return None


# Funksjon for å lese ut boolsk verdi fra PLS
def ReadBool(db_number, start_offset, bit_offset):
    reading =  plc.db_read(db_number, start_offset, 1)
    a = snap7.util.get_bool(reading, 0, bit_offset)
    print('DB Number:' + str(db_number) + ' Bit: ' + str(start_offset) + '.' + str(bit_offset) + ' Value: ' + str(a))

WriteBool(db_number, start_offset, bit_offset, value)

ReadBool(db_number, start_offset, bit_offset)
