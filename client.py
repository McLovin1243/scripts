import socket
import time
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput

HEADER = 64
port =5151
FORMAT = 'utf-8'
SERVER =  '192.168.0.3'
ADDR = (SERVER,port)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
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
    net = detectNet("ssd-mobilenet-v2", threshold =0.5)
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
        


#Programkode for å kjøre eget treningsett med pellet deteksjon

if a == 'f':
    net = detectNet(argv=['--model=models/rev11/ssd-mobilenet.onnx', '--labels=models/rev11/labels.txt', '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes', '--threshold=0.5'])
    print("**************************Choose test file ***************************")
    print("1. Klippet.MP4")
    print("2. foring.MP4")
    print("3. foring2.MP4")
    print("4. foring3.MP4")
    b = input()
    source = "klippet.mp4"
    
    if(b == '1'):
    	source = "klippet.mp4"
    elif(b == '2'):
    	source = "klippet.mp4"
    elif(b == '3'):
    	source = "klippet.mp4" 
    elif(b == '4'):
    	source = "testF.mp4"
    else: 
    	source = "klippet.mp4" 
    camera = videoSource('foring3.mp4') 
    display = videoOutput() # 'my_video.mp4' for file

    while display.IsStreaming():
        img = camera.Capture()
        counter = 0
        state = "true"

        if img is None: # capture timeout
            continue
        detections = net.Detect(img)
    
        for detection in detections:
            class_name = net.GetClassDesc(detection.ClassID)
            center = detection.Center
            confidence = detection.Confidence
        
    
            if class_name == "pellet" and confidence > 0.5:
                print("PELLETS:")
                print(center)
                counter +=1
                if counter > 5:
            	    state='false'   
            elif counter < 5 and class_name == "salmon":
                state='true'

    
        print(counter)
        send(state)
  

    
        display.Render(img)
        display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
    

    
        














