# topology.py

import csv
import os
from os import listdir
from os.path import isfile, join
import ast
import mysql.connector

# read crawl
# ScreamingFrog Export
file = open('SF_Crawl/all_outlinks.csv')
csvreader = csv.reader(file)
header = []
header = next(csvreader)

# build topology
topology = {}

for row in csvreader:
    # if source == target
    if row[1] == row[2]:
        continue
    if row[0] == "CSS":
        continue
    if row[0] == "JavaScript":
        continue
    if row[0] == "HTML Canonical":
        continue
    if row[0] == "Image":
        continue
        
    else:
        global topology
        if row[1] not in topology:
            topology[row[1]] = [row[2]]
        else:
            # exclude repetition
            if row[2] not in topology[row[1]]:
                topology[row[1]].append(row[2])
            else:
                continue


# OPTIONAL: corrupted links (crawler-budget limit hit, temporarily none available, etc.)
# folder path
dir_path = 'CSRA_Phase_1_Archive/Archive_Corrupted_Links/'

# Save data names
res = []

# Save corrupted links 
link_dicts = []

# Iterate directory
for path in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, path)):
        res.append(path)

for r in res:
    with open(dir_path + r,"r") as r:
        tempString = str(r) + '_as_String'
        tempString = r.read()
        tempDict = ast.literal_eval(tempString)
        link_dicts.append(tempDict)
        
# x = day of corrupted links 
for x in link_dicts: 
    # y = session (dict)
    for y in x:
        # each key in sessions dictonary
        for k in y:
            if k in topology:
                for n in y[k]:
                    if n not in topology[k]:
                        topology[k].append(n)
                    else:
                        continue
            else:
                # continue
                topology[k] = y[k]

### OPTIONAL ###

# adding prev/next links

# ScreamingFrog Export
file2 = open('SF_Crawl/list_mode_export.csv')
csvreader2 = csv.reader(file2)
for row in csvreader2:
    if row[28] != "" and row[29] != "":
        if row[0] in topology:
            if row[28] not in topology[row[0]]:
                topology[row[0]].append(row[28])
            if row[29] not in topology[row[0]]:
                topology[row[0]].append(row[29])
            else:
                continue
    else:
        continue


# SQL-Export

mydb = mysql.connector.connect(
  host="___",
  user="___",
  password="___",
  database="___"
)

mycursor = mydb.cursor()
# dont forget to set up the database before inserting values, e.g. URL and OUTGOING_LINKS as columns
for k in topology:
    sql = "INSERT INTO ___ (URL, OUTGOING_LINKS) VALUES (%s, %s)"
    val = (k, str(topology[k]))
    mycursor.execute(sql, val)
mydb.commit()

