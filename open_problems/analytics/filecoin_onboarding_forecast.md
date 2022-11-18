# Detection of collusion communities in the FIL+ program

## Introduction to the problem

Filecoin is a decentralized storage network. Here, Storage Providers (SPs) contribute storage to the network and, in turn, receive a proportional claim on network consensus and block rewards. Therefore, storage capacity is the single most important metric of growth for Filecoin.

Every day, we see some new storage being onboarded by both existing and new providers. On the other end, every day, some storage is terminated or expired, and the respective capacity exits the network. The net effect of these two time-series (onboardings and exits) results in the [daily changes observed in the total storage capacity of Filecoin](https://observablehq.com/@starboard/chart-network-storage-capacity). In this project, we are interested in the new storage entering the network every day (i.e., the onboardings).

Another important factor to storage onboarding is the committed duration. Every day, Storage Providers have two decisions:
1. How many sectors are they adding? *Note that a sector in Filecoin is a unit of storage*.
2. For how long each sector will be committed.

Currently, Storage Providers can commit sector for periods between 6 months and 1.5 years. So, besides forecasting how many sectors are onboarded, it is also key to forecast the duration of those sectors.


### Research questions

1. Does time-series forecasting methods work for predicting storage onboarding in Filecoin?
2. Does splitting the forecast by miner ID improve the model performance?
3. Can we categorize miner IDs into similar onboarding profiles? Does this split help with forecasting?

## Solving this problem

The ultimate goal of this project is to design good forecasting models for Filecoin storage onboarding. The base model would be to forecast directly on the aggregate storage being onboarded by the network each day. Here, one can test multiple models, including classical time-series models such as ARMA or ARIMA, and more recent model such as LSTMs.

After this first model, we then want to split the forecasting task by miner ID or by groups of miner IDs. More concretely, the idea is to split the historical storage onboarding time-series into a set of miner-level time series and then apply forecasting to each time-series independently. To get the total onboarding forecast, one would add the individual time-series. The underlying assumption is that the past onboarding rates of individual Storage Providers are a good predictor of their short-term behavior. 

### Estimated impact

Being able to forecast the storage onboarding capacity of the Filecoin network will be extremely helpful to the community (Filecoin participants can use it to plan their operations) and to the CryptoEconLab team (our lab can take advantage of the models to guide our planing and design of economic policies).

## Additional reading

- [Historical time-series of daily changes in Filecoin's storage capacity](https://observablehq.com/@starboard/chart-network-storage-capacity)
- [Sector onboarding time-series](https://observablehq.com/@starboard/chart-prove-commit-32-64-gib-splits)
- [Lily dataset](https://lilium.sh/data/)