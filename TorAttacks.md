# Analyzing Anonymous Routing of Network Traffic Using Tor

## Understanding the Various Adversaries of Tor

Tor is not a perfect system. In fact it is a very much far-from-perfect system
where the Tor developers are aware of the fact that there are many methods in
which Tor's anonymity can be broken. However, Tor developers encourage continued
research in finding ways to break the system's anonymity because each new method
provides a new perspective to see how the Tor network can be strengthened to
protect against these attacks.

This section aims to provide readers with a concrete understanding of the various
attacks that have been conducted on the Tor network. For each attack the following
points will be covered to keep everything organized:

1. Has this attack been performed previously?
2. Key terms concerning the attack.
3. Is the attack active or passive?
4. Which part of the network does it attack?
5. Which parts of the network does the attacker need to control or be able to
access?
6. What are the specifics of the attack? How is the attack performed?

### AS-Level Adversary Attack

1. This attack has been recreated by Matthew Edman and Paul Syverson, in their
paper called _AS-awareness in Tor Path Selection_ [1]. In this paper, their main
goal was to propose possible AS-aware path selection algorithms that would increases
anonymity and avoid AS-level adversaries. In order to show this, they first used
past routing information to construct a model of the ASes. Then they used an
algorithm to calculate shortest paths between ASes, and from this experiment
they found that a single AS could observe both ends of a connection around 10 to
30% of the time.
2. __Autonomous Systems__ (ASes) are a series of independent networks that make up
the Internet. Whenever a user's data is sent through the Tor network to the
requested destination, the data goes through ASes.
__Traffic Correlation__ is an attack which aims to deanonymize a user by matching
incoming and outgoing traffic. A common type of traffic correlation attack known
as the end to end confirmation attack is performed by correlating the size of
packets incoming and outgoing, as well as the timing of these packets that are
transmitted [2]. A good example of this kind of correlation is how a user
streaming a video would be receiving packets in a different pattern from someone
who is simply using Facebook and browsing the page.
3. This attack is a passive attack because the attacker does not put into the
traffic but simply listens to the connection.
4. This attack focuses on the entry and exit points of the Tor network as places
to attack.
5. The attacker must have control of an AS where the traffic between a user and
the entry node, and that between the exit node and destination go through the
same AS.
6. When the traffic between the user and entry node, as well as the traffic
between the exit node and destination both go through the same AS that is under
the control of the attacker, the attacker can see the user's traffic that is
ingoing and outgoing the Tor network. Using traffic correlation (defined above),
the attacker aims to deanonymize the user and figure out who is communicating with
who.

### Website Fingerprinting

1. This attack has been performed by Panchenko et al. and is described in their
paper called _Website Fingerprinting in Onion Routing Based Anonymization Networks_
[3]. The paper describes website fingerprinting as another traffic confirmation
attack, which is described in AS-Level Adversary section, but can be performed by
a local adversary. For example, for people in oppressive regimes, who try to access
websites that are located in outside countries, are still able to deanonymized by
a local eavesdropper that is able to listen to the traffic traveling between the
user and the entry node of the Tor network.
2. __Fingerprinting__ is a kind of traffic analysis that involves observing a user's
traffic and identifying certain patterns which can later be used in traffic
confirmation to correlate what website a user may be accessing.
3. This attack is passive because the attack is simply gathering fingerprints of
the user and website, and is not padding any data into the traffic.
4. This attack is focused mostly on observing the data between the user and the
entry node of the Tor network.
5. The attacker must have packet traces of the websites that he is interested in
seeing whether a certain user accesses that specific website.
6. First, the attacker collects packet traces from certain websites that he is
interested in monitoring. Then the attacker collects packet traces that are sent
by the user that he believes may be visiting those sites. He then compares the
traces from both sides by using supervised classification [4]. The local attacker
is located on the same network or ISP as the user, or has access to that network.

### Selective Denial of Service (SDoS)

1. This attack is a theoretical attack that is described in a paper by Borisov et al.
called _Denial of Service or Denial of Security?_ [5]. This attack is described as
having a secondary objective to deanonymizing the user, which is to decrease the
reliability and efficiency of using the Tor network. The specifics of how this
attack is performed will be explained in greater detail in the upcoming bullet
points.
2. __Denial of Service (DoS)__ as the name connotes is an attack which aims to disallow
a user from using a service that would otherwise be allowed. In this case, the DoS
refers to disallowing using a certain connection in the Tor network to pass traffic.
3. This attack is active due to the action of killing a connection tunnel to
disallow the forwarding of a user's traffic.
4. SDoS is a direct attack on the connection tunnel that would be blocked if
traffic confirmation is not successful. Otherwise, the attack focuses more on the
traffic of a user as it enters and leaves the Tor network.
5. In order to perform this attack successfully, the adversary must be in control
of an entry and exit relay that is used on the same circuit of a user to pass
traffic.
6. This attack has two possible outcomes, where neither is a failed outcome. One
is that if both the entry and exit nodes of a connection are run by the same
adversary, then traffic confirmation can be performed to deanonymize the user.
If this does not turn out to be the outcome, the adversary will block forwarding
of traffic through that connection tunnel, and as a result the user will need to
use another circuit. A main point of this active attack is that instead of making
users not want to use Tor anymore, the attack merely makes the attack a bit less
reliable but nonetheless functional [5]. Tor users that try to create another circuit
will provide adversaries more opportunities of deanonymization, which is an
important strength of this attack.

### Low Resource Routing Attack

1. This attack has been performed by Bauer et al. and is described in their paper
_Low-Resource Routing Attacks Against Tor_ [6]. An important goal of this experiment
was to try to minimize the requirements for an adversary to be able to compromise
a user and its destination, especially due to the fact that the adversary relays
have minimal resources.
2. __Load Balancing__ is a process used in network traffic which aims to balance
traffic efficiently across all of the available resources in the network. In
order to maintain a low-latency system, Tor must not only rely on the routers that
have high amounts of available bandwidth, but on all of the available resources.
3. This attack is an active attack because not only does the adversary install
one's own routers, but also logs fake statistics of available bandwidth.
4. The areas of the Tor network that this attack focuses on are the relays of the
network, as the adversary's relays are competing with the other relays to be
chosen as users' relays to direct traffic.
5. This attack requires a number of low-resource routers that can advertise false
bandwidth capabilities, as well as a central authority that will link the colluding
relays by matching the logs of information that each router collects and to see
whether there is any correlation.
6. After an adversary has under his/her possession a number of low-resource relays
that can advertise high bandwidth capabilities, and preferably has an unrestricted
exit policy to allow all kinds of traffic, the next step is to try to compromise
the user and destination communication before any payload is sent. This means that
the attack is focused on the initial circuit building algorithm stage. This is
important because the adversary relays are simply falsely advertising bandwidth,
therefore will not be able to efficiently forward any actual payload, so the
attack must be done in the early stages. Each adversary logs the following information:
(1) its location on the current circuit’s path (whether it is an entry, middle,
or exit node); (2) local timestamp; (3) previous circuit ID; (4) previous IP
address; (5) previous connection’s port; (6) next hop’s IP address; (7) next hop’s
port; and (8) next hop’s circuit ID." [6]. The colluding central authority then
collects these logs from each adversary relay and sees whether there is any
correlation to compromise a connection.

### Sniper Attack

1. The sniper attack has been performed by Jansen et al. and their experiment
is laid out in there paper _The Sniper Attack: Anonymously Deanonymizing
and Disabling the Tor Network_ [7]. The sniper attack is a low cost yet highly
effective denial of service. However, this attack by itself is only capable of
performing DoS attacks, and not deanonymization. However, when coupled with
SDoS, the attacks are very effective.
2.  __Denial of Service (DoS)__ (taken from the SDoS section above) is an attack which
aims to disallow a user from using a service that would otherwise be allowed. In
this case, the DoS refers to disallowing using a certain connection in the Tor
network to send traffic.  
__End-to-End Sliding Window Mechanism__ is a mechanism used by Tor to control
congestion in the Tor network. Each node at the end of a circuit (client and exit
relay) manages a package window for incoming packets, and a delivery window for
outgoing packets.
3. This attack, as it is a DoS attack is certainly active.
4. The main victim that the Sniper Attack aims for is the entry relay that is
used in the circuit to pass the user's traffic.
5. There are two parts of the network that an adversary must control in order to
conduct this attack: an adversary client and an exit relay. These two colluding
parts work together to conduct a DoS on the entry relay.
6. The basic process of this attack is that when the delivery edge of a node stops
reading from its TCP port, the receive buffer will fill, which would result in
the adjacent node being able to forward any more traffic, filling up the queue of
the entry node. The malicious exit node also ignores any empty package window and
continues to send traffic along the circuit. The middle node does not have any
congestion control mechanism to stop accepting from the exit relay, so therefore
continues to pass the traffic to the entry relay, piling up there. A more detailed
explanation of the attack is provided by Jansen et al [7]:

 > The adversarial client constructs a circuit by selecting the target relay as
the entry and the adversarial relay as the exit. The client signals the exit to
start the attack by issuing an arbitrary request over the custom attack circuit,
and then stops reading from the TCP connection to the target entry. The exit
simply ignores the empty package windows and continuously sends data it arbitrarily
generates, increasing the amount of memory consumed by the entry to queue the cells.
Note that it is not necessary for the malicious exit to produce correctly encrypted
Tor cells since they will never be fully decrypted by the client (though correct
circuit IDs are required). Eventually, the Tor process on the entry node depletes
all of the available memory resources and is terminated by the operating system.

### DNS Correlation Attack

1. This attacked has been developed by Greschbach et al. and is explained in their
paper _The Effect of DNS on Tor’s Anonymity_ [8]. Unlike most traffic confirmation
attacks which focus on TCP traffic to correlate a user and its destination's
communication, this attack focuses on the DNS traffic that is sent alongside TCP
traffic. Simply loading a webpage requires generating lots of DNS traffic to many
different domains. In this paper a type of attack called DefecTor is introduced,
which was produced to test the DNS correlation attack. Compromising a connection
using DNS traffic confirmation is still a relatively new idea with this paper
serving as one of the forefronts to this research.
2. __Domain Name Servers (DNS)__ is like a phone book for the Internet, in which
they are servers that have a directory of names of domains, and there corresponding
IP addresses. Although computers can easily remember a series of numbers, we users
have difficulty doing so, and are able to remember names like Facebook and Youtube
more easily. DNS are responsible for being the middleman between us users and our
computer so that we can access the specific site that we want.
3. A DNS Correlation Attack is a passive active like an AS-Level Adversary Attack,
as it only listens to the network and collects traces of traffic to see if there
is any correlation.
4. This attack focuses its attack on the DNS traffic that is generated whenever
a Tor user accesses a website.
5. In order for this attack to be performed, a user must have access to the DNS
traffic at both ends of the Tor network.
6. To see the DNS traffic at the entry point of the Tor network, the adversary
can operate on the network level, for example to have access to an ISP. Another
alternative is to operate on the relay level by running an adversary entry relay.
The adversary must also be able to see the outgoing DNS traffic, therefore must
either operate on the network level, or run a malicious DNS resolver or server [8].
Operating a malicious exit relay is also an option, but the efficiency would be
on par with a normal correlation attack. The following image shows the layout
of a DNS Correlation Attack.

![](https://raw.githubusercontent.com/tfukui95/tor-experiment/master/DNSCorrelation.PNG)  
*Image Source: Paper by Greschbach et al. [8]*   


### Hidden Services Attack

1. This attack has been performed by Kwon et al., described in their paper _Circuit
Fingerprinting Attacks: Passive Deanonymization of Tor Hidden Services_ [9]. This
attack on users that utilize hidden services of the Tor network is one of the first
of its kind. In this paper it is described that traffic that is generated to use a
hidden service is quite unique from regular Tor traffic, and thus it is easy to
separate these users and focus on the users using hidden services. The method uses
circuit fingerprinting, a form of attack we observed in the website fingerprinting
section. The paper describes how circuit fingerprinting comes in "two settings:
open- or closed-world. In the closed-world setting, the attacker assumes that the
websites visited are among a list of k known websites, and the goal of the attacker
is to identify which one. The open-world setting is more realistic in that it assumes
that the client will visit a larger set of websites" [9].
2. __Fingerprinting__ is a kind of traffic analysis that involves observing a user's
traffic and identifying certain patterns which can later be used in traffic
confirmation to correlate what website a user may be accessing.  
__Hidden Services__ are special services provided by Tor, in which only Tor users
can access. Using these services is like an extra layer of anonymity within the
Tor network.
3. A Hidden Service Attack is a passive attack because it is a form of circuit
fingerprinting, which only observes the traffic in the Tor network and aims to
find any correlation in traffic. An extra step that is taken in this attack is that
traffic relating to hidden services and traffic of normal Tor usage is separated
so a more efficient may be conducted.
4. The focus of attack are the hidden services of the Tor network, which exhibit
different behaviors from regular Tor traffic.
5. An important factor for a successful hidden service attack is that the adversary
must be able to listen to the traffic between the user and the hidden service. This
communication is not direct, but through the relays that the user chooses to create
a circuit to the hidden service.
6. In order for a user to use a hidden service, the hidden service must first choose
a random relay to serve as the Introduction Point (IP), in which a message containing
the service's public key is sent. The client also must choose a random relay to serve
as the Rendezvous Point (RP) which will serve as a connection point to the hidden service.
Both sides must also create a circuit connection to the IP and RP to exchange keys [9].
An attack on the hidden services requires knowing how a connection to a hidden
service is established in the first place, and seeing that traffic sent to a hidden
service is unique. The actual deanonymization of the circuit is done through a
website fingerprinting attack, explained in a section above.

## A Taxonomy of Tor Adversaries

In order to better see how all of these adversaries of Tor are unique in of itself
but also at the same have similarities amongst each other, I have made a taxonomy
of the attacks in a table.

|      | Active/Passive | Observes Incoming/ Outgoing Traffic  | Level of Authority | Has Been Performed Before |
| :-------------: | :-------------: | :-------------: | :-------------: | :-----: |
| **AS-Level Adversary**     |   Passive | :heavy_check_mark: | Network Level | :heavy_check_mark: |
| **Website Fingerprinting**  | Passive | :heavy_check_mark:| Network Level | :heavy_check_mark: |
| **SDoS** | Active | :heavy_check_mark: | Relay Level | |
| **Low-Resource Routing**     | Active | :heavy_check_mark: | Relay Level | :heavy_check_mark: |
| **Sniper** | Active | | Relay Level | :heavy_check_mark: |
| **DNS Correlation** | Passive | :heavy_check_mark: | Network/Relay Level | :heavy_check_mark: |
| **Hidden Services** | Passive | :heavy_check_mark: | Network Level | :heavy_check_mark: |

The first categorization is whether the active or passive. Active attacks usually
require the usage of one's own resources, such as installing one's own adversary
relays in order to conduct the attack. Passive attacks on the other hand typically
have the one requirement of being on the network level, such as an AS or ISP, to
be able to listen to the network for the user's traffic.

The next categorization is whether the attack requires listening to the traffic
of a user that goes into and out of the Tor network, or in other words having to
be at the ends of the Tor network to capture user packets. The Sniper Attack is the
only attack that does not require any listening on user traffic at the ends of the
Tor network because the goal of this attack is not deanonymization but rather
a DoS of the entry relay that is chosen for that circuit. Making the Tor network
less reliable but still functional is the main objective of the Sniper Attack.

The third categorization defines the level of authority, or in other terms the
amount of traffic that the attacker needs to be able to see to be able to perform
the attack. This being said, for example not every attacker is able to perform a
website fingerprinting attack. We define two levels: network and relay. An attack
that requires to be on the network level means that the attacker must either be on
the same connection as the user, or has control over/has data sharing from the ISP
of the user. An attack that requires to be on the relay level means that the attacker
must install one's own malicious relays, and have those relays be chosen to create
a user's circuit.

The last categorization is whether the attack is an actual experiment that has
been conducted and proven, or is still just a theoretical attack waiting to be
tested. The only attack that has not actually been tested is the SDoS attack, where
the theory behind the experiment is there, with credible evidence. The possible
outcomes of an experiment that is performed is also given, backed by the theoretical
evidence that is presented.  


## References

[1] "AS-awareness in Tor Path Selection", Matthew Edman, Paul Syverson,
[https://www.freehaven.net/anonbib/cache/DBLP:conf/ccs/EdmanS09.pdf](https://www.freehaven.net/anonbib/cache/DBLP:conf/ccs/EdmanS09.pdf)  
[2] "How do traffic correlation attacks against Tor users work?", Arminius,
Security Stack Exchange, [http://security.stackexchange.com/questions/147402/how-do-traffic-correlation-attacks-against-tor-users-work](http://security.stackexchange.com/questions/147402/how-do-traffic-correlation-attacks-against-tor-users-work)  
[3] "Website Fingerprinting in Onion Routing Based Anonymization Networks",
Andriy Panchenko, Lukas Niessen, Andreas Zinnen, [https://www.freehaven.net/anonbib/cache/wpes11-panchenko.pdf](https://www.freehaven.net/anonbib/cache/wpes11-panchenko.pdf)  
[4] "Effective Attacks and Provable Defenses for Website Fingerprinting", Tao Wang,
Xiang Cai, Rishab Nithyanand, Rob Johnson, Ian Goldberg, [https://www.freehaven.net/anonbib/cache/wang14-fingerprinting-defenses.pdf](https://www.freehaven.net/anonbib/cache/wang14-fingerprinting-defenses.pdf)  
[5] "Denial of Service or Denial of Security?", Nikita Borisov, Prateek Mittal,
George Danezis, Parisa Tabriz, [http://www.australianscience.com.au/research/google/33413.pdf](http://www.australianscience.com.au/research/google/33413.pdf)  
[6] "Low-Resource Routing Attacks Against Tor", Kevin Bauer, Damon McCoy, Dirk
Grunwald, Tadayoshi Kohno, Douglas Sicker, [https://www.freehaven.net/anonbib/cache/bauer:wpes2007.pdf](https://www.freehaven.net/anonbib/cache/bauer:wpes2007.pdf)  
[7] "The Sniper Attack: Anonymously Deanonymizing and Disabling the Tor Network",
Rob Jansen, Florian Tschorsch, Aaron Johnson, Bjorn Scheuermann, [http://www.robgjansen.com/publications/sniper-ndss2014.pdf](http://www.robgjansen.com/publications/sniper-ndss2014.pdf)  
[8] "The Effect of DNS on Tor’s Anonymity", Benjamin Greschbach, Tobias Pulls, Laura Roberts,
Philipp Winter, Nick Feamster, [https://nymity.ch/tor-dns/tor-dns.pdf](https://nymity.ch/tor-dns/tor-dns.pdf)  
[9] "Circuit Fingerprinting Attacks: Passive Deanonymization of Tor Hidden Services",
Albert Kwon, Mashael AlSabah, David Lazar, Marc Dacier, Srinivas Devadas, [https://people.csail.mit.edu/devadas/pubs/circuit_finger.pdf](https://people.csail.mit.edu/devadas/pubs/circuit_finger.pdf)  
