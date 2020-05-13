import json
import math
import sys

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
    

# def getAP():
#     interface = 'wlan0'
    
#     rssi_scanner = rssi.RSSI_Scan(interface)
#     ssids = ['GL-MT300N-V2-bd4', 'GL-MT300N-V2-303', 'GL-MT300N-V2-d22', 'GL-MT300N-V2-d2a']
    
#     ap_info = rssi_scanner.getAPinfo(ssids, sudo=True)
    
#     return ap_info


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
    global gridPoints

    xArr = []
    yArr = []
    shortestDistance = float("inf")

    for point in gridPoints:
        compareAP = point['ap']
        totalCalculatedDistance = 0.0
        
    
        for i in range(4):  # go through each AP in inputAP (4 APs)
            inputQualityString = inputAP[i]["quality"].split("/")[0]
            inputQuality = float(inputQualityString)

            compareQualityString = compareAP[i]["quality"].split("/")[0]
            compareQuality = float(compareQualityString)

            inputSignal = float(inputAP[i]["signal"])
            compareSignal = float(compareAP[i]["signal"])

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
            print("total ", totalCalculatedDistance)
            
        print("shortest", shortestDistance)
        if totalCalculatedDistance < shortestDistance:
            print("here")
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

def findAP(inputAP):
    global gridPoints
    for point in gridPoints:
        # compare all access points in a certain range
        compareAP(inputAP)
        # return the closest x and y
        point
    
    return 


# def editPoint(x,y):
#     global gridPoints
#     for point in gridPoints:
#         if(point["x"] == x and point["y"] == y):
#             point["ap"] = getAP()
#             saveFile()
#             return
        

recording = False    # setting new points in fingerprint database
editing = False     # replacing AP RSSI on given X, Y point
locating = True    # finding X, Y point given new AP RSSI
reading = False     # prints out all points and AP RSSI in database

x = 0
y = 0

# if(recording):

#     for y in range(yMax + 1):
#         for x in range(xMax + 1):
#             print("move nano to point " , x , ", " , y)
            
#             input("press enter to record APs")

#             result = getAP()
            
#             point = {
#                 'x': x,
#                 'y': y,
#                 'ap': result
#             }

#             print(point)

#             gridPoints.append(point)

#     print(gridPoints)
#     saveFile()

if(locating):
    openFile()
    # getAP()
    inputAP = [{"ssid": "BeMerry", "quality": "64/70", "signal": -46}, {"ssid": "DIRECT-F6-HP ENVY 4520 series", "quality": "42/70", "signal": -68}, {"ssid": "NETGEAR76", "quality": "50/70", "signal": -60}, {"ssid": "xfinitywifi", "quality": "31/70", "signal": -79}]
    location = compareAP(inputAP)
    print(location)
        
# if(editing):
#     openFile()
#     x = int(input("enter x point"))
#     y = int(input("enter y point"))
#     if(x <= xMax and y <= yMax):
#         editPoint(x,y)
    
if(reading):
    openFile()
    for point in gridPoints:
        print(point, '\n')