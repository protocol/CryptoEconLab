<p align="center">
  <a href="https://cryptoeconlab.io" title="CryptoEconLab">
    <img src="https://user-images.githubusercontent.com/25029171/149471901-e6ea751d-b030-4bf3-bb2e-f1ac54c14db2.png" width="140" />
  </a>

</p>

# CryptoEconLab

**Welcome to the CryptoEconLab public repository. Here you will be able to learn about and contribute to our Open Problems, RFPs, and Research Projects, as well as keep tabs on what we're planning for the future.** You can learn more about our lab in our [website](https://cryptoeconlab.io/) and the [Protocol Labs Research webpage](https://research.protocol.ai/groups/cryptoeconlab/). You can also follow us on [Twitter](https://mobile.twitter.com/cryptoeconlab) to keep taps on relevant discussions and information.
## Table of Contents

- [The CryptoEconLab](#cryptoeconlab)
  - [Mission & Vision](#mission--vision)
- [Research](#research)
  - [Open Problems](#research)
  - [Projects](#research)
  - [Collaborations](#collaborations)
- [Team](#team)
- [Community](#community)
- [Publications, Talks, & Tutorials](#publications-talks--tutorials)
- [Contact](#contact)

## `CryptoEconLab`

Cryptoeconomics is an emerging field of economic coordination games in cryptographically secured peer-to-peer networks. As an interdisciplinary study, cryptoeconomics involves a constellation of knowledge including computer science, network science, statistics, psychology, decision neuroscience, economics, and system engineering. In an increasingly networked and open world, cryptoeconomics will play a bigger role in coordinating human and machine activities and building a better future.

### Mission & Vision

CryptoEconLab is Protocol Lab's hub for research on economic incentives, coordination game theory, and novel marketplaces. We aim to develop capacity to design, validate, deploy, and govern large-scale economic systems. CryptoEconLab strives to empower projects in the ecosystem through novel incentives and advance humanity’s understanding of multiagent systems and algorithmic steering of economic networks.

We are applying our learnings to grow and maintain the Filecoin ecosystem, where we are active drivers and participants. Filecoin is a layer1 blockchain that orchestrates a decentralized data storage network designed to store humanity’s most important information - and Filecoin’s unique cryptoeconomic system is central to its design.

## Research

CryptoEconLab’s current focus areas are:

- Incentive & token design
- Optimal pricing and resource allocation in distributed networks
- Real-world experience & business impact
- Network analytics & data-driven monitoring
- Formation, diffusion, and learning in networks
- Modeling & simulation
- Value attribution and graph-based algorithms
- Evolutionary game theory, population games, state-based potential games
- Prediction markets, automated market makers, reputation systems
- Governance process & principles


### Open Problems

We welcome discussion of our [current Open Problems](https://github.com/protocol/CryptoEconLab/tree/main/Open_Problems) on our [github discussion page](https://github.com/protocol/CryptoEconLab/discussions/categories/ideas-open-problems-and-proposals). Please join us in exploring the future of cryptoeconomics by contributing to the solution of current problems and posing new ones! 

<table>
  <thead>
    <tr>
      <th><b>Research Area</b></th>
    <th><b>Open Problem(s)</b></th>
    <th><b>Short Description</b></th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td rowspan="3">General Incentive Research</td>
      <td> 
<a href="https://github.com/protocol/CryptoEconLab/blob/main/Open_Problems/incentivized_network_formation.md">Incentivized Network Formation</a>
</td>
      <td rowspan="3">General problems related to incentivizing behavior in cryptoeconomic networks</td>
   </tr><tr>
      <td> <a href="https://github.com/protocol/CryptoEconLab/blob/main/Open_Problems/truthful-games.md">Truthful Games for Incentives under Unreliable Signals</a></td>
    </tr><tr>
      <td><a href="https://github.com/protocol/CryptoEconLab/blob/main/Open_Problems/value_attribution.md">Value Attribution in a Network of Contributions</a></td>
     </tr>
       <!--<tr>
      <td rowspan="3">Area 2</td>
      <td>open problem 1</td>
      <td rowspan="3">description 2</td>
    </tr><tr>
      <td>open problem 2</td>
    </tr><tr>
      <td>open problem 3</td>
    </tr>-->
  </tbody>
</table>

### Projects 

In addition to our current [Open Problems](https://github.com/protocol/CryptoEconLab/tree/main/Open_Problems), CryptoEconLab has developed a set of research questions that can be used to develop an MSc thesis or PhD  industry-experience project for students in computer science, statistics, complexity, economics or related areas. These questions can also serve as the basis for independent postdoctoral research.

These project ideas can be discused on the [CryptoEconLab Discussion Board](https://github.com/protocol/CryptoEconLab/discussions); inquiries about opportunities for [grant-supported research](https://grants.protocol.ai/) can be directed to [research-grants@protocol.ai](mailto:research@protocol.ai).


#### Project  area 1: Scaling structure and network stability
Self-organized criticality provides a framework to reason about relaxation events with burst-like scale invariant power laws[1]. It’s the common thread across complex systems that links the dynamics of the natural world, from rainfall (think relaxations in the sky!) and earthquakes, to social network tweet storms[2], and rare events in volatile financial markets[3]. 

The Filecoin decentralized network generates millions of unique events per day. We'd like to understand the emergent scaling structure of event cascades, and how this structure  can inform the economic impact of rare events on future network stability. 

These questions might be explored in the context of modeling [Filecoin circulating supply](https://filecoin.io/blog/filecoin-circulating-supply/), understanding the dynamic adjustment of base fees, and examining relationships between storage deal state transitions and other protocol activities. For example, Filecoin uses EIP1559-style[4] gas fees, but how effective are they in practice at regulating volatility[5] in the network, and can a more effective structure be designed?

##### Related resources
1.  [Rain: Relaxations in the Sky](https://arxiv.org/pdf/cond-mat/0204109.pdf) 
    
2.  [A tutorial on Hawkes Processes for events in social media](https://arxiv.org/pdf/1708.06401.pdf) 
    
3.  [State dependent Hawkes processes and their application to limit order book modelling](https://arxiv.org/abs/1809.08060) 
    
4.  [ETH EIP1559](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1559.md) 
    
5.  [EIP1559 empirical analysis](https://arxiv.org/pdf/2201.05574.pdf)


#### Project area 2: using machine learning to model the Filecoin network

The Filecoin network has a near-perfect record of storage provider state, with sector events across the network reported at 30-second intervals. Despite this wealth of data, our understanding is still restricted by the difficulty of interpreting time-changing interactions between pairs of nodes. Yet understanding mutualism and reciprocity, rent-seeking, community structure, sparsity and degree heterogeneity on the network are critical to building a deep understanding of cryptoeconomic dynamics. 

We seek to employ machine learning approaches to model this data-rich system. We are particularly interested in approaches involving models furnished with the appropriate inductive biases,  e.g. mutually self-exciting temporal models [1] and deep graphical neural nets [2]. We believe that machine learning may be particularly useful in modeling the Filecoin [sector lifecycle](https://spec.filecoin.io/systems/filecoin_mining/sector/lifecycle/) and develop optimal responses to network fault events.

##### Related resources
1.  [Modelling sparsity, heterogeneity, reciprocity, and community structure in temporal interaction data](https://proceedings.neurips.cc/paper/2018/file/160c88652d47d0be60bfbfed25111412-Paper.pdf) 
    
2. [GNNs: A review of methods and applications](https://arxiv.org/ftp/arxiv/papers/1812/1812.08434.pdf)


#### Project  area 3: implementing optimal control in a blockchain system

This  problem is about using online optimal control to update tokenomic parameters in a systematic way. Filecoin mainnet has been live for over a year. The decentralized network relies on key parameters to ensure stable dynamics and agent alignment through incentivized behaviors. One challenge is online optimization of parameters that define the mechanistic structure of the protocol. On a technical level, this is akin to tuning the engine of a 747 while it’s off the ground, and leads to a classic high-stakes exploration/exploitation trade-off[1].  

Work on this project may benefit from considering how the lessons of the optimal control literature can be applied to blockchains. We seek to develop an understanding of what optimal search on a live mainnet looks like, and how decisions from a computational protocol might be combined with a human governance layer. This project is about developing an optimal theoretical framework, but potentially has a strong practical element – deciding when and by how much to update blockchain network parameters is becoming a bigger issue[2,3,4] as chains mature. 

##### Related resources
1.  [A tutorial on Thompson Sampling](https://web.stanford.edu/~bvr/pubs/TS_Tutorial.pdf) 
    
2.  [EIP-1559](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1559.md) 
    
3.  ["Tokenomics is back (thanks to CRV)"](https://doseofdefi.substack.com/p/tokenomics-is-back-thanks-to-crv?utm_source=url) 
    

4. ["Yearn Finance Changes Up its Tokenomics and YFI Soars 85%"](https://thedefiant.io/yearn-tokenomics-change/)


#### Project  area 4: injecting stochasticity into Web3 game environments

This project sits at the intersection of web3 games, stochastic processes, and tokenomics. Axie Infinity breeding creates offspring distributed as a birth-death process in which each generation gives rise to exactly two offspring, and effective death occurs according to sterilization after seven breeding cycles to avoid token issuance inflation[2]. One generalization is to introduce stochasticity to breeding, as we see in biology. In the simplest instance the offspring distribution could be Poisson-distributed. This specific case often produces branching dynamics with a closed-form solution for the mean and variance of the population, for which the tokenomic scheduling could in theory be specified analytically. 

Some interesting questions concern how far the idea of injecting randomness be pushed;  the behavioral psychology context of randomized rewards;  the consequences in terms of the burning and minting schedule for token design; and, given a such an issuance schedule, discovering what a 'good' outcome looks like.

##### Related resources
1. [Axie Infinity whitepaper: breeding](https://whitepaper.axieinfinity.com/gameplay/breeding)

### RFPs
  
 As we develop and post RFPs, they will be posted in [this github repo](https://github.com/protocol/research-RFPs).
  
### Collaborations
  
We are very interested in forming collaborations with researchers and engineers working in our fields of interest, and we offer several grants and research fellowships to support these working relationships. Please check out the [PL Research website](https://research.protocol.ai/outreach/) for further details and application instructions.

## Community

Please join us for discussion an  anything in the CryptoEconLab extended universe on our [discussion forum](https://github.com/protocol/CryptoEconLab/discussions/)
  
## Publications, Talks, & Tutorials

You can vew our current slate of publications, talks, and other resources on [our lab webpage](https://research.protocol.ai/groups/cryptoeconlab/).


## Team 👨🏽‍🚀

- [Zixuan (ZX) Zhang](https://research.protocol.ai/authors/zixuan-zhang/)
- [Alex Terrazas](https://research.protocol.ai/authors/alex-terrazas)
- [Axel Cortés Cubero](https://research.protocol.ai/authors/axel-cortes-cubero)
- [Tom Mellan](https://research.protocol.ai/authors/tom-mellan/)

###  Hiring 🚀

We are working to expand the team -- if you're a scientist or engineer interested in cryptoeconomics research, visit PL's [jobs page](https://boards.greenhouse.io/protocollabs) to learn more and apply! 

## Contact

You can reach out to us anytime with your questions and interest in these projects by emailing [research@protocol.ai](mailto:research@protocol.ai)
