# Detection of collusion communities in the FIL+ program

## Introduction to the problem

Filecoin is a decentralized storage network. Here, Storage Providers (SPs) contribute storage to the network and, in turn, receive a proportional claim on network consensus and block rewards. Filecoin is then built on the concept of "available storage". However, available storage is not useful is clients are not using that storage to store real data. With this in mind, the Filecoin community introduced the Filecoin Plus program.

Filecoin Plus aims to maximize the amount of useful storage on Filecoin by adding a layer of social trust to the Network. Clients can apply to Notaries to receive DataCap, which can be used to incentivize Storage Providers to take storage deals. Storage Providers who take deals that are compensated with DataCap receive a 10x multiplier on their block rewards. Filecoin Plus puts power in the hands of Clients and incentivizes SPs to support real use case on the Network.

The job of the Notaries is to access whether a Client applying with a given dataset is a legitimate entity and has, in fact, real data to be stored. If there were no checks in place, a Storage Provider could pretend to be a Client and submit "trash" data just to get a higher share of rewards. Even though we have these checks in place, because there is a level of human interaction between Notaries, Clients and Storage Providers, there is space for abuse.

If we want to scale this process and serve ever more Clients, we need to have automated processes in place to detect collusion and abuse. This is whether this project fits in. We are interested in analysis previous applications (and the corresponding deals) and to find automated ways to detect collusion in the application process and to prevent future abuse taking place.
 
### Research questions

1. What collusion typologies can we find in previous FIL+ applications?
2. Can we use automated methods to detect abuse in previous FIL+ applications?
3. Can we develop a reputation scope for the application participants based on the collusion detection methods in order to inform future application requests?

## Solving this problem

Clients, Notaries and Storage Providers form a graph that can be analyzed. Each participant is a node and each application forms a set of edges connecting the participants involved in the application process.

With this in mind, one can apply an exploratory data analysis on this graph in order to specific cases or graph topologies that could be indicative of collusion between the parties. Possible methods to explore include:
- Community detection
- Clustering coefficient analysis
- Network motifs

After this exploratory phase, we want to apply the most promising methods to score the entire set of participants and to develop a collusion score for each participant. This can then be used in future application processes to prevent abuse.

### Estimated impact

- Understand how collusion happens in the FIL+ application process
- Having a score for Clients, Notaries and Storage Providers that summarizes their collusion activities in past applications can be a good tool to improve and automate the application process.

## Additional reading

- [DataCap application](https://github.com/filecoin-project/filecoin-plus-client-onboarding)
- [FIL+ dashboard](https://filplus.d.interplanetary.one/)
- [DataCap application funnel analysis](https://observablehq.com/@starboard/filplus-ldn-application-funnel)
- [Heterogeneous Network Motifs](https://arxiv.org/abs/1901.10026)
- [Community detection in graphs](https://arxiv.org/abs/0906.0612)
- [Clustering coefficient from Wiki](https://en.wikipedia.org/wiki/Clustering_coefficient)