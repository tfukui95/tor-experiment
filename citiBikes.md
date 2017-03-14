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
with opern(filename, 'rb') as csvfile:
  filereader = csv.reader(csvfile,delimiter= ',')
  for row in filereader:
    print(','.join(row))

