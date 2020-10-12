CWD=`pwd`
mkdir $CWD/db
cd $CWD/db

# Download taxdmp file
wget ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdmp.zip
unzip taxdmp.zip

# Download annotation files
wget ftp://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid/prot.accession2taxid.gz
gunzip *gz

# Remove files 
rm taxdmp.zip

# Create sqlite3 database
cd $CWD
python setup_db.py
