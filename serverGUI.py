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
                EMGStatus = 1
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
        width=1000
        height=600
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        # LABELS

        # Label - TITLE SERVER
        GLabel_637=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=38)
        GLabel_637["font"] = ft
        GLabel_637["fg"] = "#333333"
        GLabel_637["justify"] = "center"
        GLabel_637["text"] = "Server"
        GLabel_637.place(x=300,y=20,width=420,height=40)

        # Label - IP PLC
        GLabel_584=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=10)
        GLabel_584["font"] = ft
        GLabel_584["fg"] = "#333333"
        GLabel_584["justify"] = "center"
        GLabel_584["text"] = "IP"
        GLabel_584.place(x=50,y=105,width=70,height=25)

        # Label - PLC Rack
        GLabel_769=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=10)
        GLabel_769["font"] = ft
        GLabel_769["fg"] = "#333333"
        GLabel_769["justify"] = "center"
        GLabel_769["text"] = "Rack"
        GLabel_769.place(x=50,y=170,width=70,height=25)

        # Label - PLC Slot
        GLabel_187=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=10)
        GLabel_187["font"] = ft
        GLabel_187["fg"] = "#333333"
        GLabel_187["justify"] = "center"
        GLabel_187["text"] = "Slot"
        GLabel_187.place(x=50,y=230,width=70,height=25)

        # Label - IP Server
        GLabel_528=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=10)
        GLabel_528["font"] = ft
        GLabel_528["fg"] = "#333333"
        GLabel_528["justify"] = "center"
        GLabel_528["text"] = "IP"
        GLabel_528.place(x=170,y=105,width=70,height=25)

        # Label - Port Server
        GLabel_811=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=10)
        GLabel_811["font"] = ft
        GLabel_811["fg"] = "#333333"
        GLabel_811["justify"] = "center"
        GLabel_811["text"] = "Port"
        GLabel_811.place(x=170,y=170,width=70,height=25)

        # Label - PLC
        GLabel_267=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=10)
        GLabel_267["font"] = ft
        GLabel_267["fg"] = "#333333"
        GLabel_267["justify"] = "center"
        GLabel_267["text"] = "PLC"
        GLabel_267.place(x=50,y=80,width=70,height=25)
        GLabel_267["bd"] = 1  # Adjust the border width as needed
        GLabel_267["relief"] = tk.SOLID  # Solid border

        # Label - Server
        GLabel_414=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=10)
        GLabel_414["font"] = ft
        GLabel_414["fg"] = "#333333"
        GLabel_414["justify"] = "center"
        GLabel_414["text"] = "Server"
        GLabel_414.place(x=170,y=80,width=70,height=25)
        GLabel_414["bd"] = 1  # Adjust the border width as needed
        GLabel_414["relief"] = tk.SOLID  # Solid border     

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


        # Label under the green button - "Foring PÅ"
        label_green_button = tk.Label(root)
        ft = tkFont.Font(family='Arial', size=10)
        label_green_button["bd"] = 1  # Adjust the border width as needed
        label_green_button["relief"] = tk.SOLID  # Solid border 
        label_green_button["font"] = ft
        label_green_button["fg"] = "#333333"
        label_green_button["justify"] = "center"
        label_green_button["text"] = "Foring PÅ"
        label_green_button.place(x=49, y=560, width=70, height=25)

        # Label under the yellow button - "Foring AV"
        label_yellow_button = tk.Label(root)
        ft = tkFont.Font(family='Arial', size=10)
        label_yellow_button["bd"] = 1  # Adjust the border width as needed
        label_yellow_button["relief"] = tk.SOLID  # Solid border 
        label_yellow_button["font"] = ft
        label_yellow_button["fg"] = "#333333"
        label_yellow_button["justify"] = "center"
        label_yellow_button["text"] = "Foring AV"
        label_yellow_button.place(x=120, y=560, width=70, height=25)

        # Label under the red button - "Nødstopp"
        label_red_button = tk.Label(root)
        ft = tkFont.Font(family='Arial', size=10)
        label_red_button["bd"] = 1  # Adjust the border width as needed
        label_red_button["relief"] = tk.SOLID  # Solid border 
        label_red_button["font"] = ft
        label_red_button["fg"] = "#333333"
        label_red_button["justify"] = "center"
        label_red_button["text"] = "Nødstopp"
        label_red_button.place(x=191, y=560, width=70, height=25)

        # ENTRIES

        # Entry - IP PLC
        GLineEdit_305=tk.Entry(root)
        GLineEdit_305["borderwidth"] = "1px"
        ft = tkFont.Font(family='Arial',size=10)
        GLineEdit_305["font"] = ft
        GLineEdit_305["fg"] = "#333333"
        GLineEdit_305["justify"] = "center"
        GLineEdit_305["text"] = ""
        GLineEdit_305.place(x=30,y=130,width=112,height=30)
        GLineEdit_305.insert(0,plcIP)
        def update_plcIP(event):
            global plcIP
            plcIP = GLineEdit_305.get()
        GLineEdit_305.bind("<KeyRelease>", update_plcIP)

        # Entry - Rack
        GLineEdit_166=tk.Entry(root)
        GLineEdit_166["borderwidth"] = "1px"
        ft = tkFont.Font(family='Arial',size=10)
        GLineEdit_166["font"] = ft
        GLineEdit_166["fg"] = "#333333"
        GLineEdit_166["justify"] = "center"
        GLineEdit_166["text"] = ""
        GLineEdit_166.place(x=30,y=190,width=112,height=30)
        GLineEdit_166.insert(0,rack)
        def update_rack(event):
            global rack
            rack = GLineEdit_166.get()
        GLineEdit_166.bind("<KeyRelease>", update_rack)

        # Entry - Slot
        GLineEdit_886=tk.Entry(root)
        GLineEdit_886["borderwidth"] = "1px"
        ft = tkFont.Font(family='Arial',size=10)
        GLineEdit_886["font"] = ft
        GLineEdit_886["fg"] = "#333333"
        GLineEdit_886["justify"] = "center"
        GLineEdit_886["text"] = ""
        GLineEdit_886.place(x=30,y=250,width=112,height=30)
        GLineEdit_886.insert(0,slot)
        def update_slot(event):
            global slot
            slot = GLineEdit_886.get()
        GLineEdit_886.bind("<KeyRelease>", update_slot)

        # Entry - Server IP
        GLineEdit_57=tk.Entry(root)
        GLineEdit_57["borderwidth"] = "1px"
        ft = tkFont.Font(family='Arial',size=10)
        GLineEdit_57["font"] = ft
        GLineEdit_57["fg"] = "#333333"
        GLineEdit_57["justify"] = "center"
        GLineEdit_57["text"] = ""
        GLineEdit_57.place(x=150,y=130,width=113,height=30)
        GLineEdit_57.insert(0,serverIP)
        def update_serverIP(event):
            global serverIP
            serverIP = GLineEdit_57.get()
        GLineEdit_57.bind("<KeyRelease>", update_serverIP)

        # Entry - Server Port
        GLineEdit_512=tk.Entry(root)
        GLineEdit_512["borderwidth"] = "1px"
        ft = tkFont.Font(family='Arial',size=10)
        GLineEdit_512["font"] = ft
        GLineEdit_512["fg"] = "#333333"
        GLineEdit_512["justify"] = "center"
        GLineEdit_512["text"] = ""
        GLineEdit_512.place(x=150,y=190,width=111,height=30)
        GLineEdit_512.insert(0,port)
        def update_port(event):
            global port
            port = GLineEdit_512.get()
        GLineEdit_512.bind("<KeyRelease>", update_port)

        # INDICATOR LIGHTS

        self.canvas = tk.Canvas(root, width=200, height=60)
        self.canvas.place(x=50, y=480)

        # Green light
        self.green_light = self.canvas.create_oval(10, 10, 60, 60, fill="gray")

        # Yellow light
        self.yellow_light = self.canvas.create_oval(80, 10, 130, 60, fill="gray")

        # Red light
        self.red_light = self.canvas.create_oval(150, 10, 200, 60, fill="gray")

        # BUTTONS

        # Button - Start server
        GButton_984=tk.Button(root)
        GButton_984["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Arial',size=10)
        GButton_984["font"] = ft
        GButton_984["fg"] = "#000000"
        GButton_984["justify"] = "center"
        GButton_984["text"] = "Start server"
        GButton_984.place(x=830,y=560,width=75,height=25)
        GButton_984["command"] = self.GButton_984_command

        # Button - Exit server
        btnAvslutt=tk.Button(root)
        btnAvslutt["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Arial',size=10)
        btnAvslutt["font"] = ft
        btnAvslutt["fg"] = "#000000"
        btnAvslutt["justify"] = "center"
        btnAvslutt["text"] = "Avslutt server"
        btnAvslutt.place(x=907,y=560,width=85,height=25)
        btnAvslutt["command"] = self.btnAvslutt

    # FUNCTION LIGHT-CHANGING
    def update_lights(self):
        if EMGStatus == 0:
            self.canvas.itemconfig(self.red_light_light, fill="gray") 
        else:
            self.canvas.itemconfig(self.red_light, fill="red") 
        if feedingstatus == 1:
            self.canvas.itemconfig(self.green_light_light, fill="green") 
            self.canvas.itemconfig(self.yellow_light, fill="grey") 
        else:
            self.canvas.itemconfig(self.green_light_light, fill="grey") 
            self.canvas.itemconfig(self.yellow_light, fill="yellow") 



    # FUNCTION START SERVER
    def GButton_984_command(self):

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
        while True:
            self.update_lights()

        
        
    # FUNCTION EXIT APPLICATION
    def btnAvslutt(self):
         sys.exit()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()