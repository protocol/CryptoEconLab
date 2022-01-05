# Incentivized Network Formation

## Introduction to the Problem

Traditional network formation literature has focused on coming up with models to explain how networks are formed: random graphs, the [Erdős–Rényi model](https://www.renyi.hu/~p_erdos/1959-11.pdf) for the evolution of random networks, the [Watts–Strogatz model](http://worrydream.com/refs/Watts-CollectiveDynamicsOfSmallWorldNetworks.pdf) for the generation of random graphs with small world properties, the [Price](https://www.science.org/doi/10.1126/science.149.3683.510) and  [Barabási–Albert model](https://arxiv.org/abs/cond-mat/0106096) introducing a preferential attachment mechanism, and the [Expander Graphs](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.393.1430&rep=rep1&type=pdf) described by Bassalygo and Pinsker. 

Cryptoeconomic networks -- like many other economic and behavioral networks -- present the opportunity to define microeconomic structures that can enable specific targerted macro network structures to emerge. Being able to incentivize the formation of specific network topologies and influence network structural parameters is a powerful tool in token economic design with applications in  geographic incentivization and market and payment network design.

This Open Problem seeks novel methods for the discovery and incentivization of optimal network structures under a variety of conditions.

## State of the Art

### Network Formation Games

Network formation games describe the principles of interaction that determine network structure, which in turn affects economic outcomes -- including whether or not coordination will occur [0](https://authors.library.caltech.edu/79723/1/sswp1160.pdf),[1](https://dir.ilam.ac.ir/mozafar/gt/s15/Nisan_Non-printable.pdf#page=508),[2](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.454.9588&rep=rep1&type=pdf). Understanding the proceses that produce different network configurations is therefore important to understanding how and where value is generated in a network.

Network interaction dynamics can lead self-interested entities to form large and efficient networks[1](https://dir.ilam.ac.ir/mozafar/gt/s15/Nisan_Non-printable.pdf#page=508), but path dependencies during network formation can produce inefficient structures [2](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.454.9588&rep=rep1&type=pdf). Tradeoffs between efficiency and stability in determining network quality can be quantitatively modeled in a game-theoretical framework [3](https://web.stanford.edu/~jacksonm/netsurv.pdf), and we can evaluate network quality using measures asessing various aspects of distance/connectivity, congestion, and cost. 

Research on swarm formation and cooperation (e.g. [4](http://www.ppgia.pucpr.br/~alceu/mestrado/aula3/PSO_2.pdf),[5](https://www.sciencedirect.com/science/article/pii/S0925231219316558), [6](http://utpedia.utp.edu.my/16515/),[7](https://ieeexplore.ieee.org/abstract/document/1655446)) has provided insights into optimizing the search for condition-appropriate topologies and the dynamics of cooperative behaviours in a spatial network that may be relevant to this problem. Swarm research also provides a useful analogy to the problem of creating incentives for individual agents to produce a desired emergent global behaviour, as well as methods for evaluating system performance across a network of numerous agents. The swarm literature also models approaches to the general problem of emergent intelligent collective behaviour under the the important constraints of *scalability*, *robustness*, and *decentralization*.

Additionally, results from game theory and biology have demonstrated the significance of spatial structure in determining interaction dynamics and their resulting equilibria, as well as evidence for the co-evolution of network structure and strategy[8](https://link.springer.com/chapter/10.1007/978-3-642-01284-6_11). These results have interesting implications for dynamic networks in which geography can be considred a salient variable.

### Known shortcomings of existing solutions

Much of the literature related to this topic focuses on  observing, describing,  and modeling the dynamics of network topology emergence. There has been relatively less work on methods of influencing network topology development, particularly in a decentralized or distributed system, which is something that we are now empowered to do with digital tokens.

Additionally, much of the work referenced above is framed in terms of network topology. While network topology is an important factor in deteremining network behavior, CryptoEconLab believes that there may be other parameters relevant to the function of cryptoeconomic networks that are not completely captured by models focused on topological features. We invite the community to use a broad definition of *"network structure"* in conducting its explorations of this question. 

## Solving this Open Problem

We would like to use the principles of interaction gleaned from observations of network formation games to understand the connection between agent (node) behavior and network structure.

We seek solutions explicating the tradeoffs between cost and benefits of (decentralized) network participation for various agents under different conditions and/or optimizing the social cost of a (decentralized) network under various conditions. 

These solutions may be modeled using simulated data or via observations of a live network deployment. 

We invite solutions investigating both topological and non-topological properties relevant to the function of cryptoeconomic networks.

### What does a useful contribution to this problem look like?

A good response to this Open Problem would be the creation of a general framework that can be contextualized for different use-cases, allowing us to explore *a network's reaction to changing incentives*. We are looking for description of the [leverage points](http://www.donellameadows.org/wp-content/userfiles/Leverage_Points.pdf) in a network with predictive power. What are the parameters we can tune to accomplish different objectives?

Your contribution might resemble ZX's [work using state space representations to model blockchain-enabled networks](https://research.protocol.ai/publications/on-modeling-blockchain-enabled-economic-networks-as-stochastic-dynamical-systems/2020zhang.pdf) or Axel's exploration of the [incentives produced by different block reward structures](https://hackmd.io/@R02mDHrYQ3C4PFmNaxF5bw/B1A_BSztt).

### Estimated impact

Improved Network control via decentralized incentive mechanisms will enable new innovations in many systems modeled as a network, including but not limited to:
- Filecoin storage and retrieval market performance improvements 
- improved logistics networks
- more efficient transportation networks and two-sided markets
- improvements to CDN and indexing networks

## Supplementary Material

These papers illustrate interesting approaches to related problems from the broader research ecosystem: 

0.  Jackson, M.O. 2003. [Allocation rules for network games](https://authors.library.caltech.edu/79723/1/sswp1160.pdf)
1.  Tardos, E., and Wexler, T., in Nisan _et al_ 2007. [Algorithmic Game Theory Ch19: Network Formation Games and the Potential Function Method](https://dir.ilam.ac.ir/mozafar/gt/s15/Nisan_Non-printable.pdf#page=508)
2.  Watts, A. 1999. [A Dynamic Model of Network Formation](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.454.9588&rep=rep1&type=pdf)
3.  Jackson, M.O. 2003. [A Survey of Models of Network Formation: Stability and Efficiency](https://web.stanford.edu/~jacksonm/netsurv.pdf)
4.  Eberhardt, R., and Kennedy, J. 1995. [A New Optimizer Using Particle Swarm Theory](http://www.ppgia.pucpr.br/~alceu/mestrado/aula3/PSO_2.pdf)
5.  Xiao, H., _et al._ 2020. [Two-level structure swarm formation system with self-organized topology network](https://www.sciencedirect.com/science/article/pii/S0925231219316558)
7.  Dennis, L.K.H. 2015.[Cooperative Network Formation between Swarm Robots](http://utpedia.utp.edu.my/16515/)
9.  Freeman, R.A., _et al._ 2006. [Distributed Estimation and Control of Swarm Formation Statistics](https://ieeexplore.ieee.org/abstract/document/1655446)
10. Skyrms, B., and Pemantle, R. 2009. [A Dynamic Model of Social Network Formation](https://link.springer.com/chapter/10.1007/978-3-642-01284-6_11)
11. Derks,J., _et al._ 2008. [Local Dynamics in Network Formation](https://dke.maastrichtuniversity.nl/f.thuijsman/local%20dynamics.pdf)
12. Bala, V., and Goyal, S. 2003. [A Noncooperative Model of Network Formation](https://onlinelibrary.wiley.com/doi/abs/10.1111/1468-0262.00155)
13. Hoory, S., _et al._ 2006.[Expander graphs and their applications](https://www.ams.org/journals/bull/2006-43-04/S0273-0979-06-01126-8/S0273-0979-06-01126-8.pdf)
14. Nielsen, M.A. 2005. [Introduction to expander graphs](https://michaelnielsen.org/blog/archive/notes/expander_graphs.pdf)
15. Even-Dar, E. _et al._ [A Network Formation Game for Bipartite Exchange Economies](https://www.cis.upenn.edu/~mkearns/papers/econform.pdf)

### Notes on existing conversations

[Github discussion]() about the Bridges of Koenigsberg Problem and cryptoeconomic networks


