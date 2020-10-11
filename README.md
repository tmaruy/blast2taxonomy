# blast2taxonomy

blast2taxonomy assigns sequences to taxonomic annotation by parsing result files of local BLAST+.

## 0. Prerequisites
* [NCBI BLAST+](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download)
* [BLAST database files](https://ftp.ncbi.nlm.nih.gov/blast/db/): This system supports the following databases
    * RefSeq protein
    * NCBI nr
* Python 3
    * sqlite

## 1. Create DB file
Warning: This create file `parse_blast.db` which exceeds >30GB. 
```
git clone https://github.com/tmaruy/blast2taxonomy.git
chmod +x preprare_taxdb.sh
./prepare_taxdb.sh
```

## 2. BLAST search
Make tabular format (outfmt 6) BLAST results as following. Detail information 
```
blastx -db /path/to/refseq_protein \
       -query test/input.fasta \
       -outfmt 6 \
       -out test/blast.txt
```

## 3. Parse BLAST results
Perform taxonomic assignment with the BLAST results. This system offers two methods (i) taxonomic assignment based on best-hit sequences and (ii) based on top N sequences by lowest common ancestor.

### 3.1. Best hit annotation
* -i : Input file, result of blast search (made at step 2)
* -db : DB file `taxonomy.db` (made at step 1)
* -o : Output file
* -evalue : Threshold of evalue (Ignore hits if their evalues are above this threshold)
```
python blast2taxonomy_besthit.py -i test/blast.txt \
                                 -db taxonomy.db \
                                 -o test/tax_besthit.txt \
                                 -evalue 0.01 
```

### 3.2. LCA (Lowest common ancestor)  
* -i : Input file, result of blast search (made at step 2)
* -db : DB file `taxonomy.db` (made at step 1)
* -o : Output file
* -evalue : Threshold of evalue (Ignore hits if their evalues are above this threshold)
* -lca : Top N hits used for calculation of lowest common ancestors (default N=10)
* -lca_threshold : Returns classification if shared by X % of top hits (default X=50)
```
python blast2taxonomy_lca.py -i test/blast.txt \
                             -db taxonomy.db \
                             -o test/tax_lca.txt \
                             -evalue 0.01 \
                             -lca 10 \
                             -lca_threshold 50
```