# Setting Up Toy Experiment on Tor

## Reserve our topology on GENI



## Install Tor software

To start, we installed tor on all of the nodes _except_ the web server
using the following steps:

```
sudo sh -c 'echo "deb http://deb.torproject.org/torproject.org trusty main" >> /etc/apt/sources.list'
sudo sh -c 'echo "deb-src http://deb.torproject.org/torproject.org trusty main" >> /etc/apt/sources.list'

sudo gpg --keyserver keys.gnupg.net --recv 886DDD89
sudo gpg --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | sudo apt-key add -

sudo apt-get update
sudo apt-get -y install tor deb.torproject.org-keyring vim curl tor-arm
```
## Set up web server

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

## Bring up a directory authority

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
Nov 23 12:27:31.540 [notice] Your Tor server's identity key fingerprint is 'Unnamed 84F349212E57E0E33A324849E290331596BB6217'
Unnamed 84F3 4921 2E57 E0E3 3A32 4849 E290 3315 96BB 6217
```

Now we'll create a config file for the directory authority. First, get the two fingerprints:

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


Note: See [2] for background on writing a multi-line file with variables, and [3] for background on using cat to write a multi-line file to a protected file.

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
Nov 09 11:03:02.000 [debug] parse_dir_authority_line(): Trusted 100 dirserver at 192.168.1.4:7000 (CA36BEB3CDA5028BDD7B1E1F743929A81E26A5AA)
```

which is promising - it seems to indicated that we are using our directory authority at 192.168.1.4 (the current host).

## Bring up a router

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
Nov 23 12:34:00.137 [notice] Your Tor server's identity key fingerprint is 'Unnamed D2EB9948027BF5795FCA85182869FBFAA7C15B4C'
Unnamed D2EB 9948 027B F579 5FCA 8518 2869 FBFA A7C1 5B4C
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
Nov 23 13:06:29.000 [debug] router_parse_list_from_string(): Read router '$D2EB9948027BF5795FCA85182869FBFAA7C15B4C~router1 at 192.168.1.2', purpose 'general'
Nov 23 13:06:29.000 [debug] dirserv_single_reachability_test(): Testing reachability of router1 at 192.168.1.2:5000.
Nov 23 13:06:29.000 [info] dirserv_add_descriptor(): Added descriptor from 'router1' (source: 192.168.1.2): Descriptor accepted.
Nov 23 13:06:29.000 [info] dirserv_orconn_tls_done(): Found router $D2EB9948027BF5795FCA85182869FBFAA7C15B4C~router1 at 192.168.1.2 to be reachable at 192.168.1.2:5000. Yay.
```

Repeat all of the above commands for all of the router nodes that you create.

## Bring up a client

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
Nov 23 13:25:30.877 [notice] Your Tor server's identity key fingerprint is 'Unnamed 4BD9274359B639B5E812913A9B1962BD84BABFFF'
Unnamed 4BD9 2743 59B6 39B5 E812 913A 9B19 62BD 84BA BFFF
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

To test, run

```
curl http://webserver/
```

and verify that the server returns the client's IP address.

Next, run

```
curl -x socks5://127.0.0.1:9050/ http://webserver/
```

and verify that when using the Tor network (through the SOCKS proxy),
the server does not know the client's IP address; it returns the IP address
of one of the exit nodes.

## Testing the Private Tor Network
### Using Python Utility Scripts
To get more information about circuits available and about which exit relay
is used for each connection, we can use a couple of Python utility scripts.

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
### Using Tor Arm
Another method of figuring out which Tor circuit is being used to access a site
is by using Tor Arm (anonymizing relay monitor), a program which is serves as a
terminal status monitor of Tor [4]. Arm provides useful statistics such as
bandwidth, cpu, and memory usage, as well as known connections, and the tor
configuration file.

First run

```
curl -x socks5://127.0.0.1:9050/ http://webserver/
```

to see which Tor relay is being used as the exit node to access the webserver.

Next, run Arm on each of the Tor relays including the client and the directory
server. Open up a new terminal for running Arm on the client.

```
sudo -u debian-tor arm
```

We can see a running display of bandwidth, cpu, and memory usage. Now we will
generate a large file from the webserver. On the webserver run

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
guard and middle relays.


## Finding out More Information About the Network

Now that we were able to figure out which circuit the onion proxy (OP) is using
to send the client's traffic to its destination, now let's try to see what kind
of information can be seen at each step of the way. In order to do this, we will
use a combination of tcpdump, Wireshark and winSCP. Tcpdump is a built-in linux
function used to watch traffic on a specified network interface. Wireshark is a
software that can read in a file written by tcpdump, and displays the traffic
very neatly to allow better observation of the data. WinSCP is a program for
Windows, that is going to be used to access the tcpdump files that are saved
on the VMs, and to copy it to our local Desktop, so that we can open the file
with Wireshark.

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

### Using Tcpdump to Watch Traffic
First we must figure out which Tor circuit is being used, using the method shown
in the Tor-Arm section above.

We will require two terminals for the clients for this part. On one, run

```
sudo tcpdump -nnxxXSs 1514 -i any 'port 9050' -w client.pcap
```

to watch the traffic that is going through the SOCKS proxy port 9050, and then
save what it sees in a pcap file called client.pcap.

Next on each relay that is being used in the circuit, run

```
sudo tcpdump -nnxxXSs 1514 -i any 'port 5000' -w relay#.pcap
```

where **#** is to be replaced with the number of the specific relay
that you are working with. For example, if using tcpdump on relay1, the file
that tcpdump will write to will be relay1.pcap. This tcpdump function will
watch the traffic that is going through the OR port 5000, and then save what it
sees in a pcap file.

We must perform one extra step for the exit relay, and that is to open another
terminal and have the relay listen on port 80, which is the most commonly used
port for HTTP. On the new terminal run

```
sudo tcpdump -nnxxXSs 1514 -i any 'port 80' -w exitrelay.pcap
```

To start listening on the network through port 80.

Lastly we must also set up the web server to have it listen for traffic as well.
On the web server terminal run

```
sudo tcpdump -nnxxXSs 1514 -i any 'port 80' -w webserver.pcap
```

to start listening for traffic on port 80.

Now at this point we should have six terminals listening on a network. These
five terminals are the client, the three ORs being used in the circuit, an extra
exit relay terminal, and the web server.

Next on the second client terminal, we run

```
curl -x socks5://127.0.0.1:9050/ http://webserver/
```

to access the webserver. Since we are using the Tor network to access the site,
the three ORs must have seen some kind of traffic passing through it. Now let
us take a look at what the client and each OR saw. Stop the tcpdump processing
with Ctrl^C. When we stop tcpdump, a file is created with the traffic that was
seen passing through. Through winSCP, access each of the VMs that was listening
on the network for Tor traffic. Find the pcap file that was saved, and download
that file to your Desktop. Now open the files on Wireshark.


###To Add
sudo tcpdump -s 1514 -i any 'port 5000' -U -w - | tee testfile2.pcap | tcpdump -nnxxXSs 1514 -r -

stackoverflow: how can i have tcpdump write to file and standard output the
appropriate data.


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
