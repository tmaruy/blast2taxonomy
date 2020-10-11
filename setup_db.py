import os
import sys
import numpy as np
import sqlite3 

# Create table
dbname = "taxonomy.db"
conn = sqlite3.connect(dbname)
cur = conn.cursor()

# Create table: acc2tax
command = "CREATE TABLE acc2tax(accession STRING PRIMARY KEY, taxid STRING)"
cur.execute(command)
#
with open("db/prot.accession2taxid") as fi:
	for i, j in enumerate(fi):
		if i == 0: continue
		acc, accv, tax, gi = j.strip("\n").split("\t")
		cur.execute("INSERT INTO acc2tax VALUES (?, ?)", (acc, tax))
with open("db/ead_prot.accession2taxid") as fi:
	for i, j in enumerate(fi):
		if i == 0: continue
		acc, accv, tax, gi = j.strip("\n").split("\t")
		cur.execute("INSERT INTO acc2tax VALUES (?, ?)", (acc, tax))

# Create table: taxonomy
command = "DROP TABLE IF EXISTS taxonomy"
cur.execute(command)
command = "CREATE TABLE taxonomy(taxid STRING PRIMARY KEY, category STRING, name STRING, t_domain STRING, t_phylum STRING, t_class STRING, t_order STRING, t_family STRING, t_genus STRING, t_species STRING )"
cur.execute(command)
# tax2name
tax2name = dict()
with open("db/names.dmp") as fi:
    for ii,jj in enumerate(fi):
        data = jj.strip("\n\t|").split("\t|\t")
        if data[3] == "scientific name": tax2name[data[0]] = data[1]
# classification info
category2num = {"species":6,"genus":5,"family":4,"order":3,"class":2,"phylum":1,"superkingdom":0}
tax2ancestor = dict() 
tax2category = dict()
taxes = []
with open("db/nodes.dmp") as fi:
    for ii,jj in enumerate(fi):
        data = jj.strip("\n").split("\t|\t")
        tax2category[data[0]] = data[2]
        tax2ancestor[data[0]] = data[1]
        taxes.append(int(data[0]))
with open("db/merged.dmp") as fi:
    for ii,jj in enumerate(fi):
        data = jj.strip("\n|\t").split("\t|\t")
        tax2category[data[0]] = tax2category[data[1]]
        tax2ancestor[data[0]] = tax2ancestor[data[1]]
        taxes.append(int(data[0]))
        tax2name[data[0]] = tax2name[data[1]]
# 
taxes = np.sort(taxes)
for taxn in taxes:
    tax = str(taxn)
    name = tax2name[tax]
    cate = tax2category[tax]
    vector = ["","","","","","",""]
    if cate in category2num:
        vector[category2num[cate]] = tax2name[tax]
    #
    tax2 = tax
    while tax2 != "1":
        tax3 = tax2ancestor[tax2]
        cate3 = tax2category[tax3]
        if cate3 in category2num:
            vector[category2num[cate3]] = tax2name[tax3]
        if cate3 == "superkingdom": break
        tax2 = tax3
    cur.execute("INSERT INTO taxonomy VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [tax, cate, name] + vector)

# Save
conn.commit()
cur.close()
conn.close()
