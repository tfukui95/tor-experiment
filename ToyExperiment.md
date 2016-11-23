# Setting Up Toy Experiment on Tor

For debugging, we would like to put up a working Tor network in three stages:

1. Configure one node to act as a directory server. Move on to the next step only when it runs successfully with a config file that tells it to act as a directory server.
2. Configure one node to act as a relay and use the node from the previous step as the directory server. Move on to the next step only when it runs successfully with a config file that tells it to use that directory server.
3. Configure one node to act as a client and contact the relay from the previous step.

To start, we installed tor on all three of those nodes using the following steps:

```
sudo sh -c 'echo "deb http://deb.torproject.org/torproject.org trusty main" >> /etc/apt/sources.list'
sudo sh -c 'echo "deb-src http://deb.torproject.org/torproject.org trusty main" >> /etc/apt/sources.list'

sudo gpg --keyserver keys.gnupg.net --recv 886DDD89
sudo gpg --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | sudo apt-key add -

sudo apt-get update
sudo apt-get -y install tor deb.torproject.org-keyring vim apache2 curl
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

In previous attempts, we had trouble using the DataDirectory, because it was owned by the debian-tor user and group. So we are going to run some commands as debian-tor. First, open a Bash shell running as the debian-tor user with:

```
sudo -u debian-tor bash
```

Your prompt should now show that you are the debian-tor user. Then, run

```
mkdir /var/lib/tor/keys
tor-gencert --create-identity-key -m 12 -a 192.168.1.4:7000 \
            -i /var/lib/tor/keys/authority_identity_key \
            -s /var/lib/tor/keys/authority_signing_key \
            -c /var/lib/tor/keys/authority_certificate \
```

and enter a password when prompted. Finally, run

```
tor --list-fingerprint --orport 1 \
    --dirserver "x 127.0.0.1:1 ffffffffffffffffffffffffffffffffffffffff" \
    --datadirectory /var/lib/tor/
```

The output should say something like:

```
Nov 09 10:55:07.491 [notice] Your Tor server's identity key fingerprint is 'Unnamed CA36BEB3CDA5028BDD7B1E1F743929A81E26A5AA'
Unnamed CA36 BEB3 CDA5 028B DD7B 1E1F 7439 29A8 1E26 A5AA
```

After this step, run

```
exit
```

to go back to your regular (user-owned) shell.

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

Then, write the config file with

```
sudo bash -c "cat >/etc/tor/torrc <<EOL
TestingTorNetwork 1
DataDirectory /var/lib/tor
RunAsDaemon 1
ConnLimit 60
Nickname RS4
ShutdownWaitLength 0
PidFile /var/lib/tor/pid
Log notice file /var/log/tor/notice.log
Log info file /var/log/tor/info.log
Log debug file /var/log/tor/debug.log
ProtocolWarnings 1
SafeLogging 0
DisableDebuggerAttachment 0
DirAuthority RS4 orport=5000 no-v2 hs v3ident=$finger1 192.168.1.4:7000 $finger2
SocksPort 0
OrPort 5000
Address 192.168.1.4
DirPort 7000
# An exit policy that allows exiting to IPv4 LAN
ExitPolicy accept 192.168.1.0/24:*
# An exit policy that allows exiting to IPv6 localhost
ExitPolicy accept [::1]:*
IPv6Exit 1
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

## Bring up a client

## References
[1] "Tor FAQ - Key Management" [https://www.torproject.org/docs/faq#KeyManagement](https://www.torproject.org/docs/faq#KeyManagement)  
[2] "How do you write multiple line configuration file using BASH, and use variables on multiline?" YumYumYum, Stack Overflow,  [http://stackoverflow.com/questions/7875540/how-do-you-write-multiple-line-configuration-file-using-bash-and-use-variables](http://stackoverflow.com/questions/7875540/how-do-you-write-multiple-line-configuration-file-using-bash-and-use-variables)  
[3] "sudo cat << EOF > File doesn't work, sudo su does" iamauser, Stack Overflow, [http://stackoverflow.com/questions/18836853/sudo-cat-eof-file-doesnt-work-sudo-su-does](http://stackoverflow.com/questions/18836853/sudo-cat-eof-file-doesnt-work-sudo-su-does)
