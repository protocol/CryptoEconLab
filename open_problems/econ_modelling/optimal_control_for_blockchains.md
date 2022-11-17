# Implementing optimal control in a blockchain system

This problem is about using online optimal control to update tokenomic parameters systematically. Filecoin mainnet has been live for over a year. The decentralized network relies on key parameters to ensure stable dynamics and agent alignment through incentivized behaviors. One challenge is online optimization of parameters that define the mechanistic structure of the protocol. On a technical level, this is akin to tuning the engine of a 747 while it’s off the ground, and leads to a classic high-stakes exploration/exploitation trade-off[1].  

Work on this project may benefit from considering how the lessons of the optimal control literature can be applied to blockchains. We seek to develop an understanding of what optimal search on a live mainnet looks like, and how decisions from a computational protocol might be combined with a human governance layer. This project is about developing an optimal theoretical framework, but potentially has a strong practical element – deciding when and by how much to update blockchain network parameters is becoming a bigger issue[2,3,4] as chains mature. 

##### Related resources
1.  [A tutorial on Thompson Sampling](https://web.stanford.edu/~bvr/pubs/TS_Tutorial.pdf) 
    
2.  [EIP-1559](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1559.md) 
    
3.  ["Tokenomics is back (thanks to CRV)"](https://doseofdefi.substack.com/p/tokenomics-is-back-thanks-to-crv?utm_source=url) 

4.  ["Yearn Finance Changes Up its Tokenomics and YFI Soars 85%"](https://thedefiant.io/yearn-tokenomics-change/)