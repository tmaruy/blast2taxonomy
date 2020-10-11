CWD=`pwd`
mkdir $CWD/db
cd $CWD/db

# Download taxdmp file
wget ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdmp.zip
unzip taxdmp.zip

# Download annotation files
wget ftp://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid/prot.accession2taxid.gz
wget ftp://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid/dead_prot.accession2taxid.gz
gunzip *gz

# Remove files 
rm taxdmp.zip
rm prot.accession2taxid.gz
rm dead_prot.accession2taxid.gz

# Create sqlite3 database
python setup_db.py