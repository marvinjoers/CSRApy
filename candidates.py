# candidates.py 

import os
from ast import literal_eval
import operator
import ast

# arrays

Original_Candidates = []
Candidates = []
Path1_Sessions = []
Multi_Sessions = []

# antiDuplicate
# method to save unique nodes

duplicate = {}
def antiDuplicate(candidate):
    
    global duplicate
    if candidate in duplicate:
        return True
    else:
        duplicate[candidate] = 1 
        return False

# getRedirectURL: check redirected status
# 302.REDIRECTS.txt contains a dictonary: {'REDIRECT_URL': 'TARGET_URL', 'REDIRECT_URL': 'TARGET_URL', ...}

with open('302.REDIRECTS.txt',"r") as r:    
    R_as_String = r.read()
R = ast.literal_eval(R_as_String)
                      
def getRedirectURL(el):
    if el in R:
        el = R[el]
        return el
    else:
        return el

# read original sequences from web logs (already pre-processed as arrays in array: [['url1', 'url2'], ['url1', 'url2', 'url3'], ...]
with open("ORIGINAL_SEQUENCES.txt","r") as r:
    Candidates_as_String = r.read()
Original_Candidates = literal_eval(Candidates_as_String)


# remove redirects proactively
No_Redirects = []
for OC in Original_Candidates:
    TempC = []
    for Node in OC:
        TempC.append(getRedirectURL(Node))
    No_Redirects.append(TempC)

# read candidates
count = 0
for Session in Candidates:
        if not Session:
            continue
        if len(Session) == 1:
            Path1_Sessions.append(Session) # 1Path-Sessions
            count = count + 1
        else:
            Multi_Sessions.append(Session) # Path+-Sessions
            count = count + 1

# Pre-processing
Multis = []

for S in Multi_Sessions:
    tempArray = []
    # remove duplicates from array
    path = list(dict.fromkeys(tempArray))
    # protocol handling
    path = [p.replace('http://', 'https://') for p in path]
    
    if len(path) == 1:
        Path1_Sessions.append(path)
    else:
        Multis.append(path)
    
print("Sessions with one node: " + str(len(Path1_Sessions)))
print("Sessions with multiple nodes: " + str(len(Multis)))
print("All Sessions: " + str(count))

# Save both as txt
with open('CSRA.v2.1Path.Candidates.txt', 'w') as p1:
    p1.write(str(Path1_Sessions))
with open('CSRA.v2.Multi.Candidates.txt', 'w') as p2:
    p2.write(str(Multis))

