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
tool for example tcpdump to capture packet traces of IP layer packets. These packets
are known as _training instances_
2. Using information captured such as the length of the packet, the time sent and
received, etc. the attacker creates a profile of the website, also known as a _fingerprint_ [1].
3. Next the attacker listens on the target user's network and similarly captures
packet that is going in and out from the user. However this data is not going to
be blatantly similar to the fingerprint that the attacker creates in step 2, due
to a difference in user, possible packet fragmentation, and website updates. These
packets are known as _test instances_
4. The attacker cannot compromise the target user by comparing the website fingerprint
and user data by looking at them with the eye, and so must use statistical methods
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

__Size Markers__- These are markers to be be placed whenever the direction of
traffic changes from ingoing to outgoing and vice-versa. These markers must work
in conjunction with filtering out the ACK packets.

__Total Transmitted Bytes__- This involves adding up separately the total number of
bytes sent and received.

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
out to improve performance.

Another factor that is taken into account is that Tor cells are sent in 512-byte
sizes, therefore the packets are rounded up to a size that is a multiple of 600
and are classified accordingly.

In the experiment by Panchenko, et. al, the SVM implementation is done on a
software called Weka, which is a collection of machine learning tools and algorithms
used popularly for data mining experiments. Weka can be used for analyzing data
and predicting results, with an easy to use graphical user interface. The software
provides functions for preprocessing, filtering, classifying, associating, and
visualizing data which is usually imported from a database or csv file.





## References

[1] "Website Fingerprinting in Onion Routing Based Anonymization Networks",
Andriy Panchenko, Lukas Niessen, Andreas Zinnen, [https://www.freehaven.net/anonbib/cache/wpes11-panchenko.pdf](https://www.freehaven.net/anonbib/cache/wpes11-panchenko.pdf)  
[2] "Touching from a Distance: Website Fingerprinting Attacks and Defenses", Xiang
Cai, Xin Cheng Zhang, Brijesh Joshi, Rob Johnson, [http://www3.cs.stonybrook.edu/~xcai/fp.pdf](http://www3.cs.stonybrook.edu/~xcai/fp.pdf)  
[3] "Improved Website Fingerprinting on Tor", Tao Wang, Ian Goldberg, [http://www.cypherpunks.ca/~iang/pubs/webfingerprint-wpes.pdf](http://www.cypherpunks.ca/~iang/pubs/webfingerprint-wpes.pdf)  
