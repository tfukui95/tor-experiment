# Implementation of Website Fingerprinting on GENI

## Gaining a Better Understanding of Website Fingerprinting

In order to be able to perform a successful website fingerprinting attack on our
private Tor network, we must first go through the steps of understanding the
specifics of this attack fully. First we define two settings of a dataset that
are possible:

* __Closed-world dataset__- the situation where the attacker already knows the set
of possible webpages that the victim user uses. This scenario is a bit unrealistic
because the probability of compromising the user increases drastically by only
having to gain packet traces from a few websites.

* __Open-world dataset__- the more realistic situation where the attacker does not
know what kinds of pages the user goes on, which makes the ranges of webpages basically
infinite.

For our experiment, clearly we are going to be following the closed-world dataset
because of the difficulty of simulating an open-world dataset experiment, and due
to a limit in resources.

Next, let us take a look at the general procedure of website fingerprinting:

1. The attacker first listens to and records packet traces from several websites that
may be possible websites that the user visits. The attacker uses a traffic analyzer
tool for example tcpdump to capture packet traces of IP layer packets. These packets
are known as _training instances_
2. Using information captured such as the length of the packet, the time sent and
received, etc. the attacker creates a profile of the website, also known as a _fingerprint_ [1].
3. Next the attacker listens on the target user's network and similarly captures
packet that is going in and out from the user. However this data is not going to
be blatantly similar to the fingerprint that the attacker creates in step 2, due
to a difference in user, possible packet fragmentation, and website updates. These
packets are known as _test instances_
4. The attacker tries to compromise the target user by comparing the website fingerprint
and user data by looking at them with the eye, or uses statistical methods
to probabilistically come to a conclusion.

### Characteristics of Packet Traces

Now let us go into more detail of the website fingerprinting process. Many of the
specific details that we cover come from an attack that has been performed by
Panchenko, et al. and is described in their paper called _Website Fingerprinting
in Onion Routing Based Anonymization Networks_ [1].

Now for each website, the attacker first collects around 20 instances of traffic.
Within this traffic, there are many characteristics that the attacker must look
out for to create a better more detailed fingerprint of the website.

__Size and Direction__- The size of the packet and whether the packet is ingoing or outgoing
is recorded. Incoming packets are marked as positive, while those that are outgoing
are marked as negative. Keeping track of the order in which the packets arrived
is important as well.

__Filtering ACK Packets__- Acknowledgement packets are sent back and forth almost
constantly, and do not provide any useful information to the attacker. Therefore
we first filter out packets of these size.

__Size Markers__- These are markers to be placed whenever the direction of
traffic changes from ingoing to outgoing and vice-versa. These markers must work
in conjunction with filtering out the ACK packets. These markers note how much bytes
went a certain direction before going the other.

__HTML Markers__- Whenever a request for a webpage is made, the initial process is
to request for the HTML document. Being that every site has an HTML document of
a different size, we can use this information to make the packet trace more unique.
We place an HTML marker after the HTML document is fully received.

__Total Transmitted Bytes__- This involves adding up separately the total number of
bytes sent and received at the end of the packet trace.

__Number Markers__- These markers are similar to size markers, but instead mark how
many packets came a certain direction before switching to the other direction.

__Occurring Packet Sizes__- This marker keeps track of the number of unique packet
sizes there were in the packet trace, and appended at the end of trace.

__Percentage of Incoming Packets__- This step involves finding the percentage of
packets that were incoming compared to outgoing.

__Total Number of Packets__- Similar to adding up the total number of bytes sent
and received, the total number of packets is also counted.

## Setting up the Website Fingerprinting Experiment

We will now be setting up our own website fingerprinting experiment on GENI. The
following steps will be taken for this experiment:

1. Reserve resources and set up new a new private Tor network
2. Get the homepages of a number of sites onto the webserver
3. Create a fingerprint for each site
4. Hit a random site on the client, and see if there is a match with any of the
fingerprints.

For each website's fingerprint as well as the client's traffic that we capture,
we will be creating plots as visuals to compare the fingerprints.

### Setting up a new Private Tor Network

For the purposes of this experiment, we will be slightly changing the topology of
our private Tor network to better suit our experiment. The following is our new
topology:

![](https://raw.githubusercontent.com/tfukui95/tor-experiment/master/ToyTopology2.png)  

We have made three changes to this topology:

1. Remove the direct link between the client and webserver
2. Remove a link from the client to the Tor network, leaving only one
3. Add another link for the directory server, for a total of two links

The total number of VMs remains the same, as well as the IP addresses. In the GENI
Portal, create a new slice. Load the RSpec from the following URL:
https://raw.githubusercontent.com/tfukui95/tor-experiment/master/final_exp_request_rspec.xml

After the topology is loaded onto your canvas, click "Site", and choose an InstaGENI
site to reserve our resources from. Then press Reserve Resources. After the topology
is ready to be used, and we are logged into each VM, we will continue with setting
up each VM.

Since we have already went through the steps of setting up each VM very thoroughly,
let us not go into too much detail. Instead we will simply set up the VMs using
the script files on my [Github page](https://github.com/tfukui95/tor-experiment). The
order in which the VMs are set up is very important. Making sure that the directory
server is set up first before any of the other nodes is vital for the private Tor
network to be set up properly, as the Tor configuration files for the rest of the nodes
are first created in the directory server. Once the directory server is set up, the
order of setup of the other VMs is flexible. To setup  the directory server, go to
the directory server VM and run

```
wget https://raw.githubusercontent.com/tfukui95/tor-experiment/master/wfp-directoryserver.sh
bash wfp-directoryserver.sh
```

After that is finished, let us setup the webserver, relays, and client VMs. On the
webserver run

```
wget https://raw.githubusercontent.com/tfukui95/tor-experiment/master/wfp-webserver.sh
bash wfp-webserver.sh
```

On each of the relays run

```
wget https://raw.githubusercontent.com/tfukui95/tor-experiment/master/wfp-router.sh
bash wfp-router.sh
```

Lastly on the client VM run

```
wget https://raw.githubusercontent.com/tfukui95/tor-experiment/master/wfp-client.sh
bash wfp-client.sh
```

Now that all the VMs are setup, reconfirm that the private Tor network is up and
running by using Tor Arm on each of the nodes:

```
sudo -u debian-tor arm
```

### Setting up Websites on the Webserver

Now we will be setting up the webserver for our experiment. We will be saving
homepages of 5 different website homepages onto our webserver, so that we can create
fingerprints of these websites later. The following are the 5 websites:

1. NYU Tandon School of Engineering
2. Facebook
3. Youtube
4. Reddit
5. Official New York Mets Website

For each website, we will be storing the webpage in its own directory inside the
/var/www/html/ directory of the webserver. We will first download the NYU Tandon
School of Engineering homepage. On the webserver terminal, run

```
cd /var/www/html/
sudo wget -e robots=off --wait 1 -H -p -k http://engineering.nyu.edu/
```

Now do the same for the other four websites.

```
sudo wget -e robots=off --wait 1 -H -p -k http://facebook.com/
sudo wget -e robots=off --wait 1 -H -p -k http://youtube.com/
sudo wget -e robots=off --wait 1 -H -p -k http://reddit.com/
sudo wget -e robots=off --wait 1 -H -p -k http://www.mlb.com/mets
```

Now we have all 5 websites set up on our webserver's html directory.

### Creating Website Fingerprints

Now we will be creating the fingerprints of each website by accessing the website's
homepage that is stored on the webserver from the client node. First we must install
__proxychains__, which we will be using with the wget function to use the Tor network
to access the websites. Another function that we need is __tshark__, which is a
network protocol analyzer similar to tcpdump. On the client terminal, run

```
sudo apt-get -y install proxychains tshark
```

When we create the fingerprints of the websites, we will be creating plots to
visualize our fingerprints to better compare with the client traffic that we will
eventually capture. We will be using __seaborn__, a python visualization library
that is based off the more common matplotlib. On the client terminal, run

```
sudo apt-get -y install python-pip python-dev libfreetype6-dev liblapack-dev libxft-dev gfortran
sudo pip install stem seaborn pandas

```

Next, in order to make our fingerprints, we must run our website packet captures
through a filter, defined by a python script that we have written. This script
takes in the packet trace and filters out unneeded packets and places markers of
different kinds in the trace, defined in the __Characteristics of Packet Traces__
section above. This script will create the fingerprint out of the packet trace.
The python script filter can be accessed on my [Github page](https://github.com/tfukui95/tor-experiment).
On the client terminal, run

```
wget https://raw.githubusercontent.com/tfukui95/tor-experiment/master/make-fingerprint.py
```

to save the script to our client terminal. Next we need to open another client
terminal in order to have two. One terminal will be to access the websites that
are located on the webserver, and then the other terminal will be to listen and
capture the packet trace. After capturing the traffic we will place the trace through
the filter using the python script in order to create the fingerprint.

Let us first test to make sure that everything is working out first. On one of the
client terminals, start listening with tshark by running

```
sudo tshark -i eth1 -n -f "host 192.168.1.100 and tcp and port 5000" -T fields -e frame.len -e ip.src -e ip.dst -E separator=,
```

On the other client terminal access the webserver's default index.php page

```
sudo proxychains wget -p http://webserver/
```

On the client terminal listening on the network using tshark, you should see a comma
separated list, where the rows contain the packet size, the source of the packet,
and the destination of the packet, respectively.

Now we are ready to build the fingerprints of each of the websites. Let us first
start with the first website that we stored on our webserver, which is the NYU
Engineering site. In order to be able to run the packet trace through the filter,
we must save it as a csv file. On the client terminal using tshark, run

```
sudo tshark -i eth1 -n -f "host 192.168.1.100 and tcp and port 5000" -T fields -e frame.len -e ip.src -e ip.dst -E separator=, >engineering.csv
```

On the other client terminal, run

```
proxychains wget -p http://192.168.2.200/engineering.nyu.edu/
```

Now stop the tshark from listening on the network, which will save the captured
traffic into engineering.csv. Now in order to put the file through the filter
using the python script, on one of the client terminals, run

```
python make-fingerprint.py --filename engineering.csv
```

A list of tuples, containing the type of data (whether a data packet or a marker)
and the data itself, will be outputted onto the display. During this process two plots
are created as visuals of the fingerprint for the comparison part of our experiment
later. The plots are saved as a PNG image file, and should be stored somewhere for
later. We can use SCP (Secure Copy Protocol) to save the image from our remote Linux
terminal to our local machine. Go to your GENI slice page, and click Details to
get more information of your client VM.

Open up a local terminal, and go to whichever folder you want to save your
plots to. The SCP command for saving the image to your local machine is the following:

```
scp -P <port_number> <user>@<site_address>:~/fingerprint-plot.png <any_filename.png>
```

Therefore for example in my case, the codes to run will be

```
scp -P 32570 tef243@pc2.instageni.maxgigapop.net:~/fingerprint-plot.png engineeringPlot.png
scp -P 32570 tef243@pc2.instageni.maxgigapop.net:~/fingerprint-plot2.png engineeringPlot2.png
```

The file fingerprint-plot.png contains a plot of incoming and outgoing packets,
as well as the size markers whenever the direction changes. The file fingerprint-plot2.png
contains a plot of just the number markers in its own plot.

Now we must do the same for the other four sites. For Facebook:

```
# On one client terminal
sudo tshark -i eth1 -n -f "host 192.168.1.100 and tcp and port 5000" -T fields -e frame.len -e ip.src -e ip.dst -E separator=, >facebook.csv

# On the other client terminal
proxychains wget -p http://192.168.2.200/facebook.com/

# After stopping tshark, on either client terminal
python make-fingerprint.py --filename facebook.csv

# After the fingerprinting is done, on the local terminal
scp -P 32570 tef243@pc2.instageni.maxgigapop.net:~/fingerprint-plot.png facebookPlot.png
scp -P 32570 tef243@pc2.instageni.maxgigapop.net:~/fingerprint-plot2.png facebookPlot2.png
```

Next for the fingerprint for Youtube:

```
# On one client terminal
sudo tshark -i eth1 -n -f "host 192.168.1.100 and tcp and port 5000" -T fields -e frame.len -e ip.src -e ip.dst -E separator=, >youtube.csv

# On the other client terminal
proxychains wget -p http://192.168.2.200/youtube.com/

# After stopping tshark, on either client terminal
python make-fingerprint.py --filename youtube.csv

# After the fingerprinting is done, on the local terminal
scp -P 32570 tef243@pc2.instageni.maxgigapop.net:~/fingerprint-plot.png youtubePlot.png
scp -P 32570 tef243@pc2.instageni.maxgigapop.net:~/fingerprint-plot2.png youtubePlot2.png
```

Next for the fingerprint for Reddit:

```
# On one client terminal
sudo tshark -i eth1 -n -f "host 192.168.1.100 and tcp and port 5000" -T fields -e frame.len -e ip.src -e ip.dst -E separator=, >reddit.csv

# On the other client terminal
proxychains wget -p http://192.168.2.200/reddit.com/

# After stopping tshark, on either client terminal
python make-fingerprint.py --filename reddit.csv

# After the fingerprinting is done, on the local terminal
scp -P 32570 tef243@pc2.instageni.maxgigapop.net:~/fingerprint-plot.png redditPlot.png
scp -P 32570 tef243@pc2.instageni.maxgigapop.net:~/fingerprint-plot2.png redditPlot2.png
```

Lastly, for the fingerprint for the Mets homepage:

```
# On one client terminal
sudo tshark -i eth1 -n -f "host 192.168.1.100 and tcp and port 5000" -T fields -e frame.len -e ip.src -e ip.dst -E separator=, >mets.csv

# On the other client terminal
proxychains wget -p http://192.168.2.200/www.mlb.com/mets

# After stopping tshark, on either client terminal
python make-fingerprint.py --filename mets.csv

# After the fingerprinting is done, on the local terminal
scp -P 32570 tef243@pc2.instageni.maxgigapop.net:~/fingerprint-plot.png metsPlot.png
scp -P 32570 tef243@pc2.instageni.maxgigapop.net:~/fingerprint-plot2.png metsPlot2.png
```

### Testing the Website Fingerprints

Now that we have our fingerprints for each of the sites, we will be snooping on
the client of our private Tor network and see if we can figure out what site the
client is visiting. The following is our process:

1. Start listening on the client's network
2. Have the client randomly choose one of the 5 sites
3. Capture the traffic that we can see, and create a similar fingerprint plot
as the one that we made for the websites.
4. See if we can determine which site the client visited

Now let us start our experiment. On one client terminal, run

```
sudo tshark -i eth1 -n -f "host 192.168.1.100 and tcp and port 5000" -T fields -e frame.len -e ip.src -e ip.dst -E separator=, >wfpAttack.csv
```

There is a script file on my [Github page](https://github.com/tfukui95/tor-experiment)
called randomSite.sh. Save the script file onto the client VM and then run it

```
wget https://raw.githubusercontent.com/tfukui95/tor-experiment/master/randomSite.sh
bash randomSite.sh
```

Now the process to create the fingerprint of the user's traffic is the same as before,
when we made the fingerprints for the websites. After stopping tshark, on either
client terminal, run

```
python make-fingerprint.py --filename wfpAttack.csv
```

After the fingerprinting is done, on the local terminal, run

```
scp -P 32570 tef243@pc2.instageni.maxgigapop.net:~/fingerprint-plot.png wfpPlot.png
scp -P 32570 tef243@pc2.instageni.maxgigapop.net:~/fingerprint-plot2.png wfpPlot2.png
```

Open up wfpPlot.png and wfpPlot2.png on your local machine, and compare it with the other fingerprints.
See whether it is clear or not which site the client randomly chose to visit. We
notice that for certain sites it is much easier to distinguish from the rest, for
example for the NYU Engineering homepage, we can see that towards the end of the
retrieval of the webpage we see a lot of constant back and forth between client
and server compared to the first half where there are a lot of packets sent in bunches
from the webserver. Other sites are not as easy to distinguish, but looking closely,
we can see that every site's fingerprint has some kind of unique part to it which
differentiates it from the rest of them.

Go back to the client terminal in which you ran the shell script, which should be
waiting for a keyboard input saying "Press any key to see which site the client visited:".
After you arrive upon a guess as to which site the client visited, press any key on
the keyboard to see whether your guess was correct.

This is the end of the experiment portion of the thesis. To expand on this experiment,
feel free to increase the number of sites, clients, marker types, etc. to make the
experiment even more interesting and realistic. Using Wireshark to gain a better
understanding of the packet traces is also recommended. Please refer to the Toy
Experiment in Chapter 3 for more information on using Wireshark.

## References

[1] "Website Fingerprinting in Onion Routing Based Anonymization Networks",
Andriy Panchenko, Lukas Niessen, Andreas Zinnen, [https://www.freehaven.net/anonbib/cache/wpes11-panchenko.pdf](https://www.freehaven.net/anonbib/cache/wpes11-panchenko.pdf)  
[2] "Touching from a Distance: Website Fingerprinting Attacks and Defenses", Xiang
Cai, Xin Cheng Zhang, Brijesh Joshi, Rob Johnson, [http://www3.cs.stonybrook.edu/~xcai/fp.pdf](http://www3.cs.stonybrook.edu/~xcai/fp.pdf)  
[3] "Improved Website Fingerprinting on Tor", Tao Wang, Ian Goldberg, [http://www.cypherpunks.ca/~iang/pubs/webfingerprint-wpes.pdf](http://www.cypherpunks.ca/~iang/pubs/webfingerprint-wpes.pdf)  
