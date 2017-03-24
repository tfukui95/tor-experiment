# This python script takes in a tshark traffic instance saved as a csv file,
# and creates a fingerprint of that instance by

import csv
import argparse

# Add command line arguments. To see them, run "python scriptname.py --help"
parser = argparse.ArgumentParser(description='Process a packet capture.')
parser.add_argument('--filename', default='finger.csv', help='Name of packet capture file.')
parser.add_argument('--ip', default='192.168.4.100', help='IP address of client.')

args = parser.parse_args()

filename = args.filename
ip = args.ip
sizelist = []

# Open packet capture file and read it in and then close it
with open(filename, 'rb') as csvfile:
  filereader = csv.reader(csvfile,delimiter= ',')
  for row in filereader:
      # Identify direction
      size = int(row[0])
      if row[2] == ip:
          size = -1*size
      sizelist.append(size)

# Filter out packets with size 52 - actually, 66
filterlist = []
for size in sizelist:
    if not (size == -66 or size == 66):
        filterlist.append(size)

# Insert size markers at every direction change
sizemarkerlist = []
previousDirection = 1
sizeMarker = 0
for size in filterlist:
    direction = 1
    if size < 0:
        direction = -1
    if direction == previousDirection:
        sizeMarker += abs(size)
    else:  # if the direction has changed
        sizemarkerlist.append('S' + str((sizeMarker/610+1)*600))
        sizeMarker = abs(size)
        previousDirection = direction
    sizemarkerlist.append(size)
# Append size marker for the last set of packets after going through the list
sizemarkerlist.append('S' + str((sizeMarker/610+1)*600))

# Insert total transmitted byte markers at the end
totalByteList = []
totalSizeP = 0 # total byte count for outgoing packets
totalSizeN = 0 # total byte count for incoming packets
for size in sizemarkerlist:
    direction = 1
    if size < 0:
        direction = -1
    if not isinstance( size , int ):
        pass
    elif direction == 1:
        totalSizeP += abs(size)
    elif direction == -1:
        totalSizeN += abs(size)
    totalByteList.append(size)
totalByteList.append('TS+' + str((totalSizeP-1)/10000+1*10000)) # Append total number of bytes marker
totalByteList.append('TS-' + str((totalSizeN-1)/10000+1*10000))

# Insert number markers
numberMarkerList = []
previousDirection = 1
numberCount = 0
for size in totalByteList:
    direction = 1
    if size < 0:
        direction = -1
    if not isinstance( size , int ):
        pass
    elif direction != previousDirection: #Change in direction, insert number marker
        if (numberCount == 1):
            numberMarkerList.append('N1')
        elif (numberCount == 2):
            numberMarkerList.append('N2')
        elif (numberCount >= 3 and numberCount <= 5):
            numberMarkerList.append('N3-5')
        elif (numberCount >= 6 and numberCount <= 8):
            numberMarkerList.append('N6-8')
        elif (numberCount >= 9 and numberCount <= 13):
            numberMarkerList.append('N9-13')
        else: # The number count is higher than 13
            numberMarkerList.append('N>14')
        previousDirection = direction
        numberCount = 0
    if isinstance( size , int ):
        numberCount += 1
    numberMarkerList.append(size)

# Insert HTML marker
htmlMarkerList = []
previousDirection = 1
htmlMarker = 0
htmlFlag = 0
for size in numberMarkerList:
    direction = 1
    if size < 0:
        direction = -1
    if not isinstance( size , int ): # If the row is a marker
        pass # do nothing
    elif direction == -1 and htmlFlag == 0: #If the packet is part of the html document
        htmlMarker += abs(size)
        previousDirection = -1
    # After the last html packet has been received
    elif direction == 1 and htmlFlag == 0 and previousDirection == -1:
        htmlMarkerList.append('H' + str(htmlMarker/610+1*600)) # Append the html marker
        htmlFlag = 1 # Reading html request has finished
    htmlMarkerList.append(size)


# Insert occurring packet size markers
occurringList = []
uniqueP = []
uniquePFlag = 0
uniqueN = []
uniqueNFlag = 0

for size in htmlMarkerList:
    direction = 1
    if size < 0:
        direction = -1
    if not isinstance( size , int ):
        pass
    elif direction == 1:
        for A in uniqueP:
            if(A == size): # If we find a match, raise a flag and stop
                uniquePFlag = 1
                break
        if(uniquePFlag == 0): # If there was no match in the list, append
            uniqueP.append(size)
        else:
            uniquePFlag = 0
    elif direction == -1:
        for A in uniqueN:
            if(A == size): # If we find a match, raise a flag and stop
                uniqueNFlag = 1
                break
        if(uniqueNFlag == 0): # If there was no match in the list, append
            uniqueN.append(size)
        else:
            uniqueNFlag = 0
    occurringList.append(size)
occurringList.append('OP+' + str((((len(uniqueP)-1)/2)+1)*2)) # Append occurring packet marker
occurringList.append('OP-' + str((((len(uniqueN)-1)/2)+1)*2))


# Insert percent incoming/outgoing packet marker and total number of packets markers
packetList = []
nPacketsP = 0
nPacketsN = 0
direction = 1
for size in occurringList:
    direction = 1
    if size < 0:
        direction = -1
    if not isinstance( size , int ):
        pass
    elif direction == 1:
        nPacketsP += 1
    elif direction == -1:
        nPacketsN += 1
    packetList.append(size)
percentPoverN = float(nPacketsP) / nPacketsN # calculate incoming/outgoing percentage
# Append the incoming/outgoing percent marker
packetList.append('PP-' + str("%.2f" % (float((int(((((percentPoverN-.01)*100))/5)+1)*5))/100)))
 # Append the total number of packet markers
packetList.append('NP+' + str((((nPacketsP-1)/15)+1)*15))
packetList.append('NP-' + str((((nPacketsN-1)/15)+1)*15))

print packetList
