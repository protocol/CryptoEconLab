# Concentration in Filecoin storage mining and network attacks

## Introduction to the problem

Filecoin is a decentralized storage network. Here, Storage Providers (SPs) contribute storage to the network and, in turn, receive a proportional claim on network consensus and block rewards. This means that the Storage Provider with the most storage capacity is also the participant with the largest consensus stake. Thus, the most direct way of measure concentration of "power" on Filecoin is to assess concentration of storage capacity.

Why is this important? The more concentrated the network consensus is, the more fragile it is to takeovers by a small set of individuals, which can be disastrous. By taking control of the network, an attacker can meddle with the underlying transaction infrastructure and extract value from the network. This [scenario happened to Bitcoin Gold](https://qz.com/1287701/bitcoin-golds-51-attack-is-every-cryptocurrencys-nightmare-scenario), a fork of Bitcoin with smaller market cap and hashrate). In 2018, an attacker took control of more than half of the network consensus power (which, in this case, is the hashrate) and was capable of defrauding a few exchanges. These 51% attacks happened as well to [Verge](https://thenextweb.com/news/hackers-verge-blockchain-steal-1-7m), [Monacoin](https://www.ccn.com/japanese-cryptocurrency-monacoin-hit-by-selfish-mining-attack/) and [Electroneum](https://thenextweb.com/news/hackers-verge-blockchain-steal-1-7m).

Going back to Filecoin, the protocol has a few features that make it harder for attacks willing to take over the network. Firstly, in order to gain storage capacity in the network, operators need to do some "physical" work" (i.e. buy and maintain storage hardware and do some heavy computation to process the storage when it is first being added to the network). In addition, operators need to submit collateral proportional to the storage capacity they are adding to the network.

The combination of "physical" work" and staking leads to the cost of onboarding a certain amount of storage and, thus, these onboarding costs per unit of storage directly impact the security of Filecoin against takeover attacks. Another factor that impacts Filecoin's security is the current capacity in the network. The larger the capacity, the harder it is to gain a large share of the consensus power. Thus, understanding these costs is key to understand how safe the network is against such attacks. Note that the costs vary with time, with both the total storage capacity and the onboarding costs per unit of storage varying historically.

Another important aspect of analyzing the security of the network is assessing how concentrated the network currently is. In order words, how much would it cost if the Storage Provider with the most consensus power wanted to take over the network? And what if the top two or top five Storage Providers colluded to take over the network?

To answer these questions, one needs to estimate the onboarding costs per unit of storage, similarly to analysis for a new attacker. However, there is an additional step is not straightforward. The main way of identifying Storage Providers within the Filecoin network is through their miner ID. However, because the network is pseudoanonymous, there is no registration stopping providers to create multiple miner IDs. Thus, there needs to be some work around clustering the miner IDs into their ultimate Storage Provider.

Finally, it is important to understand what is the consensus power share threshold where an attacker could start ti cause harm to the network. The team at ConsensusLab found an [attack that only requires a 20%](https://github.com/filecoin-project/FIPs/discussions/501). At the same time, they propose a fix that would increase the share to 44%. Thus, for the scope of this analysis, we are interested in investigating both cutoffs (20% and 44%).

### Research questions

1. What is the cost for an attacker without any previous storage capacity in Filecoin to achieve a 20% or 44% share of the storage power? How has the cost evolved since the launch of the network?
2. Can we cluster miner IDs into their ultimate Storage Provider?
3. How concentrated is the Filecoin network, both in terms of miner IDs and Storage Providers?
4. What is the cost for the top Storage Provider to achieve a take a 20% or 44% share of the storage power? How has these cost evolved since the launch of the network?
5. How many Storage providers need to collude to take over the network?


## Solving this problem

Solving this problem will involve three main stages:

1. Estimate the current and historical cost for a 20% takeover and a 44% takeover.
   1. Understand the costs associated with onboarding a single unit of storage in the Filecoin network. This [dashboard](https://dashboard.starboard.ventures/capacity-services) and this [calculator](https://observablehq.com/@starboard/sproi) can be good starting points.
   2. Extract how much power needs to be added to reach the desired power share by a newcomer. The dashboard linked above is another good source of data.
2. Group miner IDs into the ultimate Storage Provider. This is the task with the most room for exploration and innovation. Some possible approaches include: 
   1. Analyzing the blockchain activity to find ownership links and financial links. The [Lily dataset](https://lilium.sh/data/) is a good source for this task.
   2. Analyzing information from off-chain sources such as [FIL+ applications](https://github.com/filecoin-project/filecoin-plus-client-onboarding) or the auction market [BigDataExchange](https://www.bigdataexchange.io/)
3. Estimate the current and historical cost for a takeover of the top Storage Providers and how much collusion would be needed. This stage mostly combines the previous two stages.

### Estimated impact

1. Have a clearer view on the current safety of the Filecoin network
2. Guide future discussions about changes in economic parameters such as collateral.

## Additional reading

- [Understanding Filecoin Circulating Supply](https://filecoin.io/blog/filecoin-circulating-supply/)
- [Filecoin's cryptoeconomic constructions](https://filecoin.io/blog/posts/filecoin-s-cryptoeconomic-constructions/)
- [Filecoin collateral spec](https://spec.filecoin.io/#section-systems.filecoin_mining.miner_collaterals)
- [Filecoin consensus spec](https://spec.filecoin.io/algorithms/expected_consensus/)