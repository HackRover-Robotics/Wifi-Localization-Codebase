# import rssi

# interface = 'Wi-Fi' 
# # wlps01 name for Mac / Ubuntu 
# # Type ifconfig into terminal

# rssi_scanner = rssi.RSSI_Scan(interface)

# # GL-MT300N-V2-XXX
# # bd4,303,d22,d2a

# ap_info = rssi_scanner.getAPinfo(sudo = True)

# print(ap_info)
# # python Get-pip.py

import json

xMax = 5
yMax = 5
gridPoints = []

def saveFile():
    with open("output.json", "w") as outfile:
        global gridPoints
        json.dump(gridPoints, outfile)
        outfile.close()
    
def openFile():
    with open("output.json", "r") as infile:
        global gridPoints
        gridPoints = json.load(infile)
        infile.close()
    

def getAP():
    return [{'ssid': 'BeMerry', 'quality': '56/70', 'signal': -54}, {'ssid': 'NETGEAR76', 'quality': '62/70', 'signal': -48}, {'ssid': 'CenturyLink4688', 'quality': '42/70', 'signal': -68}]
     
def findAP(inputAP):
    global gridPoints
    for point in gridPoints:
        # compare all access points in a certain range
        # return the closest x and y
        point
    
    return 

def editPoint(x,y):
    global gridPoints
    for point in gridPoints:
        if(point["x"] == x and point["y"] == y):
            point["ap"] = getAP()
            saveFile()
            return
        

recording = True
editing = False
locating = False

x = 0
y = 0

if(recording):

    for y in range(yMax + 1):
        for x in range(xMax + 1):
            print("move nano to point " , x , ", " , y)
            
            input("press enter to record APs")

            result = getAP()
            
            point = {
                'x': x,
                'y': y,
                'ap': result
            }

            gridPoints.append(point)

    print(gridPoints)
    saveFile()

if(locating):
    openFile()
    inputAP = getAP()
    findAP(inputAP)

        
if(editing):
    openFile()
    x = int(input("enter x point"))
    y = int(input("enter y point"))
    if(x <= xMax and y <= yMax):
        editPoint(x,y)
    

