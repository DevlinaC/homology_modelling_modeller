import pathlib as pl
import os
import sys
from subprocess import check_output

"""
Setup start and main_directory
"""

main_dir = pl.Path('/Users/dc1321/testing_homology_modelling')
blast_db_dir = pl.Path('/Users/dc1321/humanPPI/data/protein_sequences_frm_PDB')
in_file = sys.argv[1]
out_file = sys.argv[2]

os.chdir(main_dir)  # move to original directory


def run_blast(in_file: str, out_file: str, prot_dir: pl.Path = main_dir) -> pl.Path:
	"""
	run blast against all sequence of PDB
	"""
	pdb_seq_dir = blast_db_dir / "pdb_seqres"
	prot_seq_file = main_dir / in_file
	blast_output = main_dir / out_file

	# blast -query test_set.fasta -db pdb_seqres -out test_set.txt -outfmt 6 -num_iterations 10 -comp_based_stats 1 -evalue 10 #
	cmd = "psiblast" + ' -query ' + str(prot_seq_file) + ' -db ' + str(pdb_seq_dir) + " -out " + str(blast_output) + " -outfmt 6 -num_iterations 10 -comp_based_stats 1 -evalue 10"
	#print(cmd)
	out = check_output(cmd,shell=True)
	#print(out)

run_blast(str(in_file), str(out_file))
