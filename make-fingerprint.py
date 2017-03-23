# This python script takes in a tshark traffic instance saved as a csv file,
# and creates a fingerprint of that instance by

import csv
import argparse

# Add command line arguments. To see them, run "python scriptname.py --help"
parser = argparse.ArgumentParser(description='Process a packet capture.')
parser.add_argument('--filename', default='finger.csv', help='Name of packet capture file.')

args = parser.parse_args()

filename = args.filename
with open(filename, 'rb') as csvfile:
  filereader = csv.reader(csvfile,delimiter= ',')
  with open('finger2.csv', 'wb') as csvfile2:
    filewriter= csv.writer(csvfile2, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    sizeMarker = 0
    totalSizeP = 0
    totalSizeN = 0
    uniqueP = []
    uniquePFlag = 0
    uniqueN = []
    uniqueNFlag = 0
    nPacketsP = 0
    nPacketsN = 0
    flag = -1
    for row in filereader:
      if (int(row[0]) > 85):
        if (row[2] == '192.168.5.200'):
          nPacketsP += 1
          if (flag > 0):
            flag += 1
            sizeMarker += int(row[0])
            filewriter.writerow(['+', row[0]])
          else:
            if (flag == -1):
              filewriter.writerow(['N', '1'])
            elif (flag == -2):
              filewriter.writerow(['N', '2'])
            elif (flag <= -3 and flag >= -5):
              filewriter.writerow(['N', '3-5'])
            elif (flag <= -6 and flag >= -8):
              filewriter.writerow(['N', '6-8'])
            elif (flag <= -9 and flag >= -13):
              filewriter.writerow(['N', '9-13'])
            else:
              filewriter.writerow(['N', '>14'])
            filewriter.writerow(['S', int(((sizeMarker/610)+1)*600)])
            sizeMarker = int(row[0])
            flag = 1
            filewriter.writerow(['+', row[0]])
          totalSizeP += int(row[0])
          uniquePFlag = 0
          for A in uniqueP:
            if(A == row[0]):
              uniquePFlag = 1
              break
          if(uniquePFlag == 0):
            uniqueP.append(row[0])
        else:
          nPacketsN += 1
          if (flag < 0):
            flag -= 1
            sizeMarker += int(row[0])
            filewriter.writerow(['-', row[0]])
          else:
            if (flag == 1):
              filewriter.writerow(['N', '1'])
            elif (flag == 2):
              filewriter.writerow(['N', '2'])
            elif (flag >= 3 and flag <= 5):
              filewriter.writerow(['N', '3-5'])
            elif (flag >= 6 and flag <= 8):
              filewriter.writerow(['N', '6-8'])
            elif (flag >= 9 and flag <= 13):
              filewriter.writerow(['N', '9-13'])
            else:
              filewriter.writerow(['N', '>14'])
            filewriter.writerow(['S', int(((sizeMarker/610)+1)*600)])
            sizeMarker = int(row[0])
            flag = -1
            filewriter.writerow(['-', row[0]])
          totalSizeN += int(row[0])
          uniqueNFlag = 0
          for A in uniqueN:
            if(A == row[0]):
              uniqueNFlag = 1
              break
          if(uniqueNFlag == 0):
            uniqueN.append(row[0])
      else:
        print row[0]
    if (flag == 1 or flag == -1):
      filewriter.writerow(['N', '1'])
    elif (flag == 2 or flag == -2):
      filewriter.writerow(['N', '2'])
    elif ((flag >= 3 and flag <= 5) or (flag <= -3 and flag >= -5)):
      filewriter.writerow(['N', '3-5'])
    elif ((flag >= 6 and flag <= 8) or (flag <= -6 and flag >= -8)):
      filewriter.writerow(['N', '6-8'])
    elif ((flag >= 9 and flag <= 13) or (flag <= -9 and flag >= -13)):
      filewriter.writerow(['N', '9-13'])
    else:
      filewriter.writerow(['N', '>14'])
    filewriter.writerow(['S', int(((sizeMarker/610)+1)*600)])
    totalPackets = nPacketsP + nPacketsN
    perPacketsP = float(nPacketsP) / totalPackets
    perPacketsN = float(nPacketsN) / totalPackets
    filewriter.writerow(['TS+',int((((totalSizeP-1)/10000)+1)*10000)])
    filewriter.writerow(['TS-',int((((totalSizeN-1)/10000)+1)*10000)])
    filewriter.writerow(['OP+',int((((len(uniqueP)-1)/2)+1)*2)])
    filewriter.writerow(['OP-',int((((len(uniqueN)-1)/2)+1)*2)])
    filewriter.writerow(['PP+', "%.2f" % (float((int((((perPacketsP*100))/5)+1)*5))/100)])
    filewriter.writerow(['PP-', "%.2f" % (float((int((((perPacketsN*100))/5)+1)*5))/100)])
    filewriter.writerow(['NP+', int((((nPacketsP-1)/15)+1)*15)])
    filewriter.writerow(['NP-', int((((nPacketsN-1)/15)+1)*15)])
