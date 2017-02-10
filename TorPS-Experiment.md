To install Tor Path Simulator (TorPS), we first need to install python stem.

```
sudo apt-get install python-stem
```

Next we glone the TorPS github repository with

```
git clone https://github.com/torps/torps.git
```

Next we need to extract the consensus archives and descriptor archives for the time period for which we are planning to run our experiment. We need to first create a directory for each month. For example for the year 2016:

```
for A in 01 02 03 04 05 06 07 08 09 10 11 12
do
mkdir torps/in/consensuses-2016-$A
done
```

