# Baseline crossing analysis

### June 2022

## Overview 

Filecoin uses a hybrid model for mining that incorporates two minting mechanisms - Simple minting and Baseline minting. 
Simple minting is the most common minting we see in other blockchains, where newly minted tokens follow a simple exponential decay model. This type of minting aims to encourage early adoption since the number of new tokens awarded to miners gets exponentially smaller as time goes on. 

In order to encourage long-term storage and to align incentives with the growth of the network’s utility, Filecoin introduced Baseline minting. The team defined a baseline function that determines the expected level of growth for the network. The tokens reserved for Baseline minting are only distributed if the network as a whole achieves or goes beyond that predefined growth goal. Thus, if storage providers don’t onboard storage at the expected rate, the network will not mint at full speed and the total rewards distributed will be lowered. When the network achieves the growth goals, tokens are minted at full capacity and follow a “normal” exponential decay.

In April 2021, the network crossed the baseline function and started to grow faster than the initial goal. This was a major milestone for Filecoin (more info here). Since then, the network has been minting tokens at full speed since the network has managed to maintain a high growth rate. However, current market conditions (e.g. China’s crackdown, crypto market crash, etc.) are putting pressure on the Storage Providers (SPs) and their growth capability.

The goal of this project is to investigate this problem and understand the potential consequences of the network experiencing a downward baseline crossing. In particular, we will estimate the likelihood of observing a baseline crossing assuming current market conditions, we will model the consequences of that event for both SPs and the network as a whole, and we will look into potential mitigation strategies.

The work is divided into 4 main milestones:

1.  BlockScience work review *[skipped due to time constrains]*
2.  Baseline Crossing prediction *[completed]*:
    - [Power model spec v1](https://hackmd.io/@msilvaPL/H1uuNlItq)
    - [Power model spec v2](https://hackmd.io/@msilvaPL/SkapZkrdc)
    -  [Power scenarios analysis](https://hackmd.io/@msilvaPL/SJHCpzBuc)
3.  Side effects modeling *[theoretical document started, but not completed]*:
    - [Impact on minting and rewards](https://hackmd.io/@msilvaPL/ry6ZDtNK9)
4.  Mitigation mechanisms and information sharing *[not started]*

## Inside this folder

This folder contains all the code and analysis done for the Baseline crossing analysis. Currently, it only includes the work done for Milestone 2:

- `power_analysis.ipynb`: EDA about historical network power statistics
- `power_forecast.ipynb`: v1 analysis of four possible scenarios for network power evolution. This notebook uses the old model coded in `power_model.py`
- `power_forecast_v2.ipynb`: v2 analysis of four possible scenarios for network power evolution. This notebook uses the newer v2 model coded in `power_model_v2.py`
- `power_model.py`: code of the old model to forecast power statistics
- `power_model_v2.py`: code of the version 2 model to forecast power statistics
- `sector_updates_trends.ipynb`: EDA about sectors expiration and renewals

## Requirements

```
altair==4.2.0
jupyterlab==3.4.2
numpy==1.22.4
pandas==1.4.2
requests==2.27.1
```

## Additional documentation

- [Project docs](https://hackmd.io/@cryptoecon/Bkit3d6ej/%2F96OArWoLQvu1HtSnfwgrnQ)