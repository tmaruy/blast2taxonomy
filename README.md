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

## 3. LCA (Lowest-common-ancestor) based taxonomic assignment
Perform taxonomic assignment with the BLAST results
```
python blast2taxonomy.py -i test/blast.txt \
                         -db taxonomy.db \
                         -o test/tax.txt \
                         -evalue 0.01 \
                         -lca 10 \
                         -lca_threshold 0.5 
```