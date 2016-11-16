# Anonymity of Network Traffic Using Tor

## Background
Today we live in a world where the Internet is accessible from almost anything that we have in our possession. However as Internet continues to become more expansive and accessible, the attacks on people using the Internet by spying on and stealing their information also increases. Nowadays we never know who may be in between you and your friend when sending text messages. How is this problem being solved in today's world? Well if there was no possible solution, I would not be writing this thesis right now. Let us take a deep dive into this solution, known as Tor.

### Overview of Tor
Tor, which stands for The Onion Router, is a software that protects you from people on the Internet who are trying to spy on you. Tor has a network of routers that keeps your identity hidden by moving your traffic across its network before your traffic is sent to its destination. In this way, when your traffic reaches the final destination, someone spying on you would not know who actually sent that specific data packet. Even the site which is your destination would not know from where the traffic is coming from. In this way, people who use Tor are able to browse the Internet anonymously without ever revealing their location.

Why was Tor built in the first place? Let us first take look back at the history of Tor when it was first created. Tor was originally developed by the US military for the purpose of providing some kind of cloaking mechanism of the identity of government personnel when they worked online[1]. Mainly funded by the Office of Naval Research and DARPA (Defense Advanced Research Projects Agency), the main goal of creating Tor was to provide anonymity for military and intelligence operations that require the use of public communication infrastructure and/or databases[1]. This was their primary objective, and perhaps the only one. The developers of Tor knew that their software would be able to be used by other people for other reasons beyond their control. People would be able to use Tor to commit crimes all while cloaking their tracks. Even while knowing this, the development of Tor continued and was marketed for everyone to use because the primary objective remained as the top and only priority. Everything else was secondary.

In fact, other than those who would use Tor for cloaking criminal activity, the US Navy needed other people other themselves to use Tor. Using a cloaking software exclusively by the US Navy would conversly decloak the people, because an attacker watching the Tor network would know that anything that goes in or out of the network would be by the US Navy. The US Navy required as diverse of a community of people as possible to use Tor in order to hide themselves behind everyone. This was an essential part in fulfilling their primary objective of cloaking the identity of government and intelligence personnel, which was why Tor became a consumer product that everyone would be able to use. Everything was a balance of priority: Tor would not be the perfect to solution for everything, but it would at least be a solution for their primary objective. The crime that comes out of releasing Tor to the public would need to be dealt with at a later time. 

![](http://geography.oii.ox.ac.uk/wp-content/uploads/2014/06/Tor_Hexagons.png)

*Data Source: Internet Geographies at the Oxford Internet Institute*

We can see from the above image that the number of Tor users other than those of the US Navy in fact did increase immensely by placing it on the market. Who are these people that are using Tor? A main group of users of Tor are journalists and activists that live in countries that place restrictions on the Internet. For example many journalists in China use Tor to get past China's national firewall in order to write about events occurring locally around them, in order to create commotion regarding both social and political reform[2]. Other groups of people that want to raise their voice to the public without revealing their identities include activists, whistleblowers, bloggers, and high and low profile people. Tor is also used by law enforcement officers for surveillance of sites that may potentially be used for illegal criminal activity or illegal gambling. Above all these groups of people however, a large group of users of Tor are people who simply with to evade surveillance and protect their privacy when browsing the Internet.

### Attacks Against Tor
Research


## An Overview of Tor's Capabilities
How does Tor actually work? Tor is a software that can run in conjunction with HTTPS, which further increases its security capabilities. HTTPS (Hypertext Transfer Protocol over TLS) is a secure communication protocol used widely in the Internet, which provides authentication of accessed websites and provides privacy of the data that is exchanged between the client, web server, and the website[3]. Encryption of data also occurs, which protects the user from attackers that spy on the network to steal the user's information. Let us take a look at the following example of a simple network to further see the capabilities of Tor and HTTPS.

![](https://github.com/tfukui95/tor-experiment/blob/master/~Tor~HTTPS.PNG)  
*Data Source: Electronic Frontier Foundation (EFF): Tor and HTTPS  
(Question for Fraida: Am i able to not just copy the picture but the simulation with the buttons?)

The above network shows a number of users/nodes with different roles: user, hacker, NSA, ISP, and others who have data sharing either with the ISP or the site that the user is accessing. The source is the user who is on the laptop, and the destination is the black box named Site.com. The yellow box next to each node represents what information about the network the node can see. We can see that in the above network, every node can see all the information that is being exchanged between the user and the website. This includes the site that the user is accessing, the username and password used to access the site, the actual payload/data that is being exchanged, and the location of the user. This specific scenario is when neither Tor nor HTTPS is being used by the user to access the website. For a hacker, such a case is paradise because they can see everything that you send, and can even steal your username and password information and pretend that they are you and do malicious activities. Users who have data sharing with an ISP are usually law enforcement people who have the rights to access this kind of information. In this case where neither Tor nor HTTPS is used, they can also see all of your information. Next we have the NSA (National Security Agency) which either spies on the network or has secret access to the network through the ISPs. The NSA's aim is primarily to deanonymize users who are using Tor as a method to commit crimes without leaving any tracks. The NSA takes control of web servers by placing their own secret servers to impersonate a specific illegal site and to send malware to the users accessing that site. When neither Tor nor HTTPS is used, the NSA can easily view and access your information. Lastly, the user clearly knows all of the information about itself, and the accessed website also does as well. 

Now let us examine what happens when we use HTTPS to access a website:
![](https://github.com/tfukui95/tor-experiment/blob/master/~TorHTTPS.PNG)   
*Data Source: Electronic Frontier Foundation (EFF): Tor and HTTPS  

We can clearly see that the user, the website, and those that have data sharing with the website still see the all the information. This is expected because the user and the site are the ends of the network, and HTTPS is responsible for encrypting the information that travels between both ends. Due to this encryption, the rest of the network can longer see the username and password of the user, and the data that is being sent to the site. Even with data sharing on the ISP, these nodes cannot decrypt the information. The data sharing must be the site itself to have access to the unencrypted information about the user and the data sent.

Now let us examine what happens when we only use Tor to access a website:
![](https://github.com/tfukui95/tor-experiment/blob/master/Tor~HTTPS.PNG)   
*Data Source: Electronic Frontier Foundation (EFF): Tor and HTTPS  

We

## References

[0] "Somehting importatn", somebody. [link to page](http://somepage.txt)  
  [1] [https://pando.com/2014/07/16/tor-spooks/]  
  [2] [https://www.torproject.org/about/torusers.html.en]  
  [3] [https://www.instantssl.com/ssl-certificate-products/https.html]  
  
