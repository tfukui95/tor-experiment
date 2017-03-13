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
