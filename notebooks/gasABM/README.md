This is an ABM  to simulate gas in Filecoin (or ethereum if you make miner demand for gas =0)

This readme is heavily under construction, but will update asap
These are the files

- driver.py This is used to set up the simulation parameters (number of users, number of miners, demand profiles, etc). it invokes the ABM.py module
- ABM.py Main simulation loop for the ABM model
- constants.py encondes some universal constants
- demandProfiles.py aux file to include demand profiles. Please folloe the template of this file when including one
-	transaction.py module for the transaction class
-	baseFee.py	module for the base fee class
-	user.py module for the user agent. 
- blockStrategies.py	module to decide how trx are included in blocks
- mempool.py a module fot the mempool object
- chain.py	a module for the chain object	
- miner.py



Will provide a tutorial soon, but how to use: change parameters in driver.py and run it. 
