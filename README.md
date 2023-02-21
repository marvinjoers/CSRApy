# CSRApy
Python Version of the Complete Session Reconstruction Algorithm

Primarily based on pseudo-code by https://link.springer.com/article/10.1007/s11280-022-01024-3 (Bayir & Toroslu, 2022)

1) candidates.py (pre-processing)
2) topology.py - create topology (multiple database concepts possible)
3) phase2.py (generate max paths)
4) bayes-predictor.py (next page prediction via bayes simulator)


Example (https://link.springer.com/article/10.1007/s11280-022-01024-3, valid results by using original examples) 

i = 2
Candidates = [['P1', 'P20', 'P23', 'P13', 'P34'], ['P1', 'P2', 'P4', 'P3', 'P7']] 
Links = [{'P1': ['P13', 'P20'], 'P13': ['P34'], 'P20': ['P23']}, {'P1': ['P2', 'P3'], 'P2': ['P3', 'P4'], 'P3': ['P6', 'P7']}]

# phase2.py (CSRA Phase 2)

Output: O = [['P1', 'P20', 'P23'], ['P1', 'P13', 'P34'], ['P1', 'P2', 'P4'], ['P1', 'P2', 'P3', 'P7'], ['P1', 'P3', 'P7']]
