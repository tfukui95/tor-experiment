# This python script takes in a tshark traffic instance saved as a csv file,
# and creates a fingerprint of that instance by

import csv
filename = 'finger.csv'
with open(filename, 'rb') as csvfile:
  filereader = csv.reader(csvfile,delimiter= ',')
  with open('finger2.csv', 'wb') as csvfile2:
    filewriter= csv.writer(csvfile2, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in filereader:
      print row[0]
      print row[1]
      print row[2]
#if (row[2] == 192.168.5.200):
#filewriter.writerow([+, row[0]])
#else:
#filewrite.writerow([-, row[0]])
