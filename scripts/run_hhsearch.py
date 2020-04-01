import pathlib as pl
import os
import sys
from subprocess import check_output

"""
Setup start and main_directory
"""

main_dir = pl.Path('/u1/home/dc1321/data/testing_homology_modelling')
hhr_db_dir = pl.Path('/u1/home/dc1321/data/hhbits_database/')

# fasta file as input and .hhr file as output #
in_file = sys.argv[1]
out_file = sys.argv[2]

os.chdir(main_dir)  # move to original directory


def run_hhsearch(in_file: str, out_file: str, prot_dir: pl.Path = main_dir) -> pl.Path:
	"""
	run hhsearch against all sequence of PDB
	"""
	pdb_seq_dir = hhr_db_dir / "pdb70"
	prot_seq_file = main_dir / in_file
	hhr_output = main_dir / out_file
	# hhsearch -i T1001.fasta -o T1001.output -d ../hhbits_database/pdb70 #
	cmd = "hhsearch" + ' -i ' + str(prot_seq_file) + ' -o ' + str(hhr_output) + " -d " + str(pdb_seq_dir)
	#print(cmd)
	out = check_output(cmd,shell=True)
	#print(out)

run_hhsearch(str(in_file), str(out_file))
