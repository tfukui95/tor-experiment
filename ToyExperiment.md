# Analyzing Anonymous Routing of Network Traffic Using Tor

## Setting Up the Toy Experiment on Tor

The best way to learn about Tor is to create our own private Tor network using
GENI, and to see the functions of Tor on a much smaller and more manageable
scale. By setting up a private Tor network, we will be in control of our own
client, routers, directory server, and web server.

Once we are done setting up the private Tor network, there will be two routes
in which a client's packet can be sent to the web server:

1. Through a direct link between client and web server
2. Through the Tor network

We will be testing both cases to see what kind of information we can see when
listening on different parts of the network. We will be looking for the
following three pieces of information for these tests:

1. Whether we can see the client address
2. Whether can see the web server address
3. Whether we can see the data packet's contents

For both cases, we will be able to see that not all information can be seen at
every part of the network.

Before we begin, please know that the process of setting up the private Tor
network is based partly on an experiment by Liu Fengyun found on this [site](http://liufengyun.chaos-lab.com/prog/2015/01/09/private-tor-network.html).

### Reserving our Topology on GENI

First off, make sure you know the basics of GENI. If not, first complete these two labs:

* [Lab 0: Reserve resources on GENI](http://witestlab.poly.edu/~ffund/el7353/1-reserve-resources.html)
* [Lab 1: Using the Linux shell](http://witestlab.poly.edu/~ffund/el7353/1-using-linux-shell.html)

After creating a slice for this toy experiment, next we must set up our resources.
The following will be the GENI topology for this experiment:

![](https://raw.githubusercontent.com/tfukui95/tor-experiment/master/ToyTopology.png)

We will be needing eight virtual machines (VMs) in total. Choose the Xen VM choice
for the eight VMs, and click on each one and give each a name depending on its
function. Use the above topology as a reference. Next, link them into a network
just like the topology above.

Now we must assign an IP address to each connection between a VM and a link. The
first 16 bits of the IP addresses are the same, which is **192.168**. The last
16 bits depend on the link number, followed by the host number. The following is
the IP address format: **192.168.link_number.host_number.**  The specific
number we assign to each link and host does not matter as long as we remain
constant. However, since the instructions that follow will be based off the
topology above, it is advised to follow the above topology in order to ensure
proper functioning of the private Tor network. To give an example, first click
the link which directly connects the client and the web server VM. Let us give the
number 5 to this link. If we scroll down to the **Interfaces** section, we can
see all of the VMs connected on that link, and that we can change the settings
for each VM, including the IP address of that connection and the Netmask. The
Netmask for each connection is the same, and is **255.255.255.0**. For link 5,
we can see that the host and web server are the VMs connected to this link. If we
look at the topology above, we can see that the host number for the client is 100,
and the host number for the web server is 200. Therefore the IP address that is
to be assigned for the connection from the client to link 5 is **192.168.5.100**
and the IP address for the connection from the web server to link 5 is **192.168.5.200**.
In this way, each of the connections should be assigned IP addresses and Netmask
numbers, using the topology as a guide to which numbers to use.

After each VM and link is set up, we must click the Site, and choose a site to
reserve our resources from. Choose any site that has a green check next to its
name. After choosing this site, scroll all the way down and press *Reserve Resources*.
After the status of adding sources says **Finished**, go back to the slice page
and you will see the resources that we have just added. Time is required in
order to completely reserve the resources, so we must wait for a few moments.
When a VM's reservation is complete, the border of the VM will change from black
to green. When all VM borders are green, meaning that the whole topology is
ready to be used, we will continue on to our next step of installing Tor onto
each VM.

### Installing the Tor Software

To start, we install tor on all of the nodes *except* the web server using the
following steps:

```
sudo sh -c 'echo "deb http://deb.torproject.org/torproject.org trusty main" >> /etc/apt/sources.list'
sudo sh -c 'echo "deb-src http://deb.torproject.org/torproject.org trusty main" >> /etc/apt/sources.list'

sudo gpg --keyserver keys.gnupg.net --recv 886DDD89
sudo gpg --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | sudo apt-key add -

sudo apt-get update
sudo apt-get -y install tor deb.torproject.org-keyring vim curl tor-arm tshark
```

An important point to note here, is that the code to get the repository from
Torproject differs depending on the version of Ubuntu that you are using. In my
case, I am using Ubuntu 14.04. If you are using an older or newer version,
look online for the correct code for your version.

### Setting up the Web Server

On the node that is designated as the web server, set up Apache:

```
sudo apt-get update
sudo apt-get -y install apache2 php5 libapache2-mod-php5
```

Then, we will set up a simple PHP script that returns the client's IP addresses
as the homepage of the web server"

```
sudo rm /var/www/html/index.html
echo '<?php' | sudo tee -a /var/www/html/index.php
echo 'echo "Remote address: " . $_SERVER['REMOTE_ADDR'] . "\n";' | sudo tee -a /var/www/html/index.php
echo 'echo "Forwarded for:  " . $_SERVER['HTTP_X_FORWARDED_FOR'] . "\n";' | sudo tee -a /var/www/html/index.php
echo '?>' | sudo tee -a /var/www/html/index.php
```

Finally, restart the Apache server:

```
sudo /etc/init.d/apache2 restart
```

In order to monitor when someone tries to access the webserver, run:

```
sudo tail -f /var/log/apache2/access.log
```

### Setting up the Directory Authority

Directory authorities help Tor clients learn the addresses of relays that make up the Tor network. Specifically, via the Tor documentation [1]:

> How do clients know what the relays are, and how do they know that they have the right keys for them? Each relay has a long-term public signing key called the "identity key". Each directory authority additionally has a "directory signing key". The directory authorities provide a signed list of all the known relays, and in that list are a set of certificates from each relay (self-signed by their identity key) specifying their keys, locations, exit policies, and so on. So unless the adversary can control a majority of the directory authorities (as of 2012 there are 8 directory authorities), he can't trick the Tor client into using other Tor relays.
>
> How do clients know what the directory authorities are? The Tor software comes with a built-in list of location and public key for each directory authority. So the only way to trick users into using a fake Tor network is to give them a specially modified version of the software.

First, stop any currently running Tor process:

```
sudo /etc/init.d/tor stop
```

In previous attempts, we had trouble using the DataDirectory, because it was
owned by the debian-tor user and group. So we are going to run some commands as
debian-tor.

First, run

```
sudo -u debian-tor mkdir /var/lib/tor/keys
sudo -u debian-tor tor-gencert --create-identity-key -m 12 -a 192.168.1.4:7000 \
            -i /var/lib/tor/keys/authority_identity_key \
            -s /var/lib/tor/keys/authority_signing_key \
            -c /var/lib/tor/keys/authority_certificate
```

and enter a password when prompted. Finally, run

```
sudo -u debian-tor tor --list-fingerprint --orport 1 \
    --dirserver "x 127.0.0.1:1 ffffffffffffffffffffffffffffffffffffffff" \
    --datadirectory /var/lib/tor/
```

The output should say something like:

```
Nov 23 12:27:31.540 [notice] Your Tor server's identity key fingerprint is
'Unnamed 84F349212E57E0E33A324849E290331596BB6217' Unnamed 84F3 4921 2E57 E0E3
3A32 4849 E290 3315 96BB 6217
```

Now we'll create a configuration file for the directory authority. First, get
the two fingerprints:

```
finger1=$(sudo cat /var/lib/tor/keys/authority_certificate  | grep fingerprint | cut -f 2 -d ' ')
finger2=$(sudo cat /var/lib/tor/fingerprint | cut -f 2 -d ' ')
```

Use echo to verify that the finger1 and finger2 variables now contain the fingerprints:

```
echo $finger1
echo $finger2
```

Also, get the hostname, which we will use as the Tor "nickname", with

```
HOSTNAME=$(hostname -s)
```

Then, write the config file with

```
sudo bash -c "cat >/etc/tor/torrc <<EOL
TestingTorNetwork 1
DataDirectory /var/lib/tor
RunAsDaemon 1
ConnLimit 60
Nickname $HOSTNAME
ShutdownWaitLength 0
PidFile /var/lib/tor/pid
Log notice file /var/log/tor/notice.log
Log info file /var/log/tor/info.log
Log debug file /var/log/tor/debug.log
ProtocolWarnings 1
SafeLogging 0
DisableDebuggerAttachment 0
DirAuthority $HOSTNAME orport=5000 no-v2 hs v3ident=$finger1 192.168.1.4:7000 $finger2
SocksPort 0
OrPort 5000
ControlPort 9051
Address 192.168.1.4
DirPort 7000
# An exit policy that allows exiting to IPv4 LAN
ExitPolicy accept 192.168.1.0/24:*

AuthoritativeDirectory 1
V3AuthoritativeDirectory 1
ContactInfo auth0@test.test
ExitPolicy reject *:*
TestingV3AuthInitialVotingInterval 300
TestingV3AuthInitialVoteDelay 20
TestingV3AuthInitialDistDelay 20
EOL"
```


Note: See [2] for background on writing a multi-line file with variables, and
[3] for background on using cat to write a multi-line file to a protected file.

Use

```
sudo cat /etc/tor/torrc
```

to make sure that the correct variables are written to the config file.

Since the router and client config files also need the directory server's
fingerprints in them, we'll generate them on the directory server (which
knows its own fingerprints). We'll download them to the individual router
and client nodes and customize them later.

First, install apache2, in order to write the router config file and store it
on the web

```
sudo apt-get update
sudo apt-get -y install apache2 php5 libapache2-mod-php5
```

Next write the router config file with

```
sudo bash -c "cat >/var/www/html/router.conf <<EOL
TestingTorNetwork 1
DataDirectory /var/lib/tor
RunAsDaemon 1
ConnLimit 60
ShutdownWaitLength 0
PidFile /var/lib/tor/pid
Log notice file /var/log/tor/notice.log
Log info file /var/log/tor/info.log
Log debug file /var/log/tor/debug.log
ProtocolWarnings 1
SafeLogging 0
DisableDebuggerAttachment 0
DirAuthority $HOSTNAME orport=5000 no-v2 hs v3ident=$finger1 192.168.1.4:7000 $finger2

SocksPort 0
OrPort 5000
ControlPort 9051

# An exit policy that allows exiting to IPv4 LAN
ExitPolicy accept 192.168.1.0/24:*
ExitPolicy accept 192.168.2.0/24:*
ExitPolicy accept 192.168.3.0/24:*
ExitPolicy accept 192.168.4.0/24:*
EOL"
```

This config file created on the directory authority creates a generic config
file for all routers, which can then be copied over to a router. The file is
saved in `/var/www/html/router.conf` and can be seen by

```
sudo cat /var/www/html/router.conf
```

Then, write the client config file with

```
sudo bash -c "cat >/var/www/html/client.conf <<EOL
TestingTorNetwork 1
DataDirectory /var/lib/tor
RunAsDaemon 1
ConnLimit 60
ShutdownWaitLength 0
PidFile /var/lib/tor/pid
Log notice file /var/log/tor/notice.log
Log info file /var/log/tor/info.log
Log debug file /var/log/tor/debug.log
ProtocolWarnings 1
SafeLogging 0
DisableDebuggerAttachment 0
DirAuthority $HOSTNAME orport=5000 no-v2 hs v3ident=$finger1 192.168.1.4:7000 $finger2

SocksPort 9050
ControlPort 9051
EOL"
```

This config file created on the directory authority creates a generic config
file for a client. The file is saved in `/var/www/html/client.conf` and can be seen by

```
cat /var/www/html/client.conf
```


Finally, start Tor with

```
sudo /etc/init.d/tor start
```

From running

```
sudo cat /var/log/tor/debug.log | grep "Trusted"
```

to search the log file, we see a line

```
Nov 09 11:03:02.000 [debug] parse_dir_authority_line(): Trusted 100 dirserver
at 192.168.1.4:7000 (CA36BEB3CDA5028BDD7B1E1F743929A81E26A5AA)
```

which is promising - it seems to indicated that we are using our directory
authority at 192.168.1.4 (the current host).

### Setting up a Router

First, stop any currently running Tor process:

```
sudo /etc/init.d/tor stop
```

Generate fingerprints as the debian-tor user with:

```
sudo -u debian-tor tor --list-fingerprint --orport 1 \
    --dirserver "x 127.0.0.1:1 ffffffffffffffffffffffffffffffffffffffff" \
    --datadirectory /var/lib/tor/
```

The output should say something like:

```
Nov 23 12:34:00.137 [notice] Your Tor server's identity key fingerprint is
'Unnamed D2EB9948027BF5795FCA85182869FBFAA7C15B4C' Unnamed D2EB 9948 027B F579
5FCA 8518 2869 FBFA A7C1 5B4C
```

Now, download the generic router config file that we created on the
directory server:

```
sudo wget -O /etc/tor/torrc http://directoryserver/router.conf
```

Now, we'll add some extra config settings that are different on
each router node: the nickname and the address(es).

Add the nickname and address(es) with

```
HOSTNAME=$(hostname -s)
echo "Nickname $HOSTNAME" | sudo tee -a /etc/tor/torrc
ADDRESS=$(hostname -I | tr " " "\n" | grep "192.168")
for A in $ADDRESS; do
  echo "Address $A" | sudo tee -a /etc/tor/torrc
done
```

Now, if you look at the contents of the config file on the router:
```
sudo cat /etc/tor/torrc
```

you should see a couple of lines like

```
Nickname router1
Address 192.168.1.2
```

at the end.

Finally, start the Tor service on the router node with

```
sudo /etc/init.d/tor restart
```

On the directory server, check if it has been made aware of the newly
added router by searching for its nickname in the log file. For example,
if the router's nickname is `relay1`, check that it has been recognized
on the directory server with

```
sudo cat /var/log/tor/debug.log | grep "relay1"
```

You should see some output like

```
Nov 23 13:06:29.000 [debug] router_parse_list_from_string(): Read router
'$D2EB9948027BF5795FCA85182869FBFAA7C15B4C~router1 at 192.168.1.2', purpose 'general'
Nov 23 13:06:29.000 [debug] dirserv_single_reachability_test(): Testing reachability
of router1 at 192.168.1.2:5000.
Nov 23 13:06:29.000 [info] dirserv_add_descriptor(): Added descriptor from 'router1'
(source: 192.168.1.2): Descriptor accepted.
Nov 23 13:06:29.000 [info] dirserv_orconn_tls_done(): Found router
$D2EB9948027BF5795FCA85182869FBFAA7C15B4C~router1 at 192.168.1.2 to be reachable
at 192.168.1.2:5000. Yay.
```

Repeat all of the above commands for all of the router nodes that you create.

### Setting up a Client

First, stop any currently running Tor process:

```
sudo /etc/init.d/tor stop
```

Then, generate fingerprints as the debian-tor user with:

```
sudo -u debian-tor tor --list-fingerprint --orport 1 \
    --dirserver "x 127.0.0.1:1 ffffffffffffffffffffffffffffffffffffffff" \
    --datadirectory /var/lib/tor/
```

The output should say something like:

```
Nov 23 13:25:30.877 [notice] Your Tor server's identity key fingerprint is
'Unnamed 4BD9274359B639B5E812913A9B1962BD84BABFFF' Unnamed 4BD9 2743 59B6 39B5
E812 913A 9B19 62BD 84BA BFFF
```

Download the client config file (that we created on the directory
server) to the default Tor config file location with:

```
sudo wget -O /etc/tor/torrc http://directoryserver/client.conf
```

Add the nickname and address(es) with

```
HOSTNAME=$(hostname -s)
echo "Nickname $HOSTNAME" | sudo tee -a /etc/tor/torrc
ADDRESS=$(hostname -I | tr " " "\n" | grep "192.168")
for A in $ADDRESS; do
  echo "Address $A" | sudo tee -a /etc/tor/torrc
done
```

Finally, start the Tor service on the client node with

```
sudo /etc/init.d/tor restart
```

## Testing the Private Tor Network

In order to clearly see the benefits of using the Tor network, we must first
run a test to see what information can be seen by a hacker when not using Tor.

### Testing the Network Without Using Tor

In order to access the webserver without going through the Tor network, we
simply run

```
curl http://webserver/
```

and verify that the server returns the client's IP address. You should see
something like

```
Remote address: 192.168.5.100
Forwarded for:
```

From this we can see how that the webserver is telling us that the VM that
accessed the webserver is the client, which shows that the client and webserver
are directly communicating with each other.

Next we will be using Tcpdump to watch the traffic on the network. We want
Tcpdump to both display the output to screen while also saving the output to a
file. The following is the format

```
sudo tcpdump -s 1514 -i any 'port <port_num>' -U -w - | tee <name_file>.pcap | tcpdump -nnxxXSs 1514 -r -
```

where <port_num> is the specific port number to access, and <name_file> is the
name that you want to save the file as.

Since we are not using the Tor network, we will be listening on port 80 which
is the most common HTTP port. Have two client terminals opened, and on one,
start listening through port 80 by running

```
sudo tcpdump -s 1514 -i any 'port 80' -U -w - | tee clientnotor.pcap | tcpdump -nnxxXSs 1514 -r -
```

On the web server terminal also listen through port 80 by running

```
sudo tcpdump -s 1514 -i any 'port 80' -U -w - | tee servernotor.pcap | tcpdump -nnxxXSs 1514 -r -
```

On the other client terminal, access the webserver by running

```
curl http://webserver/
```

On both terminals that are listening on the network, we should see something
like

```
IP 192.168.5.100.38826 > 192.168.5.200.80
IP 192.168.5.200.80 > 192.168.5.100.38826
```

which shows how we can see that the client and webserver are communicating
directly with each other. On the right-hand side of the output we should see
something like

```
MGET./.HTTPS/1.1..User-Agent:.curl/7.35.0..Host:.webserver..Accept:. */*
```

which is a request to access the webserver, and something like

```
Content-Length:.47..Content-Type:.text/html....Remote.address:.192.168.5.100.Forwarded.for:...
```

which is the output of the curl command that we ran earlier. This shows how we
can see exactly what traffic they are passing to each other. We can conclude how
communicating only through HTTP allows a person spying on this network to see
who is communicating with who, and what specifically is being communicated. This
form is communication is very risky and prone to getting your information stolen.

### Testing the Network Using Tor

Now we will test the same curl experiment of accessing the web server, now
through the Tor network. Then we will compare the results with when we do not
use Tor.

First we need to find the exit relay that is being used in the Tor network,
which serves as the relay that sends the data packet to the webserver. In order
to do this we run

```
curl -x socks5://127.0.0.1:9050/ http://webserver/
```

and verify that when using the Tor network (through the SOCKS proxy),
the server does not know the client's IP address; it returns the IP address
of the exit relay. You should see something like

```
Remote address: 192.168.2.1
Forwarded for:
```

Clearly the returned address is not the client's IP address, but the IP
address of a Tor relay that we set up. This relay is the exit relay of the
circuit that is being used.

We can see who and when someone accesses the webserver by running

```
sudo su
tail -f /var/log/apache2/access.log
```

and then running the curl command again.

Our next step is to figure out which Tor circuit is being used to access the
webserver. This can be done using Tor Arm (anonymizing relay monitor), a program
which serves as a terminal status monitor of Tor [4]. Arm provides useful
statistics such as bandwidth, cpu, and memory usage, as well as known
connections, and the Tor configuration file.

First we run Arm on each of the Tor relays including the client and the directory
server.

```
sudo -u debian-tor arm
```

We can see a running display of bandwidth, cpu, and memory usage. On the client's
Arm window, if we flip to the second page we can see the Tor circuits that are
available to pass traffic. In order to figure out which circuit is being used,
we need to pass traffic through the network and observe which Tor relays are
also passing that same traffic. To do this, we will generate a large file on the
webserver, to be downloaded by the client to allow enough time for us to observe
each relay's Arm window to see the passing traffic.

Now we will generate a large file from the webserver. On the webserver run

```
sudo truncate -s 2G /var/www/html/large
```

Now from the client terminal we will download a large file from the webserver

```
curl -x socks5://127.0.0.1:9050/ -s http://webserver/large > /dev/null
```

There will be no output on the screen for the client as it is downloading.
However on the other client terminal you should observe that the client is
downloading a file. Other than the Arm window of the client, you should notice a
similar pattern in three other relay terminals. These three relays are the
relays being used in the Tor network to access the website and through which
the file is being downloaded. In order to see which circuit specifically is
being used, move to the second page of the Arm window of the client to see a
list of connections that the client knows. Since we found out which relay is
serving as the exit node before, we should be able to see the circuit that lists
that information. Make sure that the other two relays are also listed as the
guard and middle relays. This circuit is the one that is being used to pass
the client's traffic to the webserver, and vice-versa.


### Using Tcpdump to Watch Traffic

We will again be using tcpdump to listen to the network at different locations.
We will require three terminals for the clients for this part. On one, run

```
sudo tcpdump -s 1514 -i any 'port 9050' -U -w - | tee client9050.pcap | tcpdump -nnxxXSs 1514 -r -
```

to watch the traffic that is going through the SOCKS proxy port 9050, and then
save what it sees in a pcap file called client9050.pcap. The SOCKS proxy is the
proxy that is used for the client and the onion proxy to communicate with each
other. This communication is a loop-back interface, in other words the
communication occurs in the local ethernet. On another client terminal run

```
sudo tcpdump -s 1514 -i any 'port 5000' -U -w - | tee client5000.pcap | tcpdump -nnxxXSs 1514 -r -
```

to watch the traffic through port 5000, which is the port to listen on the Tor
network. This would mean that we would be listening on any traffic that is
being transferred from the client to the Tor network. Specifically, this
communication would be between the client and the entry relay that is being
used when the traffic enters the Tor network.

Next on each relay that is being used in the circuit, run

```
sudo tcpdump -s 1514 -i any 'port 5000' -U -w - | tee $(hostname -s).pcap | tcpdump -nnxxXSs 1514 -r -
```

where **$(hostname -s)** will be converted to the name of the specific relay
that you are working with. For example, if using tcpdump on relay1, the file
that tcpdump will write to will be relay1.pcap. This tcpdump function will
watch the traffic that is going through the OR port 5000, and then save what it
sees in a pcap file.

We must perform one extra step for the exit relay, and that is to open another
terminal and have the relay listen on port 80, which is the most commonly used
port for HTTP. On the new terminal run

```
sudo tcpdump -s 1514 -i any 'port 80' -U -w - | tee exitrelay.pcap | tcpdump -nnxxXSs 1514 -r -
```

to start listening on the network through port 80.

Lastly we must also set up the web server to have it listen for traffic as well.
On the web server terminal run

```
sudo tcpdump -s 1514 -i any 'port 80' -U -w - | tee webserver.pcap | tcpdump -nnxxXSs 1514 -r -
```

to start listening for traffic on port 80.

Now at this point we should have seven terminals listening on a network. These
terminals are the two client terminals, terminals for the three ORs being used
in the circuit, an extra exit relay terminal, and the web server terminal.

Next on the third client terminal, we run

```
curl -x socks5://127.0.0.1:9050/ http://webserver/
```

to access the webserver. Since we are using the Tor network to access the site,
the three ORs must have seen some kind of traffic passing through it. Now let
us take a look at what the client and each OR saw. Stop the tcpdump process
with Ctrl^C. When we stop tcpdump, a file is created with the traffic that was
seen passing through. If you want to access the saved file to see the traffic
on Wireshark's interface, follow the steps in the following section. Otherwise,
as we listen on the network, the traffic that we can see will be outputted on
the display of each terminal.

## Summary of Toy Experiment

From using tcpdump when using and not using Tor, there is a clear difference
in the information that we can and cannot see at each node. The following table
summarizes what can be seen when listening on a network that doesn't use Tor:

|      | Client Address    | Web Server Address     | Packet Contents     |
| :------------- | :------------- | :------------- | :------------- |
| **Client Port 80**     | Yes       | Yes    | Yes     |
| **Web Server Port 80** | Yes       | Yes    | Yes     |
| **Middle-Man Port 80** | Yes       | Yes    | Yes     |

From this table, we can see then when not using Tor, and using the direct link
between the client and web server, all information can be seen. Clearly we know
that the client and the web server knows who it is communicating with, and the
packet contents that are being sent. However, what is dangerous is that any
attacker that is listening on the same network can see all the information that
both ends of the network can also see. This leads to easy spying, stealing of
information and privacy, and may lead to a virus since the attacker knows your
location and what site you visit.

This next table summarizes the same key points, but for when we communicate
while using the Tor network:

|      | Client Address    | Web Server Address     | Packet Contents     |
| :------------- | :------------- | :------------- | :------------- |
| **Client Port 9050**     | Yes       | No    | Yes     |
| **Client Port 5000**  | Yes       | No    | No    |
| **Entry Relay Port 5000** | Yes       | No   | No     |
| **Middle Relay Port 5000**     | No       | No    | No    |
| **Exit Relay Port 5000** | No       | No    | No    |
| **Exit Relay Port 80** | No      | Yes    | Yes     |
| **Web Server Port 80** | No      | Yes    | Yes     |

In order to better understand this table, let us look at each column one at a
time. The leftmost column is arranged chronologically in the order which a
packet gets transmitted to the web server. First we look at the client address
column, where we see that the client address can be seen in the beginning, where
the entry relay is the last node which knows the client address. The reason why
the change occurs here is because this is the point where the packet enters the
Tor network. Inside the Tor network, including the entry and exit relays, each
relay only knows who sent it the packet and who to send the packet to next.
Therefore the entry relay gets the packet from the client, and knows to send it
to the middle relay, but once it gets to the middle relay, the middle relay only
knows that it got the packet from the entry relay and does not know anything
about the client who originally sent the packet. Therefore from that point the
client address is no longer known.

Taking a look at the next column which is the web server address, we can see
that the web server address is not known towards the beginning, until it reaches
the exit relay and while listening through port 80. The reason why the web
server address is not known until this point is due to the encryption that is
done by the onion proxy at the beginning. When the packet reaches the exit relay,
the exit relay decrypts the last layer of encryption and at that point, the
location of the webserver is first known. Since the exit relay is responsible for
sending the packet to the web server, who can't decrypt any kind of Tor
encryption, the web server address as well as the packet contents are unencrypted.

The last column of the table is the packet contents column, which tells us who
sees encrypted or unencrypted packet information. We can see that the nodes
which can see the unencrypted packet data are the nodes at the beginning and the
end of the circuit. In order words, the nodes that are inside the Tor network
cannot see the packet contents, because the information is encrypted while
traveling inside the Tor network, and the ends of the circuit cannot decrypt
Tor encryption so the information must be unencrypted at the ends.

One of the most important conclusions to arrive upon from this experiment is that
when using the Tor network, there is no one node that knows the whole mapping
of the circuit. Therefore even if one node, say for example one of the Tor relays
gets taken control over, the relay only knows who gave it the packet and who it
needs to send it to, and nothing else. As long as no too many nodes get taken
over, anonymity will definitely stay intact. This is the power of Tor, in being
able to cloak client and web server communication as well as their locations and
actual packet contents while the packet traverses through the Tor network.

## Other Methods to See Information about the Network

There are other methods in which we can see the information that is being
passed along the circuit of the Tor network. However these methods require
additional installations of programs, and will be listed in this section as an
additional resource.

One such method to get more information about circuits available and about which
exit relay is used for each connection, is to use a couple of Python utility
scripts.

Another method is an addition to tcpdump, which allows for a better and more
organized window to analyze the packets that are being passed along the Tor
network. This method requires Wireshark and winSCP. Wireshark is a software that
can read in a file written by tcpdump, and displays the traffic very neatly to
allow better observation of the data. WinSCP is a program for Windows users,
that is going to be used to access the tcpdump files that are saved on the VMs,
and to copy it to our local Desktop, so that we can open the file with Wireshark.

### Using Python Utility Scripts

First, install some prerequisites:

```
sudo apt-get update
sudo apt-get -y install python-pip
sudo pip install stem
```

Then, you can download the utility scripts with

```
wget https://raw.githubusercontent.com/tfukui95/tor-experiment/master/utilities/exit-relay.py
wget https://raw.githubusercontent.com/tfukui95/tor-experiment/master/utilities/list-circuits.py
```

To see what circuits your Tor client is currently aware of, run

```
sudo python list-circuits.py
```

To see what exit relay is associated with an outgoing connection, you'll
need two terminals open to the client node. On one, run

```
sudo python exit-relay.py
```

to start monitoring. On another, make an outgoing connection with

```
curl -x socks5://127.0.0.1:9050/ http://webserver/                              
```

and in the first terminal, look for a message like

```
Exit relay for our connection to 192.168.2.1:80
  address: 192.168.1.3:5000
  fingerprint: B1A2C989985CD3C95C0D6C17B0A64A38007F90FB
  nickname: router3
  locale: ??
```

### Setting up Wireshark and WinSCP

Wireshark can be downloaded from the company's [homepage](https://www.wireshark.org/).
Besides downloading and installing the software, there is no often configuration
necessary.

WinSCP can also be downloaded from the company's [homepage](https://winscp.net/eng/download.php).
After installation, we open the application, and immediately a login window
comes up. To login to a specific VM, we must have certain information available,
which can be found on GENI, in the Details page of your slice. Choose **SCP** for
File Protocol. The Host name is the information after the @ symbol used for
logging into each VM, followed by the port number. Your username is the same as
the username before the @ symbol. For the password, we must use our ssh key as
an authentication method. Click "Advanced", followed by "Authentication" under
SSH. Under Authentication Parameters, click Private Key File, and browse to
your location of your ssh key. Once you add the key, you will be asked to convert
your key to PuTTY format because winSCP only supports PuTTY. Go ahead and convert
the key, and now you can save your login info of your VM, to allow faster login
the next time.

## Notes

Before restarting Tor, you must kill the current Tor process first, and then
restart Tor.

```
sudo pkill -9 tor
sudo /etc/init.d/tor restart
```

It is good practice to restart Tor whenever you haven't used the Tor network
for a few hours or so, in order to recreate the circuits.


To run the Tor monitor, use

```
sudo -u debian-tor arm
```

Use the left and right arrow keys to switch between different screens.
Use `q` to quit.


## References
[1] "Tor FAQ - Key Management" [https://www.torproject.org/docs/faq#KeyManagement](https://www.torproject.org/docs/faq#KeyManagement)  
[2] "How do you write multiple line configuration file using BASH, and use variables on multiline?" YumYumYum, Stack Overflow,  [http://stackoverflow.com/questions/7875540/how-do-you-write-multiple-line-configuration-file-using-bash-and-use-variables](http://stackoverflow.com/questions/7875540/how-do-you-write-multiple-line-configuration-file-using-bash-and-use-variables)  
[3] "sudo cat << EOF > File doesn't work, sudo su does" iamauser, Stack Overflow, [http://stackoverflow.com/questions/18836853/sudo-cat-eof-file-doesnt-work-sudo-su-does](http://stackoverflow.com/questions/18836853/sudo-cat-eof-file-doesnt-work-sudo-su-does)  
[4] "Arm (Project Page)" [https://www.torproject.org/projects/arm.html.en](https://www.torproject.org/projects/arm.html.en)  
[5] "How can I have tcpdump write to file and standard output the appropriate data." Stack Overflow, [http://stackoverflow.com/questions/25603831/how-can-i-have-tcpdump-write-to-file-and-standard-output-the-appropriate-data](http://stackoverflow.com/questions/25603831/how-can-i-have-tcpdump-write-to-file-and-standard-output-the-appropriate-data)  
