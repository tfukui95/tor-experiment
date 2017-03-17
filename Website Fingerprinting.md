# Analyzing Anonymous Routing of Network Traffic Using Tor

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
tool for example tcpdump to capture packet traces of IP layer packets.
2. Using information captured such as the length of the packet, the time sent and
received, etc. the attacker creates a profile of the website, also known as a _fingerprint_ [1].
3. Next the attacker listens on the target user's network and similarly captures
packet that is going in and out from the user. However this data is not going to
be blatantly similar to the fingerprint that the attacker creates in step 2, due
to a difference in user, possible packet fragmentation, and website updates.
4. The attacker cannot compromise the target user by comparing the website fingerprint
and user data by looking at them with the eye, and so must use statistical methods
to probabilistically come to a conclusion.

### Characteristics of Packet Traces

Now let us go into more detail of the website fingerprinting process. Many of the
specific details that we cover come from an attack that has been performed by
Panchenko et al. and is described in their paper called _Website Fingerprinting
in Onion Routing Based Anonymization Networks_ [1].

Now for each website, the attacker first collects around 20 instances of traffic.
Within this traffic, there are many characteristics that the attacker must look
out for to create a better more detailed fingerprint of the website.

__Size and Direction__- The size of the packet and whether the packet is ingoing or outgoing
is recorded. Incoming packets are marked as positive, while those that are outgoing
are marked as negative. Keeping track of the order in which the packets arrived
is important as well. Packets with a size of 52 are usually ACK packets, and can
be filtered out to minimize noise.

__Size Markers__- These are markers to be be placed whenever the direction of
traffic changes from ingoing to outgoing and vice-versa. These markers must work
in conjunction with filtering out the ACK packets.

__Total Transmitted Bytes__- This involves adding up separately the total number of
bytes sent and received.

__Percentage of Incoming Packets__- This step involves finding the percentage of
packets that were incoming compared to outgoing.

__Total Number of Packets__- Similar to adding up the total number of bytes sent
and received, the total number of packets is also counted.

### Method of Packet Classification

Herrmann et al. introduces the application of support vector machines (SVM) that
are used in data mining for classification accuracy. The main idea of using SVM's
is the classification of each instance or packet containing webpage details is
treated as a vector [1].

## References

[1] "Website Fingerprinting in Onion Routing Based Anonymization Networks",
Andriy Panchenko, Lukas Niessen, Andreas Zinnen, [https://www.freehaven.net/anonbib/cache/wpes11-panchenko.pdf](https://www.freehaven.net/anonbib/cache/wpes11-panchenko.pdf)  
[2] "Effective Attacks and Provable Defenses for Website Fingerprinting", Tao Wang,
Xiang Cai, Rishab Nithyanand, Rob Johnson, Ian Goldberg, [https://www.freehaven.net/anonbib/cache/wang14-fingerprinting-defenses.pdf](https://www.freehaven.net/anonbib/cache/wang14-fingerprinting-defenses.pdf)  
