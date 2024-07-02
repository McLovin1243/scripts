import socket
import time
import datetime
import csv
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput



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
# Timere er enklere å ha som egne variabler.
P1_starttimer = datetime.datetime.now() 
P2_starttimer = datetime.datetime.now()
P3_starttimer = datetime.datetime.now()
P1_slettes_etter_5_min = datetime.datetime.now()
P2_slettes_etter_5_min = datetime.datetime.now()
P3_slettes_etter_5_min = datetime.datetime.now()
P1_sistlogg = datetime.datetime.now()
P2_sistlogg = datetime.datetime.now()
P3_sistlogg = datetime.datetime.now()
xtolerance = 70  # Disse toleranseverdiene kan legges i parking_spots og ha unike toleranser for hver P-plass.
ytolerance = 60
areatolerance = 5000
timefordelete = 10 # 5 min er 300.
totimer = 50 # skal være 7200 (2 timer)

	## FUNKSJONER ##
def log_parking_status(detections):
    global parking_spots, boat_count, P1_slettes_etter_5_min, P1_starttimer, P2_slettes_etter_5_min, P2_starttimer, P3_slettes_etter_5_min, P3_starttimer, P1_sistlogg, P2_sistlogg, P3_sistlogg


    current_time = datetime.datetime.now()
    for detection in detections:
        class_name = net.GetClassDesc(detection.ClassID)
        
        if class_name == "Boat":
            class_name = "boat"
        if class_name == "boat": #Gjør det IKKE dersom den detekterer "person" eller "motorcycle"
            #Deteksjonsinfo oppdateres hver deteksjon
            boat_bottom = detection.Bottom
            boat_area = detection.Area
            boat_left = detection.Left
            # Kriteriene for å være på parkeringsplass 1.
	
	    # P1
            if (abs(boat_bottom - P1["Bottom"]) <= ytolerance and abs(boat_left - P1["Left"]) <= xtolerance):

                P1_loggpause = current_time - P1_sistlogg
                totimertimer = current_time - P1_starttimer
                P1_slettes_etter_5_min = datetime.datetime.now() # Oppdaterer at P1 er aktiv
                if P1["Ledig"]: #Hvis P1 er ledig (true)
                    P1_starttimer = current_time #Gjøres kun første gang
                    P1["Ledig"] = False 
                    print("P1 ble nå opptatt")
                    boat_count += 1 # En ny båt i parkeringssystemet
                elif (P1_loggpause.total_seconds()  > 5): # Skal ikke Write til csv hvis mindre enn 5 sekund siden sist
                    break
                elif (totimertimer.total_seconds() < totimer):
                    print("Oppdaterer P1 aktiv")
                else:
                    print("P-plass 1 har vært opptatt i 2 timer.") # Kan legge til noe mer alarm.
                        
                # Uansett om den er ny eller ikke, så lagrer vi dataen og skriver til excel.
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                P1_sistlogg = datetime.datetime.now()
                position = "Parkering nr.1"  # Posisjon av båten (x,y)
                lengthpixel = detection.Width  # Lengde på båten... ikke nøyaktig metode, må endres
                length = lengthpixel/30 - detection.Bottom/100
                P1["Bredde"] = length
                boat_data = {
                    "timestamp": timestamp,
                    "position": position,
                    "length": length,
                }
                write_to_csv(boat_data)
            
            # P2
            elif (abs(boat_bottom - P2["Bottom"]) <= ytolerance and abs(boat_left - P2["Left"]) <= xtolerance and abs(boat_area-P2["Area"]<areatolerance)):
                P2_loggpause = current_time - P2_sistlogg
                totimertimer = current_time - P2_starttimer
                P2_slettes_etter_5_min = current_time # Oppdaterer at P2 er aktiv
                if P2["Ledig"]: # Hvis P2 er ledig (true)
                    P2_starttimer = current_time
                    P2["Ledig"] = False
                    print("P2 ble nå opptatt")
                    boat_count += 1 # En ny båt i parkeringssystemet
                elif (P2_loggpause.total_seconds() > 5): # Skal ikke Write til csv hvis mindre enn 5 sekund siden sist
                    break
                elif (totimertimer.total_seconds() < totimer):
                    print("Oppdaterer P2 aktiv")
                else:
                    print("P-plass 2 har vært opptatt i 2 timer.") # Kan legge til noe mer alarm.
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                P2_sistlogg = datetime.datetime.now()
                position = "Parkering nr.2"  # Posisjon av båten (x,y)
                lengthpixel = detection.Width  # Lengde på båten... ikke nøyaktig metode, må endres
                length = lengthpixel/30 - detection.Bottom/100 # lengthpixel er i x-aksen, som kan være en del større enn bottom (y-aksen). detection.bottom/100 utgjør lite.
                P2["Bredde"] = length
                boat_data = {
                    "timestamp": timestamp,
                    "position": position,
                    "length": length,
                }
                write_to_csv(boat_data)
            
             # P3
            elif (abs(boat_bottom - P3["Bottom"]) <= ytolerance and abs(boat_left - P3["Left"]) <= xtolerance):
                P3_loggpause = current_time - P3_sistlogg
                totimertimer = current_time - P3_starttimer
                P3_slettes_etter_5_min = datetime.datetime.now() # Oppdaterer at P3 er aktiv
                if P3["Ledig"]: #Hvis P3 er ledig (true)
                    P3_starttimer = current_time #Gjøres kun første gang
                    P3["Ledig"] = False 
                    print("P3 ble nå opptatt")
                    boat_count += 1 # En ny båt i parkeringssystemet
                elif (P3_loggpause.total_seconds() > 5): # Skal ikke Write til csv hvis mindre enn 5 sekund siden sist
                    break
                elif (totimertimer.total_seconds() < totimer):
                    print("Oppdaterer P3 aktiv")
                else:
                    print("P-plass 3 har vært opptatt i 2 timer.") # Kan legge til noe mer alarm.
                        
                # Uansett om den er ny eller ikke, så lagrer vi dataen og skriver til excel.
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                P3_sistlogg = datetime.datetime.now()
                position = "Parkering nr.3"  # Posisjon av båten (x,y)
                lengthpixel = detection.Width  # Lengde på båten... ikke nøyaktig metode, må endres
                length = lengthpixel/30 - detection.Bottom/100
                P1["Bredde"] = length
                boat_data = {
                    "timestamp": timestamp,
                    "position": position,
                    "length": length,
                }
                write_to_csv(boat_data)

            else: #Utenfor parkering, da trenger vi ikke å bry oss.
                pass


# Funksjon for å skrive data til CSV-fil
def write_to_csv(data):
    with open('boat_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([data["timestamp"], data["position"], data["length"], boat_count]) # Boat count må vi tenke mer på hvordan vi vil ha

#Denne funksjonen sletter parkeringer som har vært inaktive, og lagrer rapporten over hvor lenge den stod.
def rapporttid(): 
    global parking_spots, boat_count, P1_slettes_etter_5_min, P1_starttimer, 		P2_slettes_etter_5_min, P2_starttimer, current_time  #Tror global i functions er nødvendig
    
    
    P1_timedifference = current_time - P1_slettes_etter_5_min
    P1_totaltid = current_time - P1_starttimer
    if ((P1_timedifference.total_seconds() >= timefordelete) and P1["Ledig"]==False):
        P1["Ledig"] = True
        boat_count-= 1
        alarm = False
        P1_bredde = P1["Bredde"]
        
        # Tidsformat
        if P1_totaltid.total_seconds() > totimer:
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

        print(f"Parkering 1 var opptatt fra {P1_starttimer.strftime('%Y-%m-%d %H:%M:%S')} UTC og stod der i {tid_format}")
        with open('rapport.csv', mode='a', newline='') as file:
            writer = csv.writer(file, delimiter = ',')
            if alarm:
                writer.writerow([f"Parkering 1 ble opptatt {P1_starttimer.strftime('%Y-%m-%d %H:%M:%S')}UTC og stod der i {tid_format}", f"Båten er {P1_bredde} meter lang.", f"AVGIFTSBELAGT", f"vedkommende skal betale:", f"{pris}", f"kr"])
            else:
                writer.writerow([f"Parkering 1 ble opptatt {P1_starttimer.strftime('%Y-%m-%d %H:%M:%S')}UTC og stod der i {tid_format}", f"Båten er {P1_bredde} meter lang",])



    P2_timedifference = current_time - P2_slettes_etter_5_min
    P2_totaltid = current_time - P2_starttimer
    if ((P2_timedifference.total_seconds() >= timefordelete) and P2["Ledig"]==False):
        P2["Ledig"] = True
        boat_count-= 1
        alarm = False
        P2_bredde = P2["Bredde"]
        
        # Tidsformat
        if P2_totaltid.total_seconds() > totimer:
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

        print(f"Parkering 1 var opptatt fra {P1_starttimer.strftime('%Y-%m-%d %H:%M:%S')} UTC og stod der i {tid_format}")
        with open('rapport.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            if alarm:
                writer.writerow([f"Parkering 2 ble opptatt {P2_starttimer.strftime('%Y-%m-%d %H:%M:%S')}UTC og stod der i {tid_format}", f"Båten er {P2_bredde} meter lang.", f"AVGIFTSBELAGT", f"vedkommende skal betale:", f"{pris}", f"kr"])
            else:
                writer.writerow([f"Parkering 2 ble opptatt {P2_starttimer.strftime('%Y-%m-%d %H:%M:%S')}UTC og stod der i {tid_format}", f"Båten er {P2_bredde} meter lang",])
              
    P3_timedifference = current_time - P3_slettes_etter_5_min
    P3_totaltid = current_time - P3_starttimer
    if ((P3_timedifference.total_seconds() >= timefordelete) and P3["Ledig"]==False):
        P3["Ledig"] = True
        boat_count-= 1
        alarm = False
        P3_bredde = P3["Bredde"]
        
        # Tidsformat
        if P3_totaltid.total_seconds() > totimer:
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

        print(f"Parkering 3 var opptatt fra {P3_starttimer.strftime('%Y-%m-%d %H:%M:%S')} UTC og stod der i {tid_format}")
        with open('rapport.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            if alarm:
                writer.writerow([f"Parkering 3 ble opptatt {P3_starttimer.strftime('%Y-%m-%d %H:%M:%S')}UTC og stod der i {tid_format}", f"Båten er {P3_bredde} meter lang.", f"AVGIFTSBELAGT", f"vedkommende skal betale:", f"{pris}", f"kr"])
            else:
                writer.writerow([f"Parkering 3 ble opptatt {P3_starttimer.strftime('%Y-%m-%d %H:%M:%S')}UTC og stod der i {tid_format}", f"Båten er {P3_bredde} meter lang",])
        







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
        # Print detection information. Nyttig for testing.
        for detection in detections:
      	    print(f"ClassID: {detection.ClassID}, Confidence: {detection.Confidence}, BBox:{detection.Bottom} {detection.Area} {detection.Left}")
	    """
	
        display.Render(img)
        display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
        
        current_time = datetime.datetime.now()
        # Må sette P1 til True etter 5 min inaktiv. slik at vi skriver ut rapport og nye kan komme.
        
        rapporttid()


elif a == 'e':
    net = detectNet(argv=['--model=models/boat/ssd-mobilenet.onnx', '--labels=models/boat/labels.txt', '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes', '--threshold=0.3'])
    source = "Main.mp4" 
    camera = videoSource(source) 
    display = videoOutput()  # 'my_video.mp4' for file, or sequence of images 'img_%i.jpg'

    
    while display.IsStreaming():
        img = camera.Capture()
        if img is None:
            continue

        detections = net.Detect(img)
        
        log_parking_status(detections)       
        

        # Print detection information
        #for detection in detections:
            #print(f"TrackID: {detection.TrackID}")

        display.Render(img)
        display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
        
        current_time = datetime.datetime.now()    
        # Må sette P1 til True etter 5 min inaktiv. slik at vi skriver ut rapport og nye kan komme.
        
        rapporttid()

        # time.sleep(2)

else:
    print("Ugyldig valg. Vennligst velg 's' for standardmodell eller 'e' for egen modell.")
