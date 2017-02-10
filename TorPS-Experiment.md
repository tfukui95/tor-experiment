To install Tor Path Simulator (TorPS), we first need to install python stem.

```
sudo apt-get install python-stem
```

Next we glone the TorPS github repository with

```
git clone https://github.com/torps/torps.git
```

Next we need to extract the consensus archives and descriptor archives for the time period for which we are planning to run our experiment. We need to first create a directory for each month. For example to create the directories to store the consensus archives for the year 2016:

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
sudo wget -O torps/in/consensuses-2016-$A http://collector.torproject.org/archive/relay-descriptors/consensuses/consensuses-2016-$A.tar.xz
done
```
