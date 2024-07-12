import snap7
import time
import sys
import socket
import tkinter as tk
import tkinter.font as tkFont
import threading

# Dette programmet kommuniserer med både Client.py inne i dockeren, samtidig som den sender boolsk verdi ut til PLS.
# ----------------------------------------------------------------------------------------------------------------------------- #
### --- FIELDS --- ###

# PLC
plcIP = '192.168.0.1'
rack = 0
slot = 1

# Server
serverIP = "192.168.0.3"
plc = snap7.client.Client()
port = 5151 # PORT NVIDIA jetson
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Adress from TIA Portal - dbCommunication
db_number = 2
start_offset = 0
# Static Bool - P1 occupied
sbP1_detected_bit_offset = 2
# Static Bool - P2 occupied
sbP2_detected_bit_offset = 3
# Static Bool - Illigal parking alarm
sbIlligalParking_bit_offset = 4
# Static Bool - Emergency Stop
#sbEMGStop_bit_offset = 1

outputOn = 1
outputOff = 0

detectedBoats = 0
feedingstatus = 0
EMGStatus = 0
P1_telles = False
P2_telles = False
#P3_telles = False

# ----------------------------------------------------------------------------------------------------------------------------- #

### --- FUNCTIONS --- ###

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

# Funksjon for å håndtere klient etter tilkobling
def handle_client(conn, addr):
    #global detectedBoats, P1_telles, P2_telles, lbBoatsDetected
    print(f"NVIDIA Object detecion software running   {addr}")
    connected = True
    while connected:
        msg_length=conn.recv(64).decode('utf-8')
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode('utf-8')
            print(f"{msg}")
             
                
            if msg == "P1_true":
                WriteBool(db_number, start_offset,sbP1_detected_bit_offset, outputOn)
                #if (P1_telles):
                 #   continue
                #else:
                 #   detectedBoats += 1
                  #  P1_telles = True
                   # lbBoatsDetected.delete(0,tk.END)
                    #lbBoatsDetected.insert(0, detectedBoats)
            if msg == "P1_false":
                WriteBool(db_number, start_offset,sbP1_detected_bit_offset, outputOff)
                #if (P1_telles):
                    #detectedBoats -= 1
                    #P1_telles = False
                    #update_gui()
                #else:
                    #continue
            if msg == "P2_true":
                WriteBool(db_number, start_offset,sbP2_detected_bit_offset, outputOn)
                #if (P2_telles):
                    #continue
                #else:
                    #detectedBoats += 1
                    #P2_telles = True
                    #update_gui()
            if msg == "P2_false":
                WriteBool(db_number, start_offset,sbP2_detected_bit_offset, outputOff)
                #if (P2_telles):
                 #   detectedBoats -= 1
                  #  P2_telles = False
                   # update_gui()
                #else:
                 #   continue
            if msg == "DIP_true":
                WriteBool(db_number, start_offset,sbIlligalParking_bit_offset, outputOn)
            if msg == "DIP_false":
                WriteBool(db_number, start_offset,sbIlligalParking_bit_offset, outputOff)
	
# Funksjon for å starte opp server og koble til PLS og klient
def start_client():
    print(f"[Listening] server is listening on {serverIP}")
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


### --- GUI KODE --- ###

class App:
    def __init__(self, root):
        global lbBoatsDetected

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

        ### --- LABELS --- ###

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

        # Label - Boats detected
        labelBoatsDetected=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=10)
        labelBoatsDetected["font"] = ft
        labelBoatsDetected["fg"] = "#333333"
        labelBoatsDetected["justify"] = "center"
        labelBoatsDetected["text"] = "Boats detected"
        labelBoatsDetected.place(x=37,y=320,width=100,height=25)
        labelBoatsDetected["bd"] = 1  # Adjust the border width as needed
        labelBoatsDetected["relief"] = tk.SOLID  # Solid border 

        # Label - Boats detected input
        lbBoatsDetected=tk.Listbox(root)
        ft = tkFont.Font(family='Arial',size=10)
        lbBoatsDetected["font"] = ft
        lbBoatsDetected["fg"] = "#333333"
        lbBoatsDetected["justify"] = "center"
        lbBoatsDetected.place(x=37,y=350,width=100,height=25)
        lbBoatsDetected["bd"] = 1  # Adjust the border width as needed
        lbBoatsDetected["relief"] = tk.SOLID  # Solid border 
        lbBoatsDetected.insert(0, detectedBoats)

        ### --- ENTRIES --- ###

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

        ### --- BUTTONS --- ###

        # Button - Start server
        btnStartServer=tk.Button(root)
        btnStartServer["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Arial',size=10)
        btnStartServer["font"] = ft
        btnStartServer["fg"] = "#000000"
        btnStartServer["justify"] = "left"
        btnStartServer["text"] = "Start server"
        btnStartServer.place(relx=0.95, rely=0.75, anchor=tk.SE)
        btnStartServer["command"] = self.btnStartServer

	# Button - Open surveillance
        btnOpen=tk.Button(root)
        btnOpen["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Arial',size=10)
        btnOpen["font"] = ft
        btnOpen["fg"] = "#000000"
        btnOpen["justify"] = "left"
        btnOpen["text"] = "Surveillance"
        btnOpen.place(relx=0.95, rely=0.85, anchor=tk.SE)
        btnOpen["command"] = self.btnOpen    

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

    # FUNCTION OPEN SURVEILLANCE APPLICATION
    def btnOpen(self):
        bredde = 0

        # Function to draw a rounded rectangle
        def draw_rounded_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
            points = [
                x1 + radius, y1,
                x2 - radius, y1,
                x2, y1,
                x2, y1 + radius,
                x2, y2 - radius,
                x2, y2,
                x2 - radius, y2,
                x1 + radius, y2,
                x1, y2,
                x1, y2 - radius,
                x1, y1 + radius,
                x1, y1,
                x1 + radius, y1
            ]
            canvas.create_polygon(points, smooth=True, **kwargs)

        # Create the main window
        root = tk.Tk()
        root.title("Boatdeteksjon")


        # Create a canvas with full HD size (1920x1080)
        canvas = tk.Canvas(root, width=1920, height=1080, bg='light grey')
        canvas.pack()


        draw_rounded_rectangle(canvas, 619, 50, 1300, 155, 20, fill='gray12', outline='gray22', width=2) # Title box

        label = tk.Label(root, text="Haugesund Gjestebrygge", bg='gray12', fg='azure', font=("Calibri", 46))
        canvas.create_window(643, 60, anchor='nw', window=label)

        # Draw a rounded rectangle for 'hav'
        draw_rounded_rectangle(canvas, 99, 200, 1819, 980, 20, fill='#9ACBFF', outline='gray22', width=25)



        # Utstikkere
        draw_rounded_rectangle(canvas, 205, 595, 220, 750, 10, fill='gray46', outline='gray12', width=0)
        draw_rounded_rectangle(canvas, 475, 595, 490, 750, 10, fill='gray46', outline='gray12', width=0)
        draw_rounded_rectangle(canvas, 745, 595, 760, 750, 10, fill='gray46', outline='gray12', width=0)
        draw_rounded_rectangle(canvas, 1015, 595, 1030, 750, 10, fill='gray46', outline='gray12', width=0)
        draw_rounded_rectangle(canvas, 1285,595, 1300, 750, 10, fill='gray46', outline='gray12', width=0)

        # Draw a rounded rectangle for 'brygge'
        draw_rounded_rectangle(canvas, 200, 500, 1655, 600, 15, fill='gray76', outline='gray22', width=2)
        draw_rounded_rectangle(canvas, 1555, 500, 1655, 968, 15, fill='gray76', outline='gray22', width=2)
        draw_rounded_rectangle(canvas, 1554, 501, 1560, 599, 0, fill='gray76', outline='gray76', width=0)

        # Rektangler for øvre store p-plasser
        draw_rounded_rectangle(canvas, 330, 330, 830, 480, 60, fill='#D4EAFF', outline='#D4EAFF', width=3)
        draw_rounded_rectangle(canvas, 1000, 330, 1500, 480, 60, fill='#D4EAFF', outline='#D4EAFF', width=3)

        # Nedre P-plasser
        draw_rounded_rectangle(canvas, 230, 610, 335, 830, 65, fill='#D4EAFF', outline='#D4EAFF', width=bredde)
        draw_rounded_rectangle(canvas, 360, 610, 465, 830, 65, fill='#2EC729', outline='#2EC729', width=bredde)
        draw_rounded_rectangle(canvas, 500, 610, 605, 830, 65, fill='#D4EAFF', outline='#D4EAFF', width=bredde)
        draw_rounded_rectangle(canvas, 630, 610, 735, 830, 65, fill='#D4EAFF', outline='#D4EAFF', width=bredde)
        draw_rounded_rectangle(canvas, 770, 610, 875, 830, 65, fill='#D4EAFF', outline='#D4EAFF', width=bredde)
        draw_rounded_rectangle(canvas, 900, 610, 1005, 830, 65, fill='#D4EAFF', outline='#D4EAFF', width=bredde)
        draw_rounded_rectangle(canvas, 1040, 610, 1145, 830, 65, fill='#D4EAFF', outline='#D4EAFF', width=bredde)
        draw_rounded_rectangle(canvas, 1170, 610, 1275, 830, 65, fill='#D4EAFF', outline='#D4EAFF', width=bredde)
        draw_rounded_rectangle(canvas, 1310, 610, 1415, 830, 65, fill='#D4EAFF', outline='#D4EAFF', width=bredde)
        draw_rounded_rectangle(canvas, 1440, 610, 1545, 830, 65, fill='#D4EAFF', outline='#D4EAFF', width=bredde)

        # Create and place the buttons
        button1 = tk.Button(canvas, text="", bg='#D4EAFF', activebackground='#D0E5FA', bd=0, command=lambda: function("input"))
        button1_window = canvas.create_window(340, 340, anchor='nw', window=button1, width=480, height=130)
        button2 = tk.Button(canvas, text="", bg='#D4EAFF', activebackground='#D0E5FA', bd=0, command=lambda: function("input"))
        button2_window = canvas.create_window(1010, 340, anchor='nw', window=button2, width=480, height=130)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
