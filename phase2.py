# phase2.py

# Examples for input

# i = 1
#Candidates = [['P1', 'P2', 'P4', 'P3', 'P7']]
# Links = [{'P1': ['P2', 'P3'], 'P2': ['P3', 'P4'], 'P3': ['P6', 'P7']}]

# i = 1
#Candidates = [['P1', 'P20', 'P23', 'P13', 'P34']] 
# Links = [{'P1': ['P13', 'P20'], 'P13': ['P34'], 'P20': ['P23']}]

# i = 2
#Candidates = [['P1', 'P20', 'P23', 'P13', 'P34'], ['P1', 'P2', 'P4', 'P3', 'P7']] 
#Links = [{'P1': ['P13', 'P20'], 'P13': ['P34'], 'P20': ['P23']}, {'P1': ['P2', 'P3'], 'P2': ['P3', 'P4'], 'P3': ['P6', 'P7']}]

# load Candidates & Links
# Links with mysql.connector for example

#with open('candidates.txt',"r") as r: # see: candidates.py
    #Candidates_as_String = r.read()
#Candidates = ast.literal_eval(Candidates_as_String) 

# import mysql.connector

#Links = {}
#mycursor = mydb.cursor()
#mycursor.execute("SELECT URL,OUTGOING_LINKS FROM TOPOLOGY") # example query
#myresult = mycursor.fetchall()             
#for row in myresult:
   # Links[row[0]] = row[1]

from ast import literal_eval
import ast
import copy
import re

missing_linkgraphs = ''

# y after x (timestamp condition)
def delta(x,y,z):
    
    xIndex = z.index(x)
    yIndex = z.index(y)
    
    if (xIndex > yIndex): 
        return False
    else:
        return True

# GetLinkGraph
# array of nodes
# generiert Linkgraphen explizit für die Session

def getLinkGraphs(aon):
        
    SessionLinks = {}
    i = 0
        
    for a in aon:
                
        # D(a), insert dynamic link repository e.g.
        if (i < (len(aon) - 1)):
            print("simple levensthein distance: " + str(ratio(a, aon[i+1])))  
            # make use of it 
        
        # web topology check
        if a in Links:
            SessionLinks[a] = []
            Outlinks = ast.literal_eval(Links[a])
            for outlink in Outlinks:
                if outlink in aon and outlink != a and delta(a,outlink,aon):
                    SessionLinks[a].append(outlink)
                else:
                    continue
            i += 1

        else: # optional: save node in case theres no link information 
            SessionLinks[a] = []
            global missing_linkgraphs
            if str(a) not in missing_linkgraphs:
                missing_linkgraphs = missing_linkgraphs + a + "," 
                with open('missing-links.txt', 'w') as l:
                    l.write(str(a)  + "\n")

            i += 1
            
    return SessionLinks


def catchZeroOutdegree(P, Link):
    try:
        return len(Link[P])
    except:
        return 0

# extended pseudo-code with parameter Link
def CreateNewSequence(P, Link):
    
    New = dict()  
    New.update({P: []})
    New[P] = ["T", catchZeroOutdegree(P, Link), [P]] # Flag = Max, len(Link[P]) = OutDegree
        
    if (New[P][1] == 0):
        CMaximals.update(New)
    else:
        TSequences.update(New)


def NewSequenceExtend(Seq, P, Link, CandidateSession):
    
    Lj = TSequences[Seq][2][-1]
    hasLink = True if (P in Link[Lj]) else False  
    timeStamp = delta(Lj, P, CandidateSession)
        
    if timeStamp and hasLink:
        
        #print("new connection")
        global Flag
        Flag = True
        TSequences[Seq][1] = TSequences[Seq][1] - 1
        TSequences[Seq][0] = "F"
        
        New = dict()  
        New.update({str(Seq+","+P): []})
        
        Old = copy.deepcopy(TSequences)
        NewSequence = Old[Seq][2]
        NewSequence.append(P)
        New[str(Seq+","+P)] = ["T", catchZeroOutdegree(P, Link), NewSequence]
                
        if (New[str(Seq + "," + P)][1] == 0):
            CMaximals.update(New)
        
        else:
            TSequences.update(New)
            
        if (TSequences[Seq][1] == 0):
            del TSequences[Seq]
    else:
        useless = ''
        # print("no connection")


def MPVS(CandidateSession, Link):
        
    for P in CandidateSession:
        global Flag
        Flag = False
        for Seq in TSequences.copy():
            NewSequenceExtend(Seq, P, Link, CandidateSession) # slightly modified parameter set
        if (Flag == False):
            CreateNewSequence(P, Link) # link information has to be added for the code to work 


def CSRAPhase2(Candidates):
    
    global TSequences, CMaximals, AMaximals, Flag
    AMaximals = []
    i = 0  
    
    for Session in Candidates:
                                    
        TSequences = dict() # Temporary Sequences
        CMaximals = dict() # Current Maximals
        Link = getLinkGraphs(Session) # Current Navigation Graph

        MPVS(Session,Link)
        i = i + 1

        for k in TSequences:
            if TSequences[k][0] == "T":
                CMaximals.update(TSequences)

        AMaximals.append(CMaximals)
        
    CSRA_Paths = []
    
    for d in AMaximals:
            for k, v in d.items():
                CSRA_Paths.append(v[2])
                
    with open('paths.txt', 'w') as cc:
        cc.write(str(CSRA_Paths))        


# go! ####

TSequences = dict()
CMaximals = dict()
AMaximals = dict()
Flag = False

# start with small sessions
Candidates = sorted(Candidates, key=len)
CSRAPhase2(Candidates)