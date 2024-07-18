import os
import socket
import time
import datetime
import csv
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput

# Dette programmet kjører bildedeteksjonsmodellen og behandler denne dataen. Sender så ut en boolsk verdi til ServerGUI.py.
# ----------------------------------------------------------------------------------------------------------------------------- #Kan vi fjerne dette? : [gstreamer] gstreamer mysink taglist, video-codec=(string)"H.264\ \(Main\ Profile\)", bitrate=(uint)10014214, minimum-bitrate=(uint)6275040, maximum-bitrate=(uint)16813440;


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

ukenummer = datetime.datetime.now().isocalendar()[1]
# ----------------------------------------------------------------------------------------------------------------------------- #
### --- FUNCTIONS --- ###

def send(msg): #funksjon som sender melding via socket kommunikasjon
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length =str(msg_length).encode(FORMAT)
    send_length += b' '*(HEADER-len(send_length))
    client.send(send_length)
    client.send(message)



def log_parking_status(detections): # Logg
    global parking_spots, boat_count, P1_slettes_etter_5_min, P1_starttimer, P9_slettes_etter_5_min, P9_starttimer, P1_sistlogg, P9_sistlogg, state_P1, state_P9, state_DIP, ukenummer


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
                    send(state_P1)
                    print("P1 ble nå opptatt")
                    boat_count += 1 # En ny båt i parkeringssystemet
                    with open(f'boat_data_uke{ukenummer}.csv', mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([f"{current_time.strftime('%Y-%m-%d %H:%M:%S')}", "P1 ANKOMST"]) 
                elif (P1_loggpause.total_seconds() < 5): # Skal ikke Write til csv hvis mindre enn 5 sekund siden sist
                    break
                elif (totimertimer.total_seconds() < totimer):
                    print("Oppdaterer P1 aktiv")
                    state_P1 = "P1_true"
                    send(state_P1)
                    
                else:
                    print("P-plass 1 har vært opptatt i 2 timer.") # Kan legge til noe mer alarm.
                    state_DIP = "DIP_true"
                    send(state_DIP)
                        
                # Uansett om den er ny eller ikke, så lagrer vi dataen og skriver til excel (loggen).
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                P1_sistlogg = datetime.datetime.now()
                position = "Parkering nr.1"
                lengthpixel = detection.Width
                length = lengthpixel/52 # gir ca. verdi på P1, ved Full HD
                P1["Lengde"] = length
                boat_data = {"timestamp": timestamp, "position": position, "length": length}
                write_to_csv(boat_data)
            
            # Logg ###  P9  ###
            elif (abs(boat_bottom - P9["Bottom"]) <= ytolerance and abs(boat_left - P9["Left"]) <= xtolerance and abs(boat_area-P9["Area"]<areatolerance)):
                P9_loggpause = current_time - P9_sistlogg
                totimertimer = current_time - P9_starttimer
                P9_slettes_etter_5_min = current_time # Oppdaterer at P9 er aktiv
                if P9["Ledig"]: # Hvis P9 er ledig (true)
                    P9_starttimer = current_time
                    P9["Ledig"] = False
                    state_P9 = 'P9_true'
                    send(state_P9)
                    print("P9 ble nå opptatt")
                    boat_count += 1
                    with open(f'boat_data_uke{ukenummer}.csv', mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([f"{current_time.strftime('%Y-%m-%d %H:%M:%S')}", "P9 ANKOMST"]) 
                elif (P9_loggpause.total_seconds() < 5): # Skal ikke Write til csv dersom mindre enn 5 sekund siden sist
                    break
                elif (totimertimer.total_seconds() < totimer):
                    print("Oppdaterer P9 aktiv")
                    send(state_P9)
                else:
                    print("P-plass 9 har vært opptatt i 2 timer.") # Kan legge til noe mer alarm.

                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                P9_sistlogg = datetime.datetime.now()
                position = "Parkering nr.9"
                lengthpixel = detection.Width
                length = (lengthpixel/65) # Tilpasses per P-plass
                P9["Lengde"] = length
                boat_data = {"timestamp": timestamp, "position": position, "length": length}
                write_to_csv(boat_data)
            
            else: #Utenfor parkering, da trenger vi ikke å bry oss.
                pass

# Funksjon for å skrive data til CSV-fil
def write_to_csv(data):
    global ukenummer
    with open(f'boat_data_uke{ukenummer}.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([data["timestamp"], data["position"], data["length"], boat_count])

#Denne funksjonen sletter parkeringer som har vært inaktive, og lagrer rapporten over hvor lenge den stod.
def rapporttid():
    global parking_spots, boat_count, P1_slettes_etter_5_min, P1_starttimer, P9_slettes_etter_5_min, P9_starttimer, current_time, state_P1, state_P9, state_DIP  #Tror global i functions er nødvendig
    
    current_time = datetime.datetime.now()
    P1_timedifference = current_time - P1_slettes_etter_5_min
    P1_totaltid = current_time - P1_starttimer
    
    # RAPPORT ###  P1  ###
    if ((P1_timedifference.total_seconds() >= timefordelete) and not P1["Ledig"]):
        P1["Ledig"] = True
        boat_count-= 1
        alarm = False
        P1_lengde = P1["Lengde"]
        state_P1 = 'P1_false'
        state_DIP = "DIP_false"
        send(state_DIP)
        
        
        if P1_totaltid.total_seconds() > 7200:
            tid_format = f"{(P1_totaltid.total_seconds()-timefordelete)/3600:.2f} timer"
            alarm = True
        elif P1_totaltid.total_seconds() > 60:
            tid_format = f"{(P1_totaltid.total_seconds()-timefordelete)/60:.2f} minutter"
        else:
            tid_format = f"{(P1_totaltid.total_seconds()-timefordelete):.2f} sekunder"
        # lengde og pris
        if (P1["Lengde"] > 9.5):
            pris = 300
        else:
            pris = 250 
        with open(f'boat_data_uke{ukenummer}.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([f"{current_time.strftime('%Y-%m-%d %H:%M:%S')}", "P1 AVREISE"])
        if (P1_totaltid.total_seconds()-timefordelete > 5): # Ikke Rapporter hvis stått under et visst antall sekunder.
            print(f"Parkering 1 var opptatt fra {P1_starttimer.strftime('%Y-%m-%d %H:%M:%S')} UTC og stod der i {tid_format}")
            with open('rapport.csv', mode='a', newline='') as file:
                writer = csv.writer(file, delimiter = ',')
            if alarm:
                writer.writerow([f"Parkering 1 ble opptatt {P1_starttimer.strftime('%Y-%m-%d %H:%M:%S')}UTC og stod der i {tid_format}", f"Båten er {P1_lengde} meter lang.", f"AVGIFTSBELAGT", f"vedkommende skal betale:", f"{pris}", f"kr"])
            else:
                writer.writerow([f"Parkering 1 ble opptatt {P1_starttimer.strftime('%Y-%m-%d %H:%M:%S')}UTC og stod der i {tid_format}", f"Båten er {P1_lengde} meter lang",])

    # RAPPORT ###  P9  ###
    P9_timedifference = current_time - P9_slettes_etter_5_min
    P9_totaltid = current_time - P9_starttimer
    if ((P9_timedifference.total_seconds() >= timefordelete) and not P9["Ledig"]):
        P9["Ledig"] = True
        boat_count-= 1
        alarm = False
        P9_lengde = P9["Lengde"]
        state_P9 = 'P9_false'
        send(state_P9)
        
        # Tidsformat
        if P9_totaltid.total_seconds() > 7200:
            tid_format = f"{(P9_totaltid.total_seconds()-timefordelete)/3600:.2f} timer"
            alarm = True
        elif P9_totaltid.total_seconds() > 60:
            tid_format = f"{(P9_totaltid.total_seconds()-timefordelete)/60:.2f} minutter"
        else:
            tid_format = f"{(P9_totaltid.total_seconds()-timefordelete):.2f} sekunder"

	
        # lengde og pris
        if (P9["Lengde"] > 9.5):
            pris = 300
        else:
            pris = 250 
        with open(f'boat_data_uke{ukenummer}.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([f"{current_time.strftime('%Y-%m-%d %H:%M:%S')}", "P9 AVREISE"])
        if (P9_totaltid.total_seconds()-timefordelete > 5): # Ikke Rapporter hvis stått under et visst antall sekunder.
            print(f"Parkering 9 var opptatt fra {P9_starttimer.strftime('%Y-%m-%d %H:%M:%S')} UTC og stod der i {tid_format}")
            with open('rapport.csv', mode='a', newline='') as file:
                writer = csv.writer(file, delimiter = ',')
                if alarm:
                    writer.writerow([f"Parkering 9 ble opptatt {P9_starttimer.strftime('%Y-%m-%d %H:%M:%S')}UTC og stod der i {tid_format}", f"Båten er {P9_lengde} meter lang.", f"AVGIFTSBELAGT", f"vedkommende skal betale:", f"{pris}", f"kr"])
                else:
                    writer.writerow([f"Parkering 9 ble opptatt {P9_starttimer.strftime('%Y-%m-%d %H:%M:%S')}UTC og stod der i {tid_format}", f"Båten er {P9_lengde} meter lang"])


# ----------------------------------------------------------------------------------------------------------------------------- #
### --- KODE --- ###

# Oppretter CSV-fil og skriver headeren hvis den ikke allerede finnes
try:
    with open(f'boat_data_uke{ukenummer}.csv', mode='x', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Tidspunkt", "Parkeringsplass", "Lengde", "Antall båter nå"])
except FileExistsError:
    # Filen eksisterer allerede, Du kan vurdere å ha ingenting gjøres
    with open(f'boat_data_uke{ukenummer}.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Tidspunkt", "Parkeringsplass", "Lengde", "Antall båter nå"])

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
    {"Id": (1), "Left": (45), "Right": (1080), "Bottom": (604), "Top": None, "Area": (296000), "Ledig": (True), "Lengde": 0, },
    {"Id": (2), "Left": (1150), "Right": (1445), "Bottom": (772), "Top": None, "Area": (100000), "Ledig": (True), "Lengde": 0, },
    # Legg til flere parkeringsplasser etter behov
]

redningsleider_piksler = [(1240, 129)] # Vi har bare en som et eksempel.
redningsleider_tidtaker = None  # Timer for blocking detection (skal ikke gi alarm med en gang)

# Verdiene kan hentes slik: P1["Left"]
P1, P9 = parking_spots[0], parking_spots[1]
# Timere er enklere å jobbe med som egne variabler.
P1_starttimer = P9_starttimer = P1_slettes_etter_5_min = P9_slettes_etter_5_min = P1_sistlogg = P9_sistlogg = datetime.datetime.now() 
xtolerance = 70  # Disse toleranseverdiene kan legges i parking_spots og ha unike toleranser for hver P-plass dersom ønskelig
ytolerance = 60
areatolerance = 5000
timefordelete = 10 # 5 min er 300.
totimer = 50 # skal være 7200 (2 timer)
state_P1 = "P1_false" # PLS
state_P9 = "P9_false"
state_DIP = "DIP_false"
send(state_DIP)
send(state_P1)
send(state_P9)



print('********************* VELG BILDEDETEKSJONSMODELL *********************')
print('           SKRIV INN s FOR STANDARDMODELL OG e FOR EGEN MODELL')


running = False
while (not running):
    a = input()

    if a == 's':
        running = True
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
        running = True
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


            display.Render(img)
            display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
            
    else:
        print("Ugyldig valg. Vennligst velg 's' for standardmodell eller 'e' for egen modell.")
