import os
import sys
import numpy as np
import pandas as pd
import argparse
import sqlite3

parser = argparse.ArgumentParser()
parser.add_argument("-i",dest="ifile",action="store",default="",help="Input blast result file")
parser.add_argument("-o",dest="ofile",action="store",default="",help="Output filename")
parser.add_argument("-db",dest="db",action="store",default="",help="Database file")
parser.add_argument("-evalue",dest="evalue",action="store",default=1e-2,type=float,help="Threshold of evalue (Ignore hits if their evalues are above this threshold)")
parser.add_argument("-lca",dest="lca",action="store",default=10,type=int,help="Top n hits used for calculation of lowest common ancestors")
parser.add_argument("-lca_threshold", dest="lca_threshold", action="store", default=50, type=float, help="Returns classification if shared by x%% of top hits (default x=50)")
args = parser.parse_args()

# Connect to DB
conn = sqlite3.connect(args.db)
cur = conn.cursor()

# parse & LCA
def lca(vec, threshold=args.lca_threshold/100.0):
	uvec, num = np.unique(vec, return_counts=True)
	idx = np.argmax(num)
	if num[idx] > len(uvec) * threshold: return uvec[idx]
	else: return ""
def parse(df):
	df = df.loc[df.evalue.astype(float) <= args.evalue, :]
	if df.shape[0] > args.lca: df = df.iloc[:args.lca, :]
	acc = "('" + "', '".join(df.sseqid.tolist()) + "')"
	acc2tax = cur.execute("SELECT * FROM accession2taxid act, taxonomy tx WHERE act.accession IN " + acc + " AND act.taxid=tx.taxid;")
	if acc2tax.shape[0] == 0: 
		return [id, "", "", "", "", "", "", ""]
	else:
		return [id] + df.iloc[:, 5:].apply(lca).tolist()

# Load file
id = ""
fo = open(args.ofile,"w")
cols = ["qseqid", "sseqid", "pident", "length", "mismatch", "gapopen", "qstart", "qend", "sstart", "send", "evalue", "bitscore"]
with open(args.ifile) as fi:
	for i, line in enumerate(fi):
		dat = line.strip("\n").split("\t")
		if id != dat[0]:
			if i != 0: 
				df = pd.DataFrame(df, columns=cols)
				fo.write("\t".join(parse(df)))
			df = [dat]
			id = dat[0]
		else: 
			df.append(dat)
if id != dat[0]:
	df = pd.DataFrame(df, columns=cols)
	fo.write("\t".join(parse(df)))
fo.close()
