sudo sh -c 'echo "deb http://deb.torproject.org/torproject.org trusty main" >> /etc/apt/sources.list'
sudo sh -c 'echo "deb-src http://deb.torproject.org/torproject.org trusty main" >> /etc/apt/sources.list'

# TODO - one of these commands don't seem to run when using script
sudo gpg --keyserver keys.gnupg.net --recv 886DDD89
sudo gpg --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | sudo apt-key add -

sudo apt-get update
sudo apt-get -y install tor deb.torproject.org-keyring vim apache2

tor --list-fingerprint --orport 1 \
    --dirserver "x 127.0.0.1:1 ffffffffffffffffffffffffffffffffffffffff"

sudo bash -c "cat >/etc/tor/torrc <<EOL 
TestingTorNetwork 1
DataDirectory /var/lib/tor
RunAsDaemon 1
ConnLimit 60
Nickname RS2
ShutdownWaitLength 0
PidFile /var/lib/tor/pid
Log notice file /var/lib/tor/notice.log
Log info file /var/lib/tor/info.log
ProtocolWarnings 1
SafeLogging 0
DisableDebuggerAttachment 0
DirAuthority RS4 orport=5000 no-v2 hs v3ident=$finger1 192.168.1.4:7000 $finger2

SocksPort 0
OrPort 5000
Address 192.168.1.2

# An exit policy that allows exiting to IPv4 LAN
ExitPolicy accept 192.168.1.0/24:*

# An exit policy that allows exiting to IPv6 localhost
ExitPolicy accept [::1]:*
IPv6Exit 1

EOL"

sudo /etc/init.d/tor restart
    
