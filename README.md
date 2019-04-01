# POMCTS For Leduc Hold'em

This repository contains an implementation of the Monte Carlo Tree Search 
algorithm applied to the game of Leduc Hold'em.
The algorithm is based on [this](https://papers.nips.cc/paper/4031-monte-carlo-planning-in-large-pomdps.pdf) 
2010 paper by Silver and Veness.

This algorithm is then extended to apply to extensive form games based on the procedure 
outlined by Heinrich [here](http://discovery.ucl.ac.uk/1549658/1/Heinrich_phd_FINAL.pdf) (chapter 3)

This code resides mainly in the mcts.py module, with other modules being used for 
utility functions, performance evaluation, strategy persistence and invocation.
The ui package defines a game that allows a user to play against the trained agent.

NOTE: This repository utilises the seaborn and PyQt5 modules.
In order to successfully generate metrics and run the game UI these modules 
must be installed.