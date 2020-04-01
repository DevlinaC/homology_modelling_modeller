# create a local blast database using PDB sequences #

echo "Download latest PDB seqeunces"
wget ftp://ftp.wwpdb.org/pub/pdb/derived_data/pdb_seqres.txt
echo "make them to BLAST database"
makeblastdb -in pdb_seqres.txt -out pdb_seqres -dbtype prot
