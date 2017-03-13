sudo mkdir bikes

for A in 01 02 03 
do
sudo wget -O ~/bikes/2016$A-citibike-tripdata.zip https://witestlab.poly.edu/bikes/2016$A-citibike-tripdata.zip
done
