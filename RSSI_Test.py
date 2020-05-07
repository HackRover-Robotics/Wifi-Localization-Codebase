import rssi
import json

xMax = 2
yMax = 2
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
    interface = 'wlan0'
    
    rssi_scanner = rssi.RSSI_Scan(interface)
    ssids = ['GL-MT300N-V2-bd4', 'GL-MT300N-V2-303', 'GL-MT300N-V2-d22', 'GL-MT300N-V2-d2a']
    
    ap_info = rssi_scanner.getAPinfo(ssids, sudo=True)
    
    return ap_info
     
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
reading = False

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

            print(point)

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
    
if(reading):
    openFile()
    for point in gridPoints:
        print(point, '\n')

