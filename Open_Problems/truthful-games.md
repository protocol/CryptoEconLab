
# Truthful Games for Incentives under Unreliable Signals

## Introduction to the problem

Some of the large distributed systems that we are most interested in are best modeled as games of [*incomplete information*](moz-extension://5a397cd6-7082-4c36-a528-b9b0137c872f/pdfjs/viewer.html?file=https://web.stanford.edu/~jdlevin/Econ%20203/Bayesian.pdf), where players don't have common knowledge of various crucial features of the game being played, like possible moves and outcomes, potential payoffs, or even the existence of other players. 

[*Signaling games*](http://econ.ucsd.edu/~jsobel/Paris_Lectures/20070527_Signal_encyc_Sobel.pdf) are an important type of dynamic model with incomplete information. Signaling games are  strategic interactions in which players can use the actions of their opponents to make inferences about hidden information: a player with private information sends a signal to an uniformed player (or players) who acts contingent on the signal. These games have been examined in the context of  understanding the [job market](https://viterbi-web.usc.edu/~shaddin/cs590fa13/papers/jobmarketsignaling.pdf), [product pricing and advertising](https://cowles.yale.edu/sites/default/files/files/pub/d07/d0709.pdf), [insurance](https://www.nber.org/system/files/working_papers/w23556/w23556.pdf), [product warranties](https://faculty.fuqua.duke.edu/~qc2/BA532/1981%20JLE%20grossman.pdf), [bargaining strategies](https://www1.cmc.edu/pages/faculty/MONeill/math188/papers/rubinstein5.pdf), and even [animal behaviour](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.1073.4125&rep=rep1&type=pdf), among numerous other applications.

Much of cryptoeconomics today relies on “provable” signals to construct incentives and mechanisms. However, not all signals are verifiable and many are subject to [“wash trading”](https://www.investopedia.com/terms/w/washtrading.asp), wherein players engage in market activity in order to mislead other players in the market.  

In the large distributed networks CryptoEconLab is studying, it is difficult to verify the truthfulness of the signals players send. When protocols can’t rely on cryptographic primitives to restrain undesirable behaviours, it is natural to look into economic games that can align participants' incentives with that of the system. We therefore wish to design games with payoff structures encouraging truth-telling as the optimal action for rational players: designs in which truth-telling by all players forms a Bayesian Nash equilibrium. We are also inrterested in exploring deviations from this equilibrium related to the rationality assumption.

There is a parallel between this framing and that of DSIC games where truth-telling is a dominant strategy.

This Open Problem seeks game models describing mechanisms for incentiving truth telling in distributed multiplayer signalling game. We are particularly interested in discovering whether there exists a subclass of actions that can be incentivized without being proven.

## State of the Art

### Current approaches within the CryptoEconLab and broader research Ecosystem

This Open Problem stems from our current work in the field of [algorithmic mechanism design](http://www.cs.cmu.edu/~sandholm/cs15-892F07/Algorithmic%20mechanism%20design.pdf), particularly in the area of [retrieval mining](https://retrieval.market/).   

We see parallels between this Open Problem and explorations of **truthful mechanism design** in [facility location](https://www.ifaamas.org/Proceedings/aamas2019/pdfs/p1470.pdf), [congestion games](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.768.8075&rep=rep1&type=pdf), and [combinatorial auctions](https://www.aaai.org/Papers/AAAI/2002/AAAI02-058.pdf). 

These examples illustrate approaches to related problems under additional constraints, such as polynomial mechanism runtime and feasibility within a global budget. 

The design of the [CacheCash decentralized CDN network](https://academiccommons.columbia.edu/doi/10.7916/d8-kmv2-7n57) includes a defense against cache accounting attacks that rests partially upon making honesty more profitable than cheating. Game designs that make dishonest behaviour costly arem a potential approach to this problem.

### Known shortcomings of existing solutions

Some of the above games rely on or assume a central authority (e.g. the goverment planning to locate a [facility](https://www.ifaamas.org/Proceedings/aamas2019/pdfs/p1470.pdf)) and will need to be modified to better fit a decentralized context with explicit financial incentives where it is difficult or impossible to prove that any particular action was performed.

[Vickrey](http://www.cs.princeton.edu/courses/archive/spring09/cos444/papers/vickrey61.pdf)-[Clarke](https://www.jstor.org/stable/30022651)-[Groves](http://www.eecs.harvard.edu/cs286r/courses/spring02/papers/groves73.pdf) (VCG) mechanisms are truthful, and maximize social welfare, but have high computational complexity and may require the implementation of [additional functions](http://robotics.stanford.edu/~amirr/vcgbased.pdf) to be made feasible. 

These are minor shortcomings relative to the major problem: the difficulty of eliciting private information that is technically unverifiable.


## Solving this Open Problem

### What does a useful contribution to this problem look like?

Game models should take place in a decentralized system.

Any proposed mechanisms should be **truthful** --  the optimal strategy for each player is to send an honest signal/report accurate information -- and **individually rational** -- all participants benefit from the game. When appropriate, solutions should include an analysis of the mechanism's performance against a selected **objective function**.

We are particularly interested in discovering whether there exists a subclass of actions that can be incentivized without being proven. 

We believe that useful contributions can be derived from modeling this question as a general problem with private belief: establishing general rules such that the private belief in question remains unknown,  but it is incentive-compatible to reveal it. We seek to identify the bounds constraining the revelation of the private belief.

### Estimated impact

It is expected that solutions to this Open Problem will contribute to the design of new truthful mechanisms, and that this will enable improvements in networked [data storage](https://filecoin.io/), computation,  and [retrieval markets](https://retrieval.market/) and internet routing- related protocols, among other uses. 

## Related Reading 

 1.  Hörner, J.,  _et al._ 2015. [Truthful Equilibria in Dynamic Bayesian Games](https://elischolar.library.yale.edu/cgi/viewcontent.cgi?article=3330&context=cowles-discussion-paper-series)
	
 2. Chen, X., _et al._ 2019.  [Truthful Mechanisms for Location Games of Dual-Role Facilities](https://www.ifaamas.org/Proceedings/aamas2019/pdfs/p1470.pdf)
	
 3.  Rogers, R., and Roth, A.  2013. [Asymptotically truthful equilibrium selection in large congestion games ](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.768.8075&rep=rep1&type=pdf)
	
 4.  Kao, M-Y., _et al._ 2005. [Towards truthful mechanisms for binary demand games](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.83.9640&rep=rep1&type=pdf)
	
5. Mu’alem, A., and Nisan, N. 2002. [Truthful approximation mechanisms for restricted combinatorial auctions](https://www.aaai.org/Papers/AAAI/2002/AAAI02-058.pdf)
	
6. Almashaqbeh, G. 2019. [CacheCash: A Cryptocurrency-based Decentralized Content Delivery Network](https://academiccommons.columbia.edu/doi/10.7916/d8-kmv2-7n57) ([related powerpoint](https://ghadaalmashaqbeh.github.io/slides/abc-cryblock-2019.pdf))
	
7. Almashaqbeh, G., _et al._ 2019. [CAPnet: A Defense Against Cache Accounting Attacks on Content Distribution Networks](https://ssl.engineering.nyu.edu/papers/almashaqbeh_capnet_cns19.pdf)
	
8. Feldman, M., _et al._ 2021.[Distributed Signaling Games](https://arxiv.org/pdf/1404.2861.pdf)
