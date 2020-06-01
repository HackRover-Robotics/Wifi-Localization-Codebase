import rssi
import json
import math

xMax = 2
yMax = 2
gridPoints = []
filename = "output.json"

recording = False    # setting new points in fingerprint database
editing = False     # replacing AP RSSI on given X, Y point
locating = True    # finding X, Y point given new AP RSSI
reading = False     # prints out all points and AP RSSI in database
navigating = False  # prints out direction to move based on input X, Y point

def saveFile():
    with open(filename, "w") as outfile:
        global gridPoints
        json.dump(gridPoints, outfile)
        outfile.close()


def openFile():
    with open(filename, "r") as infile:
        global gridPoints
        gridPoints = json.load(infile)
        infile.close()
    

def getAP():
    interface = 'wlan0'
    
    rssi_scanner = rssi.RSSI_Scan(interface)
    ssids = ['GL-MT300N-V2-bd4', 'GL-MT300N-V2-303', 'GL-MT300N-V2-d22', 'GL-MT300N-V2-d2a']
    
    ap_info = rssi_scanner.getAPinfo(ssids, sudo=True)
    
    return ap_info


def compareAP(inputAP):
    '''
     iterate through all AP in database
     compare inputAP RSSI with AP RSSI in database
     find closest fingerprint 
         algorithm:
            average difference
                find total difference
                find average difference
                select smallest average difference

                PROBLEM
                inputAP: 
                AP1 : -54 signal, 56/70 quality -> avg: 55
                AP2 : -48 signal, 62/70 quality -> avg: 55

            shortest euclidian distance - ALMOST K-NN Machine learning

                shortestDistance = sqrt[(signal2^2 - inputSignal^2) + (quality2^2 - inputQuality^2)] FIRST TIME 
                shortestX = ?
                shortestY = ?
                newDistance = sqrt[(signal2^2 - inputSignal^2) + (quality2^2 - inputQuality^2)]
                if newDistance < shortestDistance :
                    shortestDistance = newDistance
                    locatedX = newX
                    locatedY = newY
                    
        https://www.geeksforgeeks.org/iterate-over-a-list-in-python/
        https://www.w3schools.com/python/python_dictionaries.asp
        "ap": [{"ssid": "BeMerry", "quality": "70/70", "signal": -37},  {"ssid": "DIRECT-F6-HP ENVY 4520 series", "quality": "52/70", "signal": -58}]
    '''

    xArr = []
    yArr = []
    shortestDistance = float("inf")

    for point in gridPoints:
        compareAP = point["ap"]
        totalCalculatedDistance = 0.0
        print("points: " + str(point['x']) + ", " + str(point['y']))
            
        for ap in compareAP:  # go through each AP in compareAP (~4 APs)
            ssid = ap["ssid"]

            for inAP in inputAP:    # go through each AP in inputAP

                inSsid = inAP["ssid"]
                if(ssid == inSsid): # find same SSID 

                    print(ssid + " == " + inSsid)
                    # if(inputAP[i]["ssid"] == compareAP[i]["ssid"]):

                    inputQualityString = inAP["quality"].split("/")[0]
                    inputQuality = float(inputQualityString)

                    compareQualityString = ap["quality"].split("/")[0]
                    compareQuality = float(compareQualityString)

                    inputSignal = float(inAP["signal"])
                    compareSignal = float(ap["signal"])

                    print("\t Quality:" + str(inputQuality) + " " + str(compareQuality))
                    print("\t Signals:" + str(inputSignal) + " " + str(compareSignal))

                    '''
                    point[1] += calculatedDistance[i]^2-0    -------inputAP
                    point[2] = calculatedDistance[1-4]
                    .
                    .
                    .
                    point[n] = calculatedDistance[1-4]
                    which one is the smallest?
                    '''
                    calculatedDistance = (compareQuality - inputQuality)**2 + (compareSignal - inputSignal)**2
                    totalCalculatedDistance += calculatedDistance

        print(totalCalculatedDistance)
            
        if totalCalculatedDistance < shortestDistance:
            shortestDistance = totalCalculatedDistance
            xArr.clear()
            yArr.clear()
            xArr.append(point['x'])
            yArr.append(point['y'])

        elif totalCalculatedDistance == shortestDistance:
            xArr.append(point['x'])
            yArr.append(point['y'])

    xSum = 0
    for x in xArr:
        xSum += x
    xAvg = xSum / len(xArr)

    ySum = 0
    for y in yArr:
        ySum += y
    yAvg = ySum / len(yArr)

    return {'x' : xAvg, 'y' : yAvg}


def editPoint(x,y):
    global gridPoints
    for point in gridPoints:
        if(point["x"] == x and point["y"] == y):
            point["ap"] = getAP()
            saveFile()
            return
        

if recording:

    for y in range(yMax):
        for x in range(xMax):
            print("move nano to point " , x , ", " , y)
            
            input("press enter to record APs")

            result = getAP()

            print(str(x) + ", " + str(y))
            
            while(len(result) < 4):
                result = getAP()
            
            for ap in result:
                print(ap["ssid"])

            point = {
                'x': x,
                'y': y,
                'ap': result
            }          

            gridPoints.append(point)

    print(gridPoints)
    saveFile()

if locating:
    openFile()
    # getAP()
    inputAP = getAP()
    while(len(inputAP) < 4):
        inputAP = getAP()

    print(inputAP)
    # [{"ssid": "BeMerry", "quality": "64/70", "signal": -46}, {"ssid": "DIRECT-F6-HP ENVY 4520 series", "quality": "42/70", "signal": -68}, {"ssid": "NETGEAR76", "quality": "50/70", "signal": -60}, {"ssid": "xfinitywifi", "quality": "31/70", "signal": -79}]
    # location = compareAP(inputAP)
    location = compareAP(inputAP)
    print(location)
        
if editing:
    openFile()
    x = int(input("enter x point"))
    y = int(input("enter y point"))
    if x <= xMax and y <= yMax:
        editPoint(x,y)
    
if reading:
    openFile()
    for point in gridPoints:
        print(point, '\n')

if navigating:
    openFile()
    destX = int(input("enter x destination"))
    destY = int(input("enter y destination"))

    while(True):
        # find our location
        locationPoint = compareAP(getAP())

        # compare with input X, Y
        if locationPoint['x'] == destX and locationPoint['y'] == destY:
            print("location reached!")
            break 

        # find direction in Y axis until Y location == Y input
        if locationPoint['y'] < destY:
            print("move nano forwards")
        elif locationPoint['y'] > destY:
            print("move nano backwards")

        # find direction in X axis until X location == X input
        if locationPoint['x'] < destX:
            print("shift the nano to the right")
        elif locationPoint['x'] > destX:
            print("shif the nano to the left")
