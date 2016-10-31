sudo sh -c 'echo "deb http://deb.torproject.org/torproject.org trusty main" >> /etc/apt/sources.list'
sudo sh -c 'echo "deb-src http://deb.torproject.org/torproject.org trusty main" >> /etc/apt/sources.list'

sudo gpg — keyserver keys.gnupg.net — recv 886DDD89
sudo gpg --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | sudo apt-key add -

sudo apt-get update
sudo apt-get -y install tor deb.torproject.org-keyring vim

sudo mkdir /var/lib/tor/keys
sudo tor-gencert --create-identity-key -m 12 -a 192.168.1.4:7000 \
            -i /var/lib/tor/keys/authority_identity_key \
            -s /var/lib/tor/keys/authority_signing_key \
            -c /var/lib/tor/keys/authority_certificate 
            
sudo tor --list-fingerprint --orport 1 \
    --dirserver "x 127.0.0.1:1 ffffffffffffffffffffffffffffffffffffffff" \
    --datadirectory /var/lib/tor/
