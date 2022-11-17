# Using machine learning to model the Filecoin network

The Filecoin network has a near-perfect record of storage provider state, with sector events across the network reported at 30-second intervals. Despite this wealth of data, our understanding is still restricted by the difficulty of interpreting time-changing interactions between pairs of nodes. Yet understanding mutualism and reciprocity, rent-seeking, community structure, sparsity and degree heterogeneity on the network are critical to building a deep understanding of cryptoeconomic dynamics. 

We seek to employ machine learning approaches to model this data-rich system. We are particularly interested in approaches involving models furnished with the appropriate inductive biases,  e.g. mutually self-exciting temporal models [1] and deep graphical neural nets [2]. We believe that machine learning may be particularly useful in modeling the Filecoin [sector lifecycle](https://spec.filecoin.io/systems/filecoin_mining/sector/lifecycle/) and develop optimal responses to network fault events.

##### Related resources
1.  [Modelling sparsity, heterogeneity, reciprocity, and community structure in temporal interaction data](https://proceedings.neurips.cc/paper/2018/file/160c88652d47d0be60bfbfed25111412-Paper.pdf) 
    
2. [GNNs: A review of methods and applications](https://arxiv.org/ftp/arxiv/papers/1812/1812.08434.pdf)