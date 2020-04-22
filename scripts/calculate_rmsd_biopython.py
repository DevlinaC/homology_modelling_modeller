import Bio.PDB
import sys
import re

# Start the parser
pdb_parser = Bio.PDB.PDBParser(QUIET = True)

# get the files
reference_file = sys.argv[1]
sample_file = sys.argv[2]

# get the names for printing

#H0993_2d29_A_model01.pdb #
ptrn = re.compile(r"(?P<target>[a-zA-Z0-9]+)\_(?P<template>.+\_.+)_model(?P<model>\d+)\.pdb")
#print(reference_file,sample_file)
m1 = ptrn.search(reference_file)
m2 = ptrn.search(sample_file)

if m1 is None:
    print("can't parse this ", reference_file)
else:
    target = m1.group("target")
    template = m1.group("template")
    (template_name,chain) = template.split('_')
    model_num = m1.group("model")
    model1 = target + "_" + template_name + chain + "_" + model_num

if m2 is None:
    print("can't parse this ", sample_file)
else:
    target = m2.group("target")
    template = m2.group("template")
    (template_name,chain) = template.split('_')
    model_num = m2.group("model")
    model2 = target + "_" + template_name + chain + "_" + model_num

print(model1,model2,end=" ")


# Get the structures
ref_structure = pdb_parser.get_structure("reference", reference_file)
sample_structure = pdb_parser.get_structure("sample", sample_file)

# Use the first model in the pdb-files for alignment
# Change the number 0 if you want to align to another structure
ref_model    = ref_structure[0]
sample_model = sample_structure[0]

# Make a list of the atoms (in the structures) you wish to align.
# In this case we use CA atoms whose index is in the specified range
ref_atoms = []
sample_atoms = []

# Iterate of all chains in the model in order to find all residues
for ref_chain in ref_model:
  # Iterate of all residues in each model in order to find proper atoms
  for ref_res in ref_chain:
      # Append CA atom to list
    ref_atoms.append(ref_res['CA'])

# Do the same for the sample structure
for sample_chain in sample_model:
  for sample_res in sample_chain:
    sample_atoms.append(sample_res['CA'])

# Now we initiate the superimposer:
super_imposer = Bio.PDB.Superimposer()
super_imposer.set_atoms(ref_atoms, sample_atoms)
super_imposer.apply(sample_model.get_atoms())

# Print RMSD:
rmsd = super_imposer.rms
print("{0:.2f}".format(rmsd))
