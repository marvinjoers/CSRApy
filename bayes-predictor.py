# bayes-predictor.py

from ast import literal_eval
import re
import ast
import random
import pymongo

# load all aprioriALL support values, alternative database solutions possible
myclient = pymongo.MongoClient("mongodb://___")
mydb = myclient["___"]
mycol = mydb["___"]

# Load Original Sequence
original_sequences = []

# Load Dataset of 1Path Candidates
with open('CSRA.1Path.Candidates.txt',"r") as r:  # see candidates.py
    einPfad_as_String = r.read()
einpfad = ast.literal_eval(einPfad_as_String)

for pfad in einpfad:
    original_sequences.append(pfad)
    
# Load Dataset of Multi Candidates
with open('CSRA.Multi.Candidates.txt',"r") as r: # see candidates.py
    multiPfad_as_String = r.read()
multipfad = ast.literal_eval(multiPfad_as_String) 
multipfad = sorted(multipfad, key=len)

for pfad in multipfad:
    original_sequences.append(pfad)

# function: randomize
# Creates the random dataset to simulate a possible prediction

test_data = [] # [[X,Y,...], Z]; [X,Y] = Shorted original array and Z represents the original value k+1

def randomize(sequences):
    for s in sequences:
        if len(s) > 1:
            k = random.randint(0, len(s)-2)
            test_sequence = []
            i = 0
            while i <= k:
                test_sequence.append(s[i])
                i += 1
            test_data.append([test_sequence,s[k+1]])
            
randomize(original_sequences)


# small pseudo-cache for accelerated computing
support_cache = {}

# function: calMatchedList
# calculates all Mi + 1 with Mi as Prefix

def calcMatchedList(seq):
            
    mList = []
    seq_len = len(seq) + 1

    query_string = "['"
    for s in seq:
        query_string += s 
        query_string += "',"

    supportFromDict = {"url": { "$regex": re.escape(query_string)}}
    mydoc = mycol.find(supportFromDict)

    for x in mydoc:
        path = ast.literal_eval(x['url'])
        if len(path) == seq_len:
            mList.append([path,x['support']])
                
    return mList


# function: getSupport(seq):
# returns Support-Value of seq (1 or more)

def getSupport(seq):
    
    if str(seq) in support_cache:
        return support_cache[str(seq)]
    try:
        seq_as_string = str(seq)
        supportFromDict = {"url": seq_as_string}      
        mydoc = mycol.find(supportFromDict)
        for x in mydoc: # kann nur eins sein
            support = x["support"]
            support_cache[str(x["url"])] = x["support"]
        return support
    except UnboundLocalError:
        return 'NoEntry'


# Algorithm 6: Update the Score Map.
# Procedure to update the score map of candidate
# pages based on their conditional probabilities after
# observing Sequence.

def PredictStep(Sequence):
    sequences = [Sequence] # Time-based <=> CSRA Output wenn Tail = 1
    for seq_i in sequences:
        
        support_i = getSupport(seq_i)
        matchedList = calcMatchedList(seq_i)
        
        if support_i == 'NoEntry':
            print("NoEntry")
            continue # Wenn du keinen Eintrag hast, ignoriere diesen Knoten
            
        else:
            for seq_j in matchedList: # seq_j = [[X,Y], 1]
                PageL = seq_j[0][-1]
                support_j = seq_j[1] # A -> B
                score_j = (support_j/support_i)

                if PageL in Scores:
                    Scores[PageL] =  Scores[PageL] + score_j
                else:
                    Scores[PageL] = score_j
            

# Procedure to predict top k candidates pages that will be visited after Candidate sequence S'.
# k = Prediction Size
# Tailsize = How many elements should be considered?

def Predict(Candidate, k, tailSize):
    
    CandidateLength = len(Candidate)
    tailSize = min(CandidateLength, tailSize)
    
    for i in range(0, tailSize):
        start = CandidateLength - i - 1
        seq = Candidate[start:CandidateLength]
        PredictStep(seq)
        
    PredictSetSorted = sorted(Scores.items(), key=lambda x:x[1], reverse=True)
    PredictSetSorted = PredictSetSorted[:k]
    PredictSetSortedConverted = dict(PredictSetSorted)
    return PredictSetSortedConverted


# Settings / Print-Outs

acc_1 = 0
acc_2 = 0
acc_5 = 0
acc_10 = 0
acc_50 = 0
s = 0

test_size = len(test_data)

for test_seq in test_data:
    
    Scores = dict() # Keeps score of each page
    nextPageCandidates = Predict(test_seq[0],50,1) # max = 50 Candidates
    
    first_one = list(nextPageCandidates)[:1]
    
    flag = False # Not the right prediction? Flag = False
    
    if test_seq[1] in first_one:
        acc_1 += 1
        flag = True
    
    first_two = list(nextPageCandidates)[:2]
    for element in first_two:
        if test_seq[1] == element:
            acc_2 += 1
            flag = True
    
    first_five = list(nextPageCandidates)[:5]
    for element in first_five:
        if test_seq[1] == element:
            acc_5 += 1
            flag = True
    
    first_ten = list(nextPageCandidates)[:10]
    for element in first_ten:
        if test_seq[1] == element:
            acc_10 += 1
            flag = True
    
    first_fifty = list(nextPageCandidates)[:50]
    for element in first_fifty:
        if test_seq[1] == element:
            acc_50 += 1
            flag = True
            
    if not flag: # Wrong prediction 
        print("Real value: " + str(test_seq[1]))
        print("Original Sequence: " + str(test_seq[0]) + "+" + str(test_seq[1]))
            
    
    print("Nr. " + str(s+1) + " of " + str(test_size) + " completed.")
    print("Tail = 1, 50 Candidate Size: " + str(100*(acc_50/len(test_data))) + "%")
    
    s +=1
    
    print("Progress: " + str(100*(s/len(test_data))) + "%")
       
print("++++++++++ FINAL RESULTS +++++++++++++++") 
print("ACC(Tail = 1), 1 Candidate Size: " + str(acc_1/len(test_data)))
print("ACC(Tail = 1), 2 Candidate Size: " + str(acc_2/len(test_data)))
print("ACC(Tail = 1), 5 Candidate Size: " + str(acc_5/len(test_data)))
print("ACC(Tail = 1), 10 Candidate Size: " + str(acc_10/len(test_data)))
print("ACC(Tail = 1), 50 Candidate Size: " + str(acc_50/len(test_data)))