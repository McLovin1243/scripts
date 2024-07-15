import socket
import time
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput

print('********************* VELG BILDEDETEKSJONSMODELL *********************')
print('           SKRIV INN s FOR STANDARDMODELL OG e FOR EGEN MODELL')
a = input()

#Programkode for å kjøre eksisterende objektdetekterings sett.
if a == 's' :
    net = detectNet("ssd-mobilenet-v2", threshold =0.7)
    source = "kai.mp4" 
    camera = videoSource(source) 
    display = videoOutput() # 'my_video.mp4' for fil for sekvens av bilder image 'img_%i.jpg'
    
    while display.IsStreaming():
        img =camera.Capture()

        if img is None:
            continue

        detections =net.Detect(img)

        display.Render(img)
        display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

if a == 'e' :
    net = detectNet(argv=['--model=models/boat/ssd-mobilenet.onnx', '--labels=models/boat/labels.txt', '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes', '--threshold=0.3'])
    source = "kai.mp4" 
    camera = videoSource(source) 
    display = videoOutput() # 'my_video.mp4' for fil for sekvens av bilder image 'img_%i.jpg'
        
    while display.IsStreaming():
            img =camera.Capture()

            if img is None:
                continue

            detections =net.Detect(img)

            display.Render(img)
            display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
