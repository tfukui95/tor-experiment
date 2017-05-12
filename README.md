# Analyzing Anonymous Routing of Network Traffic Using Tor

## Introduction

### Background

Today we live in a world where the Internet is accessible from almost anything
that we have in our possession. However as the Internet continues to become more
expansive and accessible, the attacks on people using the Internet by spying on
and stealing their information also increases. Tor is an anonymity network that
is volunteer-based, where the users of the Tor network can become part of the
network to increase its size and randomness. The Tor network is a system of relays
that passes around a client's traffic before sending the traffic to the client's
actual destination. While a client's traffic traverses through the Tor network,
the origin of the traffic becomes no longer known, and the final destination is
only known at the exit point of the Tor network. Also while in the Tor network,
client traffic is encrypted by Tor. In this way, Tor protects users from attackers
who spy on a network and try to steal a user's information.

Nowadays many sites are sent through protocols such as HTTPS in order to protect
a user's privacy. HTTPS (Hypertext Transfer Protocol over TLS) is a secure
communication protocol used widely in the Internet, which provides authentication
of accessed websites and provides privacy of the data that is exchanged between
the client, web server, and the website[1]. HTTPS provides end-to-end encryption
of data so that in case an attacker is spying on the network, that attacker is
not able to decrypt the information and figure out what is being transmitted.
Tor works in conjunction with HTTPS, therefore the two methods combined provides
end-to-end encryption of data, and protection by cloaking client and destination
communication, as well as the locations of both ends.

### The Origin and History of Tor

Onion routing research began in 1995 by David Goldschlag, Michael Reed, and Paul
Syverson, with one goal in mind, which was to separate identification from
routing [2]. Authenticating one's identity can be done through the data that is
passed in the data stream, and does not necessarily have to be through one's
location. The goal that these three men had in mind was not to create a complete
form of anonymity when browsing the Internet, but anonymous routing.

Today there are over 6000 Tor relays inside the Tor network, serving over 1.5
million users every day[3]. In the present day, there is a variety of Tor users with different
goals that they wish to achieve from using Tor. One group of users are law
enforcement and intelligence agency personnel, who must stay anonymous when
browsing the Internet to investigate a certain case. Their actions cannot be
traced; therefore anonymous routing is the best solution. Another group of users
stems from those who want to voice their opinion on a certain topic without
revealing their true identity. Tor provides a means for people to discuss and post
on the Internet without a risk for exposure of their location and identity. Then
there are other more ordinary people who simply want to make sure that there
information is protected at a level on step higher than just HTTPS. Simply limiting
the amount of information that can be seen by a person spying on the network is
the main goal that people wish to achieve from using Tor.

How does using Tor differ from using a Virtual Private Network (VPN)? VPNs have
vulnerability where an adversary can observe the information that is being
communicated to the VPN, and it is also easy to associate the users and affiliations
with a VPN [2]. For example, a school's VPN tells us that the users of that VPN are
only students or professors of that school, which narrows down the pool of users
incredibly. Compared to a VPN, the Tor network has a wide variety of users on the
same network. This variety is what is essential to the anonymity that is provided by
onion routing. For example, using cloaking software exclusively by the US Navy
would conversely decloak the people, because an attacker watching the Tor network
would know that anything that goes in or out of the network would be by the US Navy.
The US Navy required as diverse of a community of people as possible to use Tor
in order to hide themselves behind everyone. This was an essential part in
fulfilling their primary objective of cloaking the identity of government and
intelligence personnel, which was why Tor became an "open source" consumer product
that everyone would be able to use [2].

![](https://raw.githubusercontent.com/tfukui95/tor-experiment/master/Top5.PNG)  
*Data Source: Tor Metrics*

The above shows the number of Tor clients per day for five countries for the past
five years. The countries for whose line chart is shown are the top five countries
that are currently using. We see an interesting trend that is present in all five
countries, where the number of Tor clients skyrockets all around the same time in
the year 2013.

![](https://raw.githubusercontent.com/tfukui95/tor-experiment/master/2013TorUser.PNG)
*Data Source: Tor Metrics*

The above shows the total number of Tor clients per day for the year 2013, where
we see this rapid increase in Tor usage. The increase begins in mid-August, and
seems to settle down by the end of September. After doing some research on Tor
during that time period, results came up concerning an enormous botnet in August
2013 that increased the number of Tor users. A botnet is a network of computers
that are infected with malware, and is controlled without the owners knowing.
These computers are often controlled to send spam automatically. This botnet was
known as MEVADE/SEFNIT, created by an Israeli/Ukranian adware company, and the
effect that this botnet had on the Tor network was that the number of Tor users
increased from about 1 million to more than 5 million users [4]. This resulted in a
drastic reduction in the speed of the Tor network, and a breakdown of the
stability of the network. We see that after the number of Tor users reaches a peak
around the end of September, the number begins to decrease gradually, which we can
assume is when the botnet was compromised and the Tor network began to gain its
stability back again. Today, the Tor network is very stable and provides service
to a relatively constant pool of around 1.5 million clients.

## Overview of Tor's Security

### The Functions of Tor

How does Tor actually work? Tor is a software that can run in conjunction with
HTTPS, which further increases its security capabilities. Encryption of data
also occurs, which protects the user from attackers that spy on the network
to steal the user's information. Let us take a look at the following example of
a simple network to further see the capabilities of Tor and HTTPS.

![](https://raw.githubusercontent.com/tfukui95/tor-experiment/master/~Tor~HTTPS.PNG)  
*Image Source: Electronic Frontier Foundation (EFF): Tor and HTTPS*  

The above network shows a number of users/nodes with different
roles:

* user: the person using the network
* hacker: a malicious user who has gained access to the user's network
* NSA: a U.S. government agency
* ISP: the user's Internet service provider
* site: the website, application, or other online resource that the user is accessing

and others who have data sharing
either with the ISP or the site that the user is accessing. The
source is the user who is on the laptop, and the destination is
the black box named Site.com. The yellow box next to each node
represents what information about the network the node can see. We
can see that in the above network, every node can see all the
information that is being exchanged between the user and the
website. This includes the site that the user is accessing, the
username and password used to access the site, the actual
payload/data that is being exchanged, and the location of the
user. This specific scenario is when neither Tor nor HTTPS is
being used by the user to access the website. For a hacker, such a
case is paradise because they can see everything that you send,
and can even steal your username and password information and
pretend that they are you and do malicious activities. Users who
have data sharing with an ISP are usually law enforcement people
who have the rights to access this kind of information. In this
case where neither Tor nor HTTPS is used, they can also see all of
your information. Next we have the NSA (National Security Agency)
which either spies on the network or has secret access to the
network through the ISPs. The NSA's aim is primarily to deanonymize
users who are using Tor as a method to commit crimes without
leaving any tracks. The NSA takes control of web servers by placing
their own secret servers to impersonate a specific illegal site and
to send malware to the users accessing that site. When neither Tor
nor HTTPS is used, the NSA can easily view and access your
information. Lastly, the user clearly knows all of the information
about itself, and the accessed website also does as well.

Now let us examine what happens when we use HTTPS to access a website:

![](https://raw.githubusercontent.com/tfukui95/tor-experiment/master/~TorHTTPS.PNG)   
*Image Source: Electronic Frontier Foundation (EFF): Tor and HTTPS*   

We can clearly see that the user, the website, and those that have data sharing
with the website still see all the information. This is expected because the
user and the site are the ends of the network, and HTTPS is responsible for
encrypting the information that travels between both ends. Due to this encryption,
the rest of the network can longer see the username and password of the user,
and the data that is being sent to the site. Even with data sharing on the ISP,
these nodes cannot decrypt the information. The data sharing must be the site
itself to have access to the unencrypted information about the user and the data
sent.  

Now let us examine what happens when we only use Tor to access a website:

![](https://raw.githubusercontent.com/tfukui95/tor-experiment/master/Tor~HTTPS.PNG)   
*Image Source: Electronic Frontier Foundation (EFF): Tor and HTTPS*  

We now observe that in between the two NSA nodes, are now three new nodes,
which represent three tor relays. The hacker, the nodes sharing data with the
first ISP, and the first NSA node can only see the location of the user sending
traffic. They do not know the username information, the data the user is sending,
nor the site that the user is accessing. Why is this the case even when the user
is not using HTTPS? This is because Tor also encrypts the information in which
the tor relays can only decrypt. This encryption process begins with the user
running the Tor software's special proxy called the onion proxy (OP). The OP then
accesses a special kind of onion router called the directory server, which is a
certain reliable node that provides directories that contain known routers,
including their location and current state. Using the directory the OP determines
which routers are going to be used, negotiates the encryption keys for each router,
and encrypts the packet accordingly. Therefore a user's traffic is encrypted at
the user stage by the onion proxy. The reason why the nodes before the first Tor
relay do not even know which site the user is accessing is because the user's
traffic destination is initially the first tor relay in the circuit. Each Tor relay
in the tor network only knows the certain amount of information that they can
decrypt, which is why it becomes harder for hackers and other people spying on
one's traffic to figure out who is communicating with who. The specific processes
that occur in the Tor process will be explained in much greater detail in the
next section, **Diving Deeper into the Tor Process**. The last tor relay knows
the username information, the data being sent, and the site to access because it
is the exit relay's job to send the data to the site. At this point the traffic
exits the tor network and is no longer encrypted. Mostly everything can be seen
by the nodes that are eavesdropping on the network, except for one important piece
of information: the user location. After having been bounced around the tor
network, the traffic no longer contains the original user's location, which makes
it difficult to match which user is accessing the site. However since the user
information and data can still be seen, this information can be stolen which is
a weakness of using Tor.

We resolve the problem that nodes eavesdropping the second ISP have access to user
information by using Tor in conjunction with HTTPS.  

![](https://raw.githubusercontent.com/tfukui95/tor-experiment/master/TorHTTPS.PNG)  
*Image Source: Electronic Frontier Foundation (EFF): Tor and HTTPS*  

The information that the nodes before the entry Tor node can see is still the same,
which is very limited. The biggest change that we can see is that the nodes
eavesdropping on the second ISP which is after the Tor network can no longer see
the username and password, along with the data that is being sent. This includes
the exit relay as well. This is the case because the original traffic being sent
from the user is now encrypted with both Tor and HTTPS. When the traffic reaches
the exit relay and leaves the Tor network, it is no longer encrypted by Tor, but
is still encrypted by HTTPS from beginning to end. However we observe that the
exit relay still knows the site to access because it still has to perform its job
to deliver the HTTPS encrypted traffic to the site that it is being told to access.
Lastly we can see how the website and the nodes sharing data with the site clearly
know the username information and data because the traffic's HTTPS encryption is
decrypted at the destination. However the location of the original user is still
unknown, maintaining privacy and security. Using Tor on top of HTTPS provides
security immeasurably greater than using neither or even one or the other. From
this example the capabilities of Tor in protecting and cloaking a user from
hackers and eavesdroppers were clearly seen. The following table summarizes which
nodes can see what information on specific settings.

|      | Neither | HTTPS Only     | Tor Only | HTTPS + Tor |
| :-------------: | :-------------: | :-------------: | :-------------: | :----: |
| **Client Address**     | Everyone | Everyone | User <-> Entry Node | User <-> Entry Node |
| **Web Server Address**  | Everyone | Everyone | Exit Node <-> Site + Data Sharing | Exit Node <-> Site + Data Sharing |
| **Username and Password** | Everyone | User, Site + Data Sharing | Exit Node <-> Site + Data Sharing | User, Site + Data Sharing |
| **Packet Contents**     | Everyone | User, Site + Data Sharing | Exit Node <-> Site + Data Sharing | User, Site + Data Sharing |
| **Using Tor** | N/A | N/A | Everyone | Everyone |

### Diving Deeper into the Tor Process

Now that we know what Tor is and the benefits of using Tor to protect your privacy
and security, let us examine what goes on behind the scenes of the Tor network.
The Tor network consists of onion routers (OR), or nodes that a Tor user's traffic
passes through before reaching its destination. There are three main kinds of ORs:
entry node, relay node, and exit node. The entry node is where the user's traffic
first enters the Tor network. The exit node is conversely where the traffic exits
the Tor network. Any nodes in between are relay nodes that simply pass the traffic
from one node to the next. The specific functions of each OR will be explained
later in the section. Among these ORs there is a special kind of OR called the
directory authority (DA), which is a certain more trusted, reliable OR that
contains a list of known ORs in the network, including their location and current
state.

#### Keys

The Tor network is constantly changing, and there needs to be some kind of mechanism
so that the DAs in the Tor network are constantly aware of these changes that
occur. This is where keys come into play. A key is a form of authentication which
provides a means to encrypt as well as to decrypt information. Keys allow safe
communication of data, by making sure that information being sent is only decrypted
by the people that it was intended for. A DA has three kinds of keys: an
authority identity key, an authority signing key, and an authority certificate.
In order to keep information about the DA up to date, it must sign directory
information about itself periodically. This is done by the authority signing key.
The authority signing key is not a permanent key, and is replaced around every
3-12 months. In order to authenticate the signing key, a DA has an authority
certificate. This certificate must also be authenticated, which is done by the
DA's authority identity key. This identity key is a long term key which as the
name explains, identifies that the DA truly is a DA.

Now that we know the mechanism in which a DA's status is constantly updated, let
us take a dive into a similar process for the rest of the ORs in the Tor network.
An OR has four kinds of keys: a secret id key, a secret onion key, a secret onion
key ntor, and a fingerprint. The secret id key is similar to the authority identity
key, and is used to sign the router's descriptor, TLS certificates, and to sign
directories. A router descriptor contains the specifications of that router,
including its keys, location, bandwidth, exit policy, and other minor details [5].
The reason to sign directories comes from the necessity to constantly keep the
directories updated about all of the ORs, so that the directory authority can
provide up-to-date information to the OP and client. The secret onion key is a
key that is used when establishing a Tor circuit to pass traffic along its network.
These keys are not permanent unlike the identity key, and are changed every so
often in order to prevent any form of compromise. The onion key also creates
short-lived keys used to access TLS connections to communicate with one another
and the user [5]. The secret onion key ntor is a short-term key used specifically
for the opening of a tor circuit, when a three-way handshake is required. The
fingerprint key, as the name suggests is a fingerprint of the identity key, used
so that the identity key's location and security is preserved.

#### Cells  

ORs pass traffic along the Tor network in fixed-size cells/packets of 512 bytes.
 Each cell is encrypted in many levels, where these levels are decrypted by a key
 at each OR until it reaches the exit node where it is then sent to the website.
 There are two main types of cells: control cells and relay cells.

![](https://raw.githubusercontent.com/tfukui95/tor-experiment/master/cell%20format.PNG)   
*Data Source: https://svn.torproject.org*  

The above shows the structure of a cell, where the top is the control cell
structure and the bottom is the relay cell structure. The control cell contains
three parts: CircID, CMD, and DATA. CircID is the circuit identifier which specifies
which circuit is being referred to. CMD is the command to be done, and DATA is the
payload, which contains specific instructions for the command. There are three
main types of control commands for creating a connection: PADDING, CREATE/CREATED,
and DESTROY [5]. Padding is a command used to keep a connection alive. The create,
created and destroy commands are used to build and break down a circuit. A CREATE
cell's payload contains information on the handshake that is to be used to create
a new connection. Relay cells have an additional relay header to identify that
they are not command cells. Their header also contains a stream ID, a checksum,
and the length of the relay's payload. Unlike command cells, relay cells carry
end-to-end stream data. The main commands for a relay cell for managing a
connection are the following: RELAY BEGIN/CONNECTED, RELAY END, RELAY TRUNCATE/TRUNCATED,
'RELAY EXTEND/EXTENDED, and RELAY DATA. Relay begin is a command to open a stream,
and relay connected is to acknowledge this opening. Notice that these commands can
only be called once the Tor circuit has been created and there is a connection
between the client and the website that is to be accessed. Relay end is the
command to close a stream. Relay truncate tears down a part of the circuit and
truncated acknowledges this. Relay extend does the opposite and tells the end of
the circuit to extend by one hop, and extended acknowledges this. Lastly, relay
data is a command for flowing data along a Tor circuit, which can be done only
after a stream is opened.

An important process in creating connections is when we need to extend or truncate
a circuit. In order to extend a current circuit by one more hop, the OP first sends
an RELAY EXTEND cell which is passed along until the last node in the circuit, in
which at that point the node is instructed by the OP to send a CREATE cell to
extend the circuit to the specified new node. What is very important to note here
is that the payload of a RELAY EXTEND cell also contains the handshake instructions
of the payload of a CREATE cell. The only additional component of the payload are
link specifers that describe the next node to connect to.

#### Initialization of Connections

Before a connection between two nodes is created and opened, there are a number
of steps of package exchanges that must take place to negotiate authenticity of
the nodes. This process is called a TLS handshake to ensure that the link between
two nodes is secure and encrypted. There are three kinds of TLS handshakes:
certificates-up-front, renegotiation and in-protocol.

![](https://raw.githubusercontent.com/tfukui95/tor-experiment/master/CertificatesUpFront.PNG)  

The certificates-up-front handshake is the simplest TLS handshake that is supported
by all versions of Tor. In this process, both sides of the link must send each
other a two-certificate chain. This chain consists of a certificate using a
short-term connection public key and a self-signed certificate that contains its
identity key. This process is the simplest of the three and securely allows both
sides to confirm each others' availability.

![](https://raw.githubusercontent.com/tfukui95/tor-experiment/master/Renegotiation.PNG)  

For renegotiation and in-protocol handshakes, the following control cell commands
are required: VERSIONS, CERTS, AUTH_CHALLENGE, and AUTHENTICATE [6]. In a
renegotiation handshake, first after a node initializes, the responding node sends
a single connection certificate as the initial TLS connection. Following this a
renegotiation is performed, similar to the certificates-up-front handshake.
Following this, both nodes send a VERSION cell to negotiate which link protocol
version will be used. After this is set, both sides send a NETINFO cell to confirm
each others' location and timestamp, which is the local clock of the node. A
NETINFO cell also contains address locations of other ORs that are known by that
specific OR.

![](https://raw.githubusercontent.com/tfukui95/tor-experiment/master/InProtocol.PNG)  

An in-protocol handshake requires a few different steps from the renegotiation
handshake. After the initial TLS connection, renegotiation is skipped, and instead
both sides send a VERSION cell to negotiate the link protocol version. Directly
following this the initiator sends a CERT cell, which contains a list of keys and
certificates that a node claims to have in possession. The responder send back its
own CERT cell, followed by a AUTH_CHALLENGE which as the name describes, is a request
by the responder to authenticate the initiator's trustworthiness. The initiator
responds with an AUTH_CHALLENGE cell, a CERT cell, and an AUTHENTICATE cell which
contains the authentication [6]. Now that the authentication process has finished,
both nodes send each other a NETINFO cell containing its location and timestamp.

#### Directory Authority

In an older version of Onion Routing, the state of each router was updated through
flooding: each router was to send a status update to its neighbors, which spread
to other neighbors. However there was much inconvenience with this design due to
delays in flooding, causing different views at different parts of the network.
From there a new strategy was developed in which a group of reliable and well-known
ORs called directory authorities (DA) would be responsible for keeping an update
directory of the states and locations of all Tor routers. Each DA also acts as an
HTTPS server for clients to access to gain the most up-to-date states of the Tor
network [5]. The DA does not add ORs who do not have a proper identity key, which
prevents attackers from creating fake nodes.

The DA itself can also be vulnerable to attacks by an adversary, which makes the
network vulnerable to fake directories of router locations. In order to prevent this,
the DAs in the network must be synchronized with one another, making sure that they
agree with the same common directory. Clients must make sure that a directory is
signed by a number of DAs to consider it trustworthy. This process of synchronizing
with other DAs is called consensus. The DAs come to a new consensus every hour
and the consensus is frequently checked to make sure that it is not too old [7].

## Notes

You can find a link to my thesis defense [here](https://docs.google.com/presentation/d/1MUq0iiiuTazeB9wU_rOQFi5fCaD49f-FzRwwq74pF2A/edit#slide=id.p).

## References

  [1] "What is HTTPS?" [https://www.instantssl.com/ssl-certificate-products/https.html](https://www.instantssl.com/ssl-certificate-products/https.html)  
  [2] "A Peel of Onion" Paul Syverson, [http://dl.acm.org/citation.cfm?id=2076750](http://dl.acm.org/citation.cfm?id=2076750)
  [3] "Tor Metrics" Tor Project, [https://metrics.torproject.org/](https://metrics.torproject.org/)
  [4] "On the Actors Behind MEVADE/SEFNIT" Forward-Looking Threat Research Team,  [http://www.trendmicro.com/cloud-content/us/pdfs/security-intelligence/white-papers/wp-on-the-actors-behind-mevade-sefnit.pdf](http://www.trendmicro.com/cloud-content/us/pdfs/security-intelligence/white-papers/wp-on-the-actors-behind-mevade-sefnit.pdf)  
  [5] "Tor: The Second-Generation Onion Router" Roger Dingledine, Nick Mathewson, Paul Syverson, Tor Project, [https://svn.torproject.org/svn/projects/design-paper/tor-design.pdf](https://svn.torproject.org/svn/projects/design-paper/tor-design.pdf)  
  [6] "Tor Protocol Specification" Roger Dingledine, Nick Mathewson, Tor Project, [https://gitweb.torproject.org/torspec.git/tree/tor-spec.txt](https://gitweb.torproject.org/torspec.git/tree/tor-spec.txt)  
  [7] "How can I get consensus data from Directory authority servers for research purpose?" Stack Overflow,  [http://tor.stackexchange.com/questions/4939/how-can-i-get-consensus-data-from-directory-authority-servers-for-research-purpo](http://tor.stackexchange.com/questions/4939/how-can-i-get-consensus-data-from-directory-authority-servers-for-research-purpo)  
