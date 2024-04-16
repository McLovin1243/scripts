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


net = detectNet(argv=['--model=models/rev10/ssd-mobilenet.onnx', '--labels=models/rev10/labels.txt', '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes', '--threshold=0.3'])

print('********************* CHOOSE FILE OR WEBCAM *********************')
print('           enter f/w f is MP4 File and w is Webcam')
a = input()
if a == 'w' :
    camera = videoSource('/dev/video0')
if a == 'f':
    camera = videoSource('foring3.mp4')
    
display = videoOutput() # 'my_video.mp4' for file




while display.IsStreaming():
    img = camera.Capture()

    if img is None: # capture timeout
        continue

   # detections = net.Detect(img)
   # if detections:
    #    print        
    #	send('true')
    #else:
    #	send('false')

    detections = net.Detect(img)

    for detections in detections:
        class_name = net.GetClassDesc(detections.ClassID)
        center = detections.Center
        confidence = detections.Confidence
    
        if class_name == "pellet" and confidence > 0.5:
            pelletCounter =+ 1
            print("PELLETS: "+pelletCounter)
            send('false')
        else:
            send('true')

    
    display.Render(img)
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))









