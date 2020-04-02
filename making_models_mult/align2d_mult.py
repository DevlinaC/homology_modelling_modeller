import sys
import pathlib as pl
from modeller import *

#log.verbose()

def create_align(template_file,target_file):

    # Set up directories and path
    sequence_dir = pl.Path('/Users/dc1321/homology_modelling_modeller/sequence_files')
    output_dir = pl.Path('/Users/dc1321/homology_modelling_modeller/T1001-mult-models')

    templates_aligned = output_dir / template_file
    target_code = pl.Path(target_file).stem
    target_filepath = sequence_dir / target_file

    output_file1 = target_code + "-mult.ali"
    output_file1path = output_dir / output_file1

    output_file2 = target_code + "-mult.pap"
    output_file2path = output_dir / output_file2

    env = environ()
    env.io.atom_files_directory = '/Users/dc1321/homology_modelling_modeller/templates'  # set directory for templates
    env.libs.topology.read(file='$(LIB)/top_heav.lib')

    # Read aligned structure(s)
    aln = alignment(env)
    aln.append(file=str(templates_aligned), align_codes='all')
    aln_block = len(aln)

    # Read aligned sequence(s):
    aln.append(file=str(target_filepath), align_codes=target_code)

    # Structure sensitive variable gap penalty sequence-sequence alignment:
    aln.salign(output='', max_gap_length=20,
               gap_function=True,   # to use structure-dependent gap penalty
               alignment_type='PAIRWISE', align_block=aln_block,
               feature_weights=(1., 0., 0., 0., 0., 0.), overhang=0,
               gap_penalties_1d=(-450, 0),
               gap_penalties_2d=(0.35, 1.2, 0.9, 1.2, 0.6, 8.6, 1.2, 0., 0.),
               similarity_flag=True)

    aln.write(file=str(output_file1path), alignment_format='PIR')
    aln.write(file=str(output_file2path), alignment_format='PAP')

    return(output_file1)

