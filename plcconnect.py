import snap7

IP = '192.168.0.1'
print(IP)
RACK = 0
SLOT = 0
plc = snap7.client.Client()
plc.connect(IP, RACK, SLOT)

print(plc.get_cpu_state())

data = plc.dbCommunication(1, 0, 4)
print(data)
