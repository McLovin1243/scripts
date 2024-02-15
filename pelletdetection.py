#https://github.com/BO24EH-02/scripts.git
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput
from jetson_inference import snap7

IP = '192.168.0.1'  #PLC IP adress

print(IP) 

RACK = 0 

SLOT = 0 

PLC = snap7.client.Client() 

if PLC.connect(IP,RACK,SLOT): #establish connections with Siemens PLC if ip is correct
    print(PLC.get_cpu_state())
else:
    print("ERROR: PLC not connectet")    


net = detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = videoSource("csi://0")      # '/dev/video0' for V4L2
display = videoOutput("display://0") # 'my_video.mp4' for file

while display.IsStreaming():
    img = camera.Capture()

    if img is None: # capture timeout
        continue

    detections = net.Detect(img)
    
    display.Render(img)
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))