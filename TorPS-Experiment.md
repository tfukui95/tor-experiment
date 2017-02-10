To install Tor Path Simulator (TorPS), we first need to install python stem.

```
sudo apt-get install python-stem
```

Next we glone the TorPS github repository with

```
git clone https://github.com/torps/torps.git
```

Next we need to extract the consensus archives and server descriptor archives for the time period for which we are planning to run our experiment. We need to first create a directory for each month. For example to create the directories to store the consensus archives for the year 2016:

```
for A in 01 02 03 04 05 06 07 08 09 10 11 12
do
sudo mkdir torps/in/consensuses-2016-$A
done
```

Next we download the consensuses from the collector.torproject.org website:

```
for A in 01 02 03 04 05 06 07 08 09 10 11 12
do
sudo wget -O torps/in/consensuses-2016-$A/consensuses-2016-$A http://collector.torproject.org/archive/relay-descriptors/consensuses/consensuses-2016-$A.tar.xz
done
```

Next we do the same thing but this time for the server descriptor archives:

```
for A in 01 02 03 04 05 06 07 08 09 10 11 12
do
sudo mkdir torps/in/server-descriptors-2016-$A
sudo wget -O torps/in/server-descriptors-2016-$A/server-descriptors-2016-$A http://collector.torproject.org/archive/relay-descriptors/server-descriptors/server-descriptors-2016-$A.tar.xz
done
```

Next we need to download the necessary TorPS scripts with

```
wget https://raw.githubusercontent.com/torps/torps/master/pathsim.py
```

Now we are finally ready for path simulation. The first step is to process the Tor consensuses and server descriptors into a compact form for faster path simulation. We first must make the directories in which to store the processed files:

```
for A in 01 02 03 04 05 06 07 08 09 10 11 12
do
sudo mkdir torps/out/network-state-2016-$A
done
```

For our experiment we extracted the consensuses and server descriptors for the year 2016. Therefore run the following:

```
python pathsim.py process --start_year 2016 --start_month 2 --end_year 2016 --end_month 12 --in_dir in --out_dir out --initial_descriptor_dir in/server-descriptors-2016-01
```

We need to provide the start year and month, and the end year and month as parameters for the path simulation process. However, notice that our start month is 2 (February), and that our initial descriptor directory is ```server-descriptors-2016-01```. This is because a relay is added to the count of relays if its descriptor is found in the descriptor archive, but a relay only publishes a new descriptor after around 18 hours. Therefore if we do not start looking for descriptors from the month before, many of the relays from the start month will not be included.
