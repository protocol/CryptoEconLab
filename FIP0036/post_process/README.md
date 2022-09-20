# Post-processing scripts


The main file is main.py. This file, essentially, processes each vote by taking the following steps:

      1.Receive a signed vote from X
      2.Validate the signature
      3.Confirm that X exists on chain
        3.1 (if it does) Add X's balance to the Token Holder vote (Group 4))
      4. Iterate over all deals, adding up the bytes of deals where X is the proposer
        4.1 Add these bytes to the client vote (Group 3)
      5.  Iterate over all SPs, checking if X is the owner / worker of an SP Y
        5.1. If it is, AND the SP hasn't already voted:
          5.1.1 Add Y's raw bytes to the SP capacity vote (Group 2)
          5.1.2 Iterate over all deals, adding up the bytes of deals where Y is the provider, add these bytes to Deal Storage vote (Group 1)

This process is contained in the `counting.py` module. The rest of the files are:

`sentinel.py`: module to connect to the sentinel database. IT REQUIRES A CONNECTION STRING STORED AS `SecretString.txt` IN THIS FOLDER.
`datautils.py`: module to query the sentinel database and perform several table-lookup operations
`votes.py`: module with vote data. It connects to the FIlPoll API and queries the up-to-date list of votes
`counting.py`: vpte class.performs the algorithm above for each vote
`groups.py`: group class. 
`preprocess.py`: preprocess chain data.


