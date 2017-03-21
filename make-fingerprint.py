# This python script takes in a tshark traffic instance saved as a csv file,
# and creates a fingerprint of that instance by

import csv
filename = 'finger.csv'
with open(filename, 'rb') as csvfile:
  filereader = csv.reader(csvfile,delimiter= ',')
  with open('finger4.csv', 'wb') as csvfile2:
    filewriter= csv.writer(csvfile2, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    sizeMarker = 0
    totalSizeP = 0
    totalSizeN = 0
    flag = 1
    for row in filereader:
      if (int(row[0]) > 85):
        if (row[2] == '192.168.5.200'):
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
            filewriter.writerow(['S', sizeMarker])
            sizeMarker = int(row[0])
            flag = 1
            filewriter.writerow(['+', row[0]])
          totalSizeP += int(row[0])
        else:
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
            filewriter.writerow(['S', sizeMarker])
            sizeMarker = int(row[0])
            flag = -1
            filewriter.writerow(['-', row[0]])
          totalSizeN += int(row[0])
      else:
        print row[0]
    filewriter.writerow(['T+',totalSizeP])
    filewriter.writerow(['T-',totalSizeN])
