import os
import sys
import numpy as np
import argparse
import sqlite3

parser = argparse.ArgumentParser()
parser.add_argument("-i",dest="ifile",action="store",default="",help="Path of input file")
parser.add_argument("-o",dest="ofile",action="store",default="",help="Path of output file")
parser.add_argument("-db",dest="db",action="store",default="",help="Database file")
parser.add_argument("-evalue",dest="evalue",action="store",default=1e-5,type=float,help="e-value, evalue")
parser.add_argument("-evalue_col",dest="evalue_col",action="store",default=11,type=int,help="e-value, evalue_col")
args = parser.parse_args()

# Connect to DB
conn = sqlite3.connect(args.db)
cur = conn.cursor()

# Load file
index = args.evalue_col - 1
fi = open(args.ifile)
fo = open(args.ofile,"w")
id = ""
for ii,jj in enumerate(fi):
	data = jj.strip("\n").split("\t")
	evalue = float(data[index])
	if evalue <= args.evalue and id != data[0]:
		id = data[0]
		acc = data[1].split(".")[0]
		f1 = cur.execute("SELECT taxid FROM accession2taxid WHERE accession='" + acc + "';").fetchone()
		if f1 == None:
			tax = tax_name = ""
		else:
			tax = str(f1[0])
			f2 = cur.execute("SELECT * FROM taxonomy WHERE taxid='" + tax + "';").fetchone()
			if f2 == None: tax_name = "" 
			else: tax_name = f2[2]
		fo.write("\t".join([id, acc, str(evalue), tax, tax_name]) + "\n")
fi.close()
fo.close()
