```
sudo apt-get update
sudo apt-get install unzip

sudo mkdir bikes

for A in 01 02 03 04 05 06 07 08 09
do
sudo wget -O ~/bikes/2016$A-citibike-tripdata.zip https://witestlab.poly.edu/bikes/2016$A-citibike-tripdata.zip
done

for A in 01 02 03 04 05 06 07 08 09
do
sudo unzip ~/bikes/2016$A-citibike-tripdata.zip 
done

//printing the first column
awk -F "\"*,\"*" '{print $1}' 201601-citibike-tripdata.csv

awk -F "\"*,\"*" '{print $4}' 201601-citibike-tripdata.csv | sort | uniq | stations.txt

sudo apt-get install imagemagick
import csv

filename = '201601-citibike-tripdata.csv'
with open(filename, 'rb') as csvfile:
  filereader = csv.reader(csvfile,delimiter= ',')
  header = next(filereader)
  for row in filereader:
    print(row[4])
    
print(header)

durations = []
filename = '201601-citibike-tripdata.csv'
with open(filename, 'rb') as csvfile:
  filereader = csv.reader(csvfile,delimiter= ',')
  header = next(filereader)
  for row in filereader:
    durations.append(int(row[0])
   
print(durations)
```

Using pandas

```
sudo apt-get install python-pandas

import pandas as pd
filename='201601-citibike-tripdata.csv'
df=pd.read_csv(filename, sep=',')

print(df)

df.columns

df.head()

df.tail()

df.tail(3)

df.describe()
```

Completing the assignment

```
awk -F "\"*,\"*" '{print $5}' 201601-citibike-tripdata.csv | sort | uniq > stations.txt
wc -l stations.txt > xxx
read lines nameFile< xxx
echo $lines

counts = []
import csv
filename = '201601-citibike-tripdata.csv'
with open(filename, 'rb') as csvfile:
  filereader = csv.reader(csvfile,delimiter= ',')
  header = next(filereader)
  with open('stations.txt') as inputfile:
    for line in inputfile:
      x=0
      line = line.replace("\n", "")
      csvfile.seek(0,0)
      for row in filereader:
        if (row[4] == line):
          x=x+1
      counts.append(x)
        
  print counts
