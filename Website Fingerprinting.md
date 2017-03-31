# Implementation of Website Fingerprinting on GENI

## Understanding Website Fingerprinting Thoroughly

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

### Method of Cross Validation

For a closed-world data set, where the data set size is small, a process called
cross validation is used in data mining to make the results more meaningful.
The process is described in the paper by Panchenko, et al. [1]

>  the data is split into n evenly large parts, the folds. Then, the entire process
of training and testing is repeated n times, using one of the n folds as test data
and the remaining n − 1 folds as training data in turn. The results are averaged
and therefore more solid and meaningful. In this paper, n is set to 10 with 2
instances per fold and per class. Additionally, the so-called stratification is
used, which ensures that the instances within a class are represented as balanced
as possible in each fold. The entire procedure is called ten-fold stratified
cross-validation.

An important reason for performing cross validation is so that training instances
are not collected from the same circuit that is used to collect test instances [3].
For the case of our experiment on GENI, we will not be performing cross validation.

### Method of Packet Classification

Herrmann et al. introduces the application of support vector machines (SVM) that
are used in data mining for classification accuracy. The main idea of using SVM's
is the classification of each instance or packet containing webpage details is
treated as a vector [1]. The process involves placing a hyperplane in the vector
space to distinguish between different kinds of vectors. When vectors are not
able to be separated linearly, a technique called the kernel trick is employed,
where the vector space is brought to a higher dimension so that a hyperplane
can be placed again. The whole process behind SVM is quite complicated, and
thus will not be covered here. Those who would like further information are
recommended _An Introduction to Support Vector Machines and other kernel-based
learning methods_ written by N. Christianini and J. Shawe-Taylor.

Some packets found in a traffic stream can be superfluous and may only reduce
performance of the traffic analysis. TCP ACK packets which are acknowledgement
packets are known to reduce performance due to its repetitiveness of being sent
after every packet. This would make all traces seem very similar with all of the
ACKs, therefore these are removed. Most ACK packets are 40 or 52 bytes, so these
are filtered out.

Every 100 cells, a circuit-level SENDME cell is sent [3]. Similar to ACK cells,
these cells do not provide any useful information and thus should be filtered
out to improve performance. Another factor that is taken into account is that Tor
cells are sent in 512-byte sizes, therefore the packets are rounded up to a size
that is a multiple of 600 and are classified accordingly. For our experiment on GENI,
we will not be doing any packet classification for data mining.

## Setting up the Website Fingerprinting experiment

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
the script files on my Github. To setup the directory server, go to the directory
server VM and run

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
sudo wget -p -k http://engineering.nyu.edu/
```

Now do the same for the other four websites.

```
sudo wget -p -k http://facebook.com/
sudo wget -p -k http://youtube.com/
sudo wget -p -k http://reddit.com/
sudo wget -p -k https://www.mlb.com/mets
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
sudo apt-get -y install python-pip python-scipy python-pandas
sudo pip install seaborn stem

```

Next, in order to make our fingerprints, we must run our website packet captures
through a filter, defined by a python script that we have written. This script
takes in the packet trace and filters out unneeded packets and places markers of
different kinds in the trace, defined in the __Characteristics of Packet Traces__
section above. This script will create the fingerprint out of the packet trace.
The python script filter can be accessed on my Github page. On the client terminal,
run

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






```
sudo apt-get -y install python-pip
sudo pip install stem

wget https://raw.githubusercontent.com/tfukui95/tor-experiment/master/make-fingerprint.py

sudo python make-fingerprint.py
```

No tor
```
sudo tcpdump -s 1514 -i any 'port 80' -U -w - | tee clientnotor.pcap | tcpdump -nnxxXSs 1514 -r -
scp -P 30522 tef243@pc1.instageni.iu.edu:~/clientnotor.pcap .
```

With Tor
```
sudo tcpdump -s 1514 -i any 'port 5000' -U -w - | tee clienttor.pcap | tcpdump -nnxxXSs 1514 -r -
scp -P 30522 tef243@pc1.instageni.iu.edu:~/clienttor.pcap .
```

```
scp -P 32570 make-fingerprint.py tef243@pc2.instageni.maxgigapop.net:~/
```


## References

[1] "Website Fingerprinting in Onion Routing Based Anonymization Networks",
Andriy Panchenko, Lukas Niessen, Andreas Zinnen, [https://www.freehaven.net/anonbib/cache/wpes11-panchenko.pdf](https://www.freehaven.net/anonbib/cache/wpes11-panchenko.pdf)  
[2] "Touching from a Distance: Website Fingerprinting Attacks and Defenses", Xiang
Cai, Xin Cheng Zhang, Brijesh Joshi, Rob Johnson, [http://www3.cs.stonybrook.edu/~xcai/fp.pdf](http://www3.cs.stonybrook.edu/~xcai/fp.pdf)  
[3] "Improved Website Fingerprinting on Tor", Tao Wang, Ian Goldberg, [http://www.cypherpunks.ca/~iang/pubs/webfingerprint-wpes.pdf](http://www.cypherpunks.ca/~iang/pubs/webfingerprint-wpes.pdf)  
