import os
import socket
import time
import datetime
import csv
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput
os.environ['GST_DEBUG'] = '*:3' # Supresses GStreamer
# Dette programmet kjører bildedeteksjonsmodellen og behandler denne dataen. Sender så ut en boolsk verdi til ServerGUI.py.
# ----------------------------------------------------------------------------------------------------------------------------- #Kan vi fjerne dette? : [gstreamer] gstreamer mysink taglist, video-codec=(string)"H.264\ \(Main\ Profile\)", bitrate=(uint)10014214, minimum-bitrate=(uint)6275040, maximum-bitrate=(uint)16813440;

"""
# PLS
### --- FIELDS --- ###

# Definerer variabler og setter opp socket kommunikasjon
HEADER = 64
port =5151
FORMAT = 'utf-8'
SERVER =  '192.168.0.3'
ADDR = (SERVER,port)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# ----------------------------------------------------------------------------------------------------------------------------- #
### --- FUNCTIONS --- ###

def send(msg): #funksjon som sender melding via socket kommunikasjon
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length =str(msg_length).encode(FORMAT)
    send_length += b' '*(HEADER-len(send_length))
    client.send(send_length)
    client.send(message)
"""


def log_parking_status(detections): # Logg
    global parking_spots, boat_count, P1_slettes_etter_5_min, P1_starttimer, P2_slettes_etter_5_min, P2_starttimer, P3_slettes_etter_5_min, P3_starttimer, P1_sistlogg, P2_sistlogg, P3_sistlogg, state_P1, state_P2, state_P3, state_DIP


    current_time = datetime.datetime.now()
    for detection in detections:
        class_name = net.GetClassDesc(detection.ClassID)
        

        if class_name.lower() == "boat": #Gjør det IKKE dersom den detekterer "person" eller "motorcycle"
            #Deteksjonsinfo oppdateres hver deteksjon
            boat_bottom = detection.Bottom
            boat_area = detection.Area
            boat_left = detection.Left

            # Logg ###  P1  ###
            if (abs(boat_bottom - P1["Bottom"]) <= ytolerance and abs(boat_left - P1["Left"]) <= xtolerance):
                P1_loggpause = current_time - P1_sistlogg
                totimertimer = current_time - P1_starttimer
                P1_slettes_etter_5_min = datetime.datetime.now() # Oppdaterer at P1 er aktiv
                if P1["Ledig"]: #Hvis P1 er ledig (true)
                    P1_starttimer = current_time # Gjøres kun første gang
                    P1["Ledig"] = False 
                    state_P1 = "P1_true"
                    print("P1 ble nå opptatt")
                    boat_count += 1 # En ny båt i parkeringssystemet
                    with open('boat_data.csv', mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([f"{current_time}", "P1 ANKOMST"]) 
                elif (P1_loggpause.total_seconds() < 5): # Skal ikke Write til csv hvis mindre enn 5 sekund siden sist
                    break
                elif (totimertimer.total_seconds() < totimer):
                    print("Oppdaterer P1 aktiv")
                else:
                    print("P-plass 1 har vært opptatt i 2 timer.") # Kan legge til noe mer alarm.
                    state_DIP = "DIP_true"
                        
                # Uansett om den er ny eller ikke, så lagrer vi dataen og skriver til excel (loggen).
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                P1_sistlogg = datetime.datetime.now()
                position = "Parkering nr.1"
                lengthpixel = detection.Width
                length = lengthpixel/52 # gir ca. verdi på P1, ved Full HD
                P1["Bredde"] = length
                boat_data = {"timestamp": timestamp, "position": position, "length": length}
                write_to_csv(boat_data)
            
            # Logg ###  P2  ###
            elif (abs(boat_bottom - P2["Bottom"]) <= ytolerance and abs(boat_left - P2["Left"]) <= xtolerance and abs(boat_area-P2["Area"]<areatolerance)):
                P2_loggpause = current_time - P2_sistlogg
                totimertimer = current_time - P2_starttimer
                P2_slettes_etter_5_min = current_time # Oppdaterer at P2 er aktiv
                if P2["Ledig"]: # Hvis P2 er ledig (true)
                    P2_starttimer = current_time
                    P2["Ledig"] = False
                    state_P2 = 'P2_true'
                    print("P2 ble nå opptatt")
                    boat_count += 1
                    with open('boat_data.csv', mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([f"{current_time}", "P2 ANKOMST"]) 
                elif (P2_loggpause.total_seconds() < 5): # Skal ikke Write til csv dersom mindre enn 5 sekund siden sist
                    break
                elif (totimertimer.total_seconds() < totimer):
                    print("Oppdaterer P2 aktiv")
                else:
                    print("P-plass 2 har vært opptatt i 2 timer.") # Kan legge til noe mer alarm.
                    state_DIP = "DIP_true"

                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                P2_sistlogg = datetime.datetime.now()
                position = "Parkering nr.2"
                lengthpixel = detection.Width
                length = lengthpixel/65
                P2["Bredde"] = length
                boat_data = {"timestamp": timestamp, "position": position, "length": length}
                write_to_csv(boat_data)
            
             # Logg ###  P3  ###
            elif (abs(boat_bottom - P3["Bottom"]) <= ytolerance and abs(boat_left - P3["Left"]) <= xtolerance):
                P3_loggpause = current_time - P3_sistlogg
                totimertimer = current_time - P3_starttimer
                P3_slettes_etter_5_min = datetime.datetime.now() # Oppdaterer at P3 er aktiv
                if P3["Ledig"]: #Hvis P3 er ledig (true)
                    P3_starttimer = current_time #Gjøres kun første gang
                    P3["Ledig"] = False 
                    print("P3 ble nå opptatt")
                    boat_count += 1
                    with open('boat_data.csv', mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([f"{current_time}", "P3 ANKOMST"]) 
                elif (P3_loggpause.total_seconds() < 5): # Skal ikke Write til csv hvis mindre enn 5 sekund siden sist
                    break
                elif (totimertimer.total_seconds() < totimer):
                    print("Oppdaterer P3 aktiv")
                else:
                    print("P-plass 3 har vært opptatt i 2 timer.") # Kan legge til noe mer alarm.
                
                # Uansett om den er ny eller ikke, så lagrer vi dataen og skriver til excel.
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                P3_sistlogg = datetime.datetime.now()
                position = "Parkering nr.3"
                lengthpixel = detection.Width
                length = lengthpixel/43
                P3["Bredde"] = length
                boat_data = {"timestamp": timestamp, "position": position, "length": length}
                write_to_csv(boat_data)

            else: #Utenfor parkering, da trenger vi ikke å bry oss.
                pass


# Funksjon for å skrive data til CSV-fil
def write_to_csv(data):
    with open('boat_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([data["timestamp"], data["position"], data["length"], boat_count])

#Denne funksjonen sletter parkeringer som har vært inaktive, og lagrer rapporten over hvor lenge den stod.
def rapporttid():
    global parking_spots, boat_count, P1_slettes_etter_5_min, P1_starttimer, P2_slettes_etter_5_min, P2_starttimer, current_time, state_P1, state_P2, state_P3, state_DIP  #Tror global i functions er nødvendig
    
    current_time = datetime.datetime.now()
    P1_timedifference = current_time - P1_slettes_etter_5_min
    P1_totaltid = current_time - P1_starttimer
    
    # RAPPORT ###  P1  ###
    if ((P1_timedifference.total_seconds() >= timefordelete) and not P1["Ledig"]):
        P1["Ledig"] = True
        boat_count-= 1
        alarm = False
        P1_bredde = P1["Bredde"]
        state_P1 = 'P1_false'
        state_DIP = "DIP_false"
        
        
        if P1_totaltid.total_seconds() > 7200:
            tid_format = f"{(P1_totaltid.total_seconds()-timefordelete)/3600:.2f} timer"
            alarm = True
        elif P1_totaltid.total_seconds() > 60:
            tid_format = f"{(P1_totaltid.total_seconds()-timefordelete)/60:.2f} minutter"
        else:
            tid_format = f"{(P1_totaltid.total_seconds()-timefordelete):.2f} sekunder"
        # Bredde og pris
        if (P1["Bredde"] > 9.5):
            pris = 300
        else:
            pris = 250 
        with open('boat_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([f"{current_time}", "P1 AVREISE"])
        if (P1_totaltid.total_seconds()-timefordelete > 5): # Ikke Rapporter hvis stått under et visst antall sekunder.
            print(f"Parkering 1 var opptatt fra {P1_starttimer.strftime('%Y-%m-%d %H:%M:%S')} UTC og stod der i {tid_format}")
            with open('rapport.csv', mode='a', newline='') as file:
                writer = csv.writer(file, delimiter = ',')
            if alarm:
                writer.writerow([f"Parkering 1 ble opptatt {P1_starttimer.strftime('%Y-%m-%d %H:%M:%S')}UTC og stod der i {tid_format}", f"Båten er {P1_bredde} meter lang.", f"AVGIFTSBELAGT", f"vedkommende skal betale:", f"{pris}", f"kr"])
            else:
                writer.writerow([f"Parkering 1 ble opptatt {P1_starttimer.strftime('%Y-%m-%d %H:%M:%S')}UTC og stod der i {tid_format}", f"Båten er {P1_bredde} meter lang",])

    # RAPPORT ###  P2  ###
    P2_timedifference = current_time - P2_slettes_etter_5_min
    P2_totaltid = current_time - P2_starttimer
    if ((P2_timedifference.total_seconds() >= timefordelete) and not P2["Ledig"]):
        P2["Ledig"] = True
        boat_count-= 1
        alarm = False
        P2_bredde = P2["Bredde"]
        state_P2 = 'P2_false'
        
        # Tidsformat
        if P2_totaltid.total_seconds() > 7200:
            tid_format = f"{(P2_totaltid.total_seconds()-timefordelete)/3600:.2f} timer"
            alarm = True
        elif P2_totaltid.total_seconds() > 60:
            tid_format = f"{(P2_totaltid.total_seconds()-timefordelete)/60:.2f} minutter"
        else:
            tid_format = f"{(P2_totaltid.total_seconds()-timefordelete):.2f} sekunder"

	
        # Bredde og pris
        if (P2["Bredde"] > 9.5):
            pris = 300
        else:
            pris = 250 
        with open('boat_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([f"{current_time}", "P2 AVREISE"])
        if (P2_totaltid.total_seconds()-timefordelete > 5): # Ikke Rapporter hvis stått under et visst antall sekunder.
            print(f"Parkering 2 var opptatt fra {P2_starttimer.strftime('%Y-%m-%d %H:%M:%S')} UTC og stod der i {tid_format}")
            with open('rapport.csv', mode='a', newline='') as file:
                writer = csv.writer(file, delimiter = ',')
                if alarm:
                    writer.writerow([f"Parkering 2 ble opptatt {P2_starttimer.strftime('%Y-%m-%d %H:%M:%S')}UTC og stod der i {tid_format}", f"Båten er {P2_bredde} meter lang.", f"AVGIFTSBELAGT", f"vedkommende skal betale:", f"{pris}", f"kr"])
                else:
                    writer.writerow([f"Parkering 2 ble opptatt {P2_starttimer.strftime('%Y-%m-%d %H:%M:%S')}UTC og stod der i {tid_format}", f"Båten er {P2_bredde} meter lang"])

    # Rapport ###  P3  ###
    P3_timedifference = current_time - P3_slettes_etter_5_min
    P3_totaltid = current_time - P3_starttimer
    if ((P3_timedifference.total_seconds() >= timefordelete) and not P3["Ledig"]):
        P3["Ledig"] = True
        boat_count-= 1
        alarm = False
        P3_bredde = P3["Bredde"]
        
        # Tidsformat
        if P3_totaltid.total_seconds() > 7200:
            tid_format = f"{(P3_totaltid.total_seconds()-timefordelete)/3600:.2f} timer"
            alarm = True
        elif P3_totaltid.total_seconds() > 60:
            tid_format = f"{(P3_totaltid.total_seconds()-timefordelete)/60:.2f} minutter"
        else:
            tid_format = f"{(P3_totaltid.total_seconds()-timefordelete):.2f} sekunder"

	
        # Bredde og pris
        if (P3["Bredde"] > 9.5):
            pris = 300
        else:
            pris = 250 
        with open('boat_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([f"{current_time}", "P3 AVREISE"])
        if (P3_totaltid.total_seconds()-timefordelete > 5): # Ikke Rapporter hvis stått under et visst antall sekunder.
            print(f"Parkering 3 var opptatt fra {P3_starttimer.strftime('%Y-%m-%d %H:%M:%S')} UTC og stod der i {tid_format}")
            with open('rapport.csv', mode='a', newline='') as file:
                writer = csv.writer(file, delimiter = ',')
            if alarm:
                writer.writerow([f"Parkering 3 ble opptatt {P3_starttimer.strftime('%Y-%m-%d %H:%M:%S')}UTC og stod der i {tid_format}", f"Båten er {P3_bredde} meter lang.", f"AVGIFTSBELAGT", f"vedkommende skal betale:", f"{pris}", f"kr"])
            else:
                writer.writerow([f"Parkering 3 ble opptatt {P3_starttimer.strftime('%Y-%m-%d %H:%M:%S')}UTC og stod der i {tid_format}", f"Båten er {P3_bredde} meter lang",])

# ----------------------------------------------------------------------------------------------------------------------------- #
### --- KODE --- ###

# Oppretter CSV-fil og skriver headeren hvis den ikke allerede finnes
try:
    with open('boat_data.csv', mode='x', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Tidspunkt", "Parkeringsplass", "Bredde", "Antall båter nå"])
except FileExistsError:
    # Filen eksisterer allerede, Du kan vurdere å ha ingenting gjøres
    with open('boat_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Tidspunkt", "Parkeringsplass", "Bredde", "Antall båter nå"])

try:
    with open('rapport.csv', mode='x', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Rapport over båter som har forlatt kaien.\n"])
except FileExistsError:
    # Filen eksisterer allerede, Du kan vurdere å ha ingenting gjøres
    pass

   
        
        
	## VARIABLER ##
boat_count = 0
# Definisjon av parkeringsplasser (MÅ VITE PIKSLENES KOORDINATER)
parking_spots = [
    {"Id": (1), "Left": (45), "Right": (1080), "Bottom": (604), "Top": None, "Area": (296000), "Ledig": (True), "Bredde": 0, },
    {"Id": (2), "Left": (1150), "Right": (1445), "Bottom": (772), "Top": None, "Area": (100000), "Ledig": (True), "Bredde": 0, },
    {"Id": (3), "Left": (1305), "Right": (1870), "Bottom": (623), "Top": None, "Area": (170000), "Ledig": (True), "Bredde": 0, },
    # Legg til flere parkeringsplasser etter behov
]

redningsleider_piksler = [(1240, 129)] # Vi har bare en som et eksempel.
redningsleider_tidtaker = None  # Timer for blocking detection (skal ikke gi alarm med en gang)

# Verdiene kan hentes slik: P1["Left"]
P1, P2, P3 = parking_spots[0], parking_spots[1], parking_spots[2]
# Timere er enklere å jobbe med som egne variabler.
P1_starttimer = P2_starttimer = P3_starttimer = P1_slettes_etter_5_min = P2_slettes_etter_5_min = P3_slettes_etter_5_min = P1_sistlogg = P2_sistlogg = P3_sistlogg = datetime.datetime.now() 
xtolerance = 70  # Disse toleranseverdiene kan legges i parking_spots og ha unike toleranser for hver P-plass dersom ønskelig
ytolerance = 60
areatolerance = 5000
timefordelete = 10 # 5 min er 300.
totimer = 50 # skal være 7200 (2 timer)
state_P1 = "P1_false" # PLS
state_P2 = "P2_false"
state_DIP = "DIP_false"


print('********************* VELG BILDEDETEKSJONSMODELL *********************')
print('           SKRIV INN s FOR STANDARDMODELL OG e FOR EGEN MODELL')



a = input()

if a == 's':
    net = detectNet("ssd-mobilenet-v2", threshold=0.5)
    source = "Main.mp4" 
    camera = videoSource(source) 
    display = videoOutput()  # 'my_video.mp4' for file, or sequence of images 'img_%i.jpg'
    
    while display.IsStreaming():
        current_time = datetime.datetime.now()
        img = camera.Capture()
        if img is None:
            continue

        detections = net.Detect(img)
        log_parking_status(detections)

        """
        # Print detection information.
        for detection in detections:
      	    print(f"ClassID: {detection.ClassID}, Confidence: {detection.Confidence}, BBox:{detection.Bottom} {detection.Area} {detection.Left}")
	    """
	
        display.Render(img)
        display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
        
        current_time = datetime.datetime.now()
        # Må sette P1 til True etter 5 min inaktiv. slik at vi skriver ut rapport og nye kan komme.
        
        rapporttid()


elif a == 'e':
    net = detectNet(argv=['--model=models/boat/ssd-mobilenet.onnx', '--labels=models/boat/labels.txt', '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes', '--threshold=0.5'])
    source = "Main.mp4" 
    camera = videoSource(source) 
    display = videoOutput()  # 'my_video.mp4' for file, or sequence of images 'img_%i.jpg'

    
    while display.IsStreaming():
        img = camera.Capture()
        if img is None:
            continue

        detections = net.Detect(img)
        
        log_parking_status(detections)     

        rapporttid()

        # Print detection information
        #for detection in detections:
            #print(f"TrackID: {detection.TrackID}")
        #send(state_P1)
        #send(state_P2)
        #send(state_DIP)

        display.Render(img)
        display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
        
else:
    print("Ugyldig valg. Vennligst velg 's' for standardmodell eller 'e' for egen modell.")
