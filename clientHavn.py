import socket
import time
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput

#definerer variabler og setter opp socket kommunikasjon
HEADER = 64
port =5151
FORMAT = 'utf-8'
SERVER =  '192.168.0.3'
ADDR = (SERVER,port)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg): #funksjon som sender melding via socket kommunikasjon
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length =str(msg_length).encode(FORMAT)
    send_length += b' '*(HEADER-len(send_length))
    client.send(send_length)
    client.send(message)



print('********************* CHOOSE FILE OR WEBCAM *********************')
print('           enter f/w f is MP4 File and w is Webcam')
a = input()


#Programkode for å kjøre eksisterende objektdetekterings sett.
if a == 'w' :
    net = detectNet("ssd-mobilenet-v2", threshold =0.7)
    camera = videoSource('/dev/video0')
    display = videoOutput()

    while display.IsStreaming():
        img =camera.Capture()

        if img is None:
            continue

        detections =net.Detect(img)

        if detections:
            send("true")
        else:
            send("false")

        display.Render(img)
        display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
        


if a == 'f':
    net = detectNet(argv=['--model=models/boat/ssd-mobilenet.onnx', '--labels=models/boat/labels.txt', '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes', '--threshold=0.3'])
    #net = detectNet("ssd-mobilenet-v2", threshold =0.4)
    
    print("**************************Choose test file ***************************")
    print("1. test.MP4")
    print("2. helgevold.MP4")
    print("3. foring3.MP4")
    print("4. kai.MP4")
    b = input()
    source = "klippet.mp4"
    
    if(b == '1'):
    	source = "test.mp4"
    elif(b == '2'):
    	source = "helgevold.mp4"
    elif(b == '3'):
    	source = "kai.mp4" 
    elif(b == '4'):
    	source = "kai2.mp4"
    else: 
    	source = "klippet.mp4"  	 
    	
    camera = videoSource(source) 
    display = videoOutput() # 'my_video.mp4' for fil for sekvens av bilder image 'img_%i.jpg'
    
    while display.IsStreaming():
        img =camera.Capture()

        if img is None:
            continue

        detections =net.Detect(img)




        display.Render(img)
        display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
