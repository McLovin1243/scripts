import snap7
import time
import sys
import socket
import tkinter as tk
import tkinter.font as tkFont
import threading

# This python program is the server program that proccess all the commmuncation.
# ----------------------------------------------------------------------------------------------------------------------------- #
# FIELDS

# PLC
plcIP = '192.168.0.1'
rack = 0
slot = 1

# Server
serverIP = "192.168.0.3"
plc = snap7.client.Client()
#serverIP = socket.gethostbyname(socket.gethostname())
port = 5151 # PORT nvidia jetson
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Adress from TIA Portal - dbCommunication
db_number = 2
start_offset = 0
# Static Bool - Run/Stop Process
sbRunProcess_bit_offset = 0
# Static Bool - Emergency Stop
sbEMGStop_bit_offset = 1

outputOn = 1
outputOff = 0

detectedPellets = 0
feedingstatus = 0
EMGStatus = 0

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
    print('DB Number:' + str(db_number) + ' Bit: ' + str(start_offset) + '.' + str(bit_offset) + ' Value: ' + str(a))
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
                print(EMGStatus)
            if msg == "true":
                WriteBool(db_number, start_offset,sbRunProcess_bit_offset, outputOn)
                feedingstatus = outputOn
            if msg == "false":
                WriteBool(db_number, start_offset,sbRunProcess_bit_offset, outputOff)
                feedingstatus = outputOff

def start_client():
    print(f"[Listening] server is listening on {serverIP}")
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

class App:
    def __init__(self, root):
        # Setting title
        root.title("Server-oversikt")
        # Setting window size
        width=600
        height=400
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        # LABELS

        # Label - TITLE SERVER
        lblServerTitle=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=38)
        lblServerTitle["font"] = ft
        lblServerTitle["fg"] = "#333333"
        lblServerTitle["justify"] = "center"
        lblServerTitle["text"] = "Server"
        lblServerTitle.place(relx=0.5, y=30, anchor=tk.CENTER)



        # Label - IP PLC
        lblPLCIP=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=10)
        lblPLCIP["font"] = ft
        lblPLCIP["fg"] = "#333333"
        lblPLCIP["justify"] = "center"
        lblPLCIP["text"] = "IP"
        lblPLCIP.place(x=50,y=105,width=70,height=25)

        # Label - PLC Rack
        lblPLCRack=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=10)
        lblPLCRack["font"] = ft
        lblPLCRack["fg"] = "#333333"
        lblPLCRack["justify"] = "center"
        lblPLCRack["text"] = "Rack"
        lblPLCRack.place(x=50,y=170,width=70,height=25)

        # Label - PLC Slot
        lblPLCSlot=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=10)
        lblPLCSlot["font"] = ft
        lblPLCSlot["fg"] = "#333333"
        lblPLCSlot["justify"] = "center"
        lblPLCSlot["text"] = "Slot"
        lblPLCSlot.place(x=50,y=230,width=70,height=25)

        # Label - IP Server
        lblIPServer=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=10)
        lblIPServer["font"] = ft
        lblIPServer["fg"] = "#333333"
        lblIPServer["justify"] = "center"
        lblIPServer["text"] = "IP"
        lblIPServer.place(x=170,y=105,width=70,height=25)

        # Label - Port Server
        lblServerPort=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=10)
        lblServerPort["font"] = ft
        lblServerPort["fg"] = "#333333"
        lblServerPort["justify"] = "center"
        lblServerPort["text"] = "Port"
        lblServerPort.place(x=170,y=170,width=70,height=25)

        # Label - PLC
        lblPLC=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=10)
        lblPLC["font"] = ft
        lblPLC["fg"] = "#333333"
        lblPLC["justify"] = "center"
        lblPLC["text"] = "PLC"
        lblPLC.place(x=50,y=80,width=70,height=25)
        lblPLC["bd"] = 1  # Adjust the border width as needed
        lblPLC["relief"] = tk.SOLID  # Solid border

        # Label - Server
        lblServer=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=10)
        lblServer["font"] = ft
        lblServer["fg"] = "#333333"
        lblServer["justify"] = "center"
        lblServer["text"] = "Server"
        lblServer.place(x=170,y=80,width=70,height=25)
        lblServer["bd"] = 1  # Adjust the border width as needed
        lblServer["relief"] = tk.SOLID  # Solid border     

        # Label - Pellets detected
        labelPelletsDetected=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=10)
        labelPelletsDetected["font"] = ft
        labelPelletsDetected["fg"] = "#333333"
        labelPelletsDetected["justify"] = "center"
        labelPelletsDetected["text"] = "Pellets detected"
        labelPelletsDetected.place(x=37,y=320,width=100,height=25)
        labelPelletsDetected["bd"] = 1  # Adjust the border width as needed
        labelPelletsDetected["relief"] = tk.SOLID  # Solid border 

        # Label - Pellets detected input
        lbPelletsDetected=tk.Listbox(root)
        ft = tkFont.Font(family='Arial',size=10)
        lbPelletsDetected["font"] = ft
        lbPelletsDetected["fg"] = "#333333"
        lbPelletsDetected["justify"] = "center"
        lbPelletsDetected.place(x=37,y=350,width=100,height=25)
        lbPelletsDetected["bd"] = 1  # Adjust the border width as needed
        lbPelletsDetected["relief"] = tk.SOLID  # Solid border 
        lbPelletsDetected.insert(0, detectedPellets)

        # ENTRIES

        # Entry - IP PLC
        entryPLCIP=tk.Entry(root)
        entryPLCIP["borderwidth"] = "1px"
        ft = tkFont.Font(family='Arial',size=10)
        entryPLCIP["font"] = ft
        entryPLCIP["fg"] = "#333333"
        entryPLCIP["justify"] = "center"
        entryPLCIP["text"] = ""
        entryPLCIP.place(x=30,y=130,width=112,height=30)
        entryPLCIP.insert(0,plcIP)
        def update_plcIP(event):
            global plcIP
            plcIP = entryPLCIP.get()
        entryPLCIP.bind("<KeyRelease>", update_plcIP)

        # Entry - Rack
        entryRack=tk.Entry(root)
        entryRack["borderwidth"] = "1px"
        ft = tkFont.Font(family='Arial',size=10)
        entryRack["font"] = ft
        entryRack["fg"] = "#333333"
        entryRack["justify"] = "center"
        entryRack["text"] = ""
        entryRack.place(x=30,y=190,width=112,height=30)
        entryRack.insert(0,rack)
        def update_rack(event):
            global rack
            rack = entryRack.get()
        entryRack.bind("<KeyRelease>", update_rack)

        # Entry - Slot
        entrySlot=tk.Entry(root)
        entrySlot["borderwidth"] = "1px"
        ft = tkFont.Font(family='Arial',size=10)
        entrySlot["font"] = ft
        entrySlot["fg"] = "#333333"
        entrySlot["justify"] = "center"
        entrySlot["text"] = ""
        entrySlot.place(x=30,y=250,width=112,height=30)
        entrySlot.insert(0,slot)
        def update_slot(event):
            global slot
            slot = entrySlot.get()
        entrySlot.bind("<KeyRelease>", update_slot)

        # Entry - Server IP
        entryServerIP=tk.Entry(root)
        entryServerIP["borderwidth"] = "1px"
        ft = tkFont.Font(family='Arial',size=10)
        entryServerIP["font"] = ft
        entryServerIP["fg"] = "#333333"
        entryServerIP["justify"] = "center"
        entryServerIP["text"] = ""
        entryServerIP.place(x=150,y=130,width=113,height=30)
        entryServerIP.insert(0,serverIP)
        def update_serverIP(event):
            global serverIP
            serverIP = entryServerIP.get()
        entryServerIP.bind("<KeyRelease>", update_serverIP)

        # Entry - Server Port
        entryServerPort=tk.Entry(root)
        entryServerPort["borderwidth"] = "1px"
        ft = tkFont.Font(family='Arial',size=10)
        entryServerPort["font"] = ft
        entryServerPort["fg"] = "#333333"
        entryServerPort["justify"] = "center"
        entryServerPort["text"] = ""
        entryServerPort.place(x=150,y=190,width=111,height=30)
        entryServerPort.insert(0,port)
        def update_port(event):
            global port
            port = entryServerPort.get()
        entryServerPort.bind("<KeyRelease>", update_port)

        # BUTTONS

        # Button - Start server
        btnStartServer=tk.Button(root)
        btnStartServer["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Arial',size=10)
        btnStartServer["font"] = ft
        btnStartServer["fg"] = "#000000"
        btnStartServer["justify"] = "left"
        btnStartServer["text"] = "Start server"
        btnStartServer.place(relx=0.95, rely=0.85, anchor=tk.SE)
        btnStartServer["command"] = self.btnStartServer

        # Button - Exit server
        btnAvslutt=tk.Button(root)
        btnAvslutt["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Arial',size=10)
        btnAvslutt["font"] = ft
        btnAvslutt["fg"] = "#000000"
        btnAvslutt["justify"] = "left"
        btnAvslutt["text"] = "Avslutt server"
        btnAvslutt.place(relx=0.95, rely=0.95, anchor=tk.SE)
        btnAvslutt["command"] = self.btnAvslutt

    # FUNCTION START SERVER
    def btnStartServer(self):
        global server_running
        print(f"PLC IP: {plcIP}")
        print(f"RACK: {rack}")
        print(f"SLOT: {slot}")
        print(f"SERVER IP: {serverIP}")
        print(f"SERVER PORT: {port}")
        print("----------------------------------------------------")

        # Creating PLC connection
        plc.connect(plcIP, rack, slot)
        plcStatus = plc.get_cpu_state()
        print(plcStatus)

        # Starting up server
        ADDR = (serverIP,port)
        server.bind(ADDR)
        print("Server started")
        print(f"PLC IP:{plcIP}")
        start_client()
          
    # FUNCTION EXIT APPLICATION
    def btnAvslutt(self):
         sys.exit()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()