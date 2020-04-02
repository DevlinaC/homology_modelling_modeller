# first step is to create alignment for the templates
# using SALIGN multiple structure/sequence alignment

import os,sys
import pathlib as pl
from modeller import *


def create_salign(template_files,output_filename):
    #log.verbose()
    env = environ()
    aln = alignment(env)

    env.io.atom_files_directory = '/Users/dc1321/homology_modelling_modeller/templates' # set directory for templates
    template_dir = pl.Path('/Users/dc1321/homology_modelling_modeller/templates')
    output_dir = pl.Path('/Users/dc1321/homology_modelling_modeller/T1001-mult-models')
    os.chdir(template_dir)  # move to directory where templates should be saved

    # setting output files
    dendogram_file = output_filename + ".tree"
    dendogram_filepath = output_dir / dendogram_file
    template_alnfile1 = output_filename + ".pap"
    template_alnfile1path = output_dir / template_alnfile1
    template_alnfile2 = output_filename + ".ali"
    template_alnfile2path = output_dir / template_alnfile2

    for template in template_files:
        (code,chain)=template.split('_')
        mdl = model(env, file=code+"_"+chain, model_segment=('FIRST:'+chain, 'LAST:'+chain))
        aln.append_model(mdl, atom_files=code, align_codes=code+"_"+chain)

    for (weights, write_fit, whole) in (((1., 0., 0., 0., 1., 0.), False, True),
                                        ((1., 0.5, 1., 1., 1., 0.), False, True),
                                        ((1., 1., 1., 1., 1., 0.), True, False)):
        aln.salign(rms_cutoff=3.5, normalize_pp_scores=False,
                rr_file='$(LIB)/as1.sim.mat', overhang=30,
                gap_penalties_1d=(-450, -50),
                gap_penalties_3d=(0, 3), gap_gap_score=0, gap_residue_score=0,
                dendrogram_file=str(dendogram_filepath),
                alignment_type='tree', # If 'progressive', the tree is not
                                      # computed and all structures will be
                                      # aligned sequentially to the first
               feature_weights=weights, # For a multiple sequence alignment only
                                        # the first feature needs to be non-zero
               improve_alignment=True, fit=True, write_fit=write_fit,
               write_whole_pdb=whole, output='ALIGNMENT QUALITY')

    aln.write(file=str(template_alnfile1path), alignment_format='PAP')
    aln.write(file=str(template_alnfile2path), alignment_format='PIR')

    aln.salign(rms_cutoff=1.0, normalize_pp_scores=False,
        rr_file='$(LIB)/as1.sim.mat', overhang=30,
        gap_penalties_1d=(-450, -50), gap_penalties_3d=(0, 3),
        gap_gap_score=0, gap_residue_score=0, dendrogram_file='1is3A.tree',
        alignment_type='progressive', feature_weights=[0]*6,
        improve_alignment=False, fit=False, write_fit=True,
        write_whole_pdb=False, output='QUALITY')

    return(template_alnfile2)

