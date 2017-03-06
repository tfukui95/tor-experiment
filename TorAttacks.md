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

1. Who has performed this attack previously?
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
attack, but can be performed by a local adversary. For example, for people in
oppressive regimes, who try to access websites that are located in outside countries,
are still able to deanonymized by a local eavesdropper that is able to listen
to the traffic traveling between the user and the entry node of the Tor network.
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

1.
2.
3.
4.
5.
6.

### Low Resource Routing Attack

1.
2.
3.
4.
5.
6.

### Sniper Attack

1.
2.
3.
4.
5.
6.

### DNS Correlation Attack

1.
2.
3.
4.
5.
6.

### Hidden Services Attack

1.
2.
3.
4.
5.
6.


## References

[1] "AS-awareness in Tor Path Selection", Matthew Edman, Paul Syverson, [https://www.freehaven.net/anonbib/cache/DBLP:conf/ccs/EdmanS09.pdf](https://www.freehaven.net/anonbib/cache/DBLP:conf/ccs/EdmanS09.pdf)  
[2] "How do traffic correlation attacks against Tor users work?", Arminius,
Security Stack Exchange, [http://security.stackexchange.com/questions/147402/how-do-traffic-correlation-attacks-against-tor-users-work](http://security.stackexchange.com/questions/147402/how-do-traffic-correlation-attacks-against-tor-users-work)  
[3] "Website Fingerprinting in Onion Routing Based Anonymization Networks", Andriy Panchenko, Lukas Niessen, Andreas Zinnen, [https://www.freehaven.net/anonbib/cache/wpes11-panchenko.pdf](https://www.freehaven.net/anonbib/cache/wpes11-panchenko.pdf)
[4] "Effective Attacks and Provable Defenses for Website Fingerprinting", Tao Wang, Xiang Cai, Rishab Nithyanand, Rob Johnson, Ian Goldberg, [https://www.freehaven.net/anonbib/cache/wang14-fingerprinting-defenses.pdf](https://www.freehaven.net/anonbib/cache/wang14-fingerprinting-defenses.pdf)
