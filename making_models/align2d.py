import os
import sys
from pathlib import Path
from modeller import *

def create_align(template_file,query_file):

    """
    Set up directories as well

    :param template_file: pdb format with chain of interest
    :param query_file: Query sequence in modeller readable format (.ali)
    :return dict_input: Input parameters for running modelling

    """
    template_dir = Path('/Users/dc1321/homology_modelling_modeller/templates')
    sequence_dir = Path('/Users/dc1321/homology_modelling_modeller/sequence_files')
    output_dir = Path('/Users/dc1321/homology_modelling_modeller/T1001-models')
    env = environ()
    aln = alignment(env)
    template_file = Path(template_file)
    templ_code = template_file.stem

    templ_name,chain=templ_code.split('_')
    query_file = Path(query_file)
    query_code = query_file.stem

    template_filepath = template_dir / template_file

    query_filepath = sequence_dir / query_file

    output_filename = f"{query_code}-{templ_code}.ali"
    output_filepath = output_dir / output_filename

    mdl = model(env, file=str(template_filepath), model_segment=('FIRST:{}'.format(chain),'LAST:{}'.format(chain)))
    aln.append_model(mdl, align_codes=templ_code, atom_files=str(template_filepath))
    aln.append(file=str(query_filepath), align_codes=query_code)
    aln.align2d()
    aln.write(file=str(output_filepath), alignment_format='PIR')
    return {'sequence':query_code, 'knowns': templ_code, 'aln_file': output_filename }

