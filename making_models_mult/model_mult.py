import sys
import os
import pathlib as pl
from modeller import *
from modeller.automodel import *
from modeller.scripts import complete_pdb


#log.verbose()
env = environ()
env.libs.topology.read(file='$(LIB)/top_heav.lib')  # read topology
env.libs.parameters.read(file='$(LIB)/par.lib')  # read parameters
env.io.atom_files_directory = ['.', '/Users/dc1321/homology_modelling_modeller/templates']  # set directory for templates

main_dir = pl.Path('/Users/dc1321/homology_modelling_modeller/T1001-mult-models')  # set directory for outputs

os.chdir(main_dir)  # move to directory where models should be saved

def evaluate_model(input_file, output_file):
    """
    Generate energy profile for a model
    :param input_file: PDB file
    :param output_file: profile file

    """

    # read model file
    mdl = complete_pdb(env, input_file)

    # Assess all atoms with DOPE:
    s = selection(mdl)
    s.assess_dope(output='ENERGY_PROFILE NO_REPORT', file=output_file,
                  normalize_profile=True, smoothing_window=15)


def run_automodel(template_list, target_file, num_models: int = 5):
    """

    :param template_list: list of template codes
    :param target_file: the .ali of the target
    :param num_models: integer
    :return: best model

    """

    target_filepath = main_dir / target_file
    target_name = pl.Path(target_file).stem  # T1001-mult
    (target_code, extra) = target_name.split('-')  # T1001
    a = automodel(env, alnfile=str(target_filepath),
                  knowns=template_list, sequence=target_code,
                  assess_methods=(assess.DOPE,
                                  assess.GA341))
    a.starting_model = 1
    a.ending_model = int(num_models)
    a.make()

    # Get a list of all successfully built models from a.outputs
    ok_models = [x for x in a.outputs if x['failure'] is None]
    # Rank the models by DOPE score
    key = 'DOPE score'
    if sys.version_info[:2] == (2, 3):
        ok_models.sort(lambda a, b: cmp(a[key], b[key]))
    else:
        ok_models.sort(key=lambda a: a[key])

    # Get top model
    m = ok_models[0]

    print("Top model: %s (DOPE score %.3f)" % (m['name'], m[key]))
    return (m['name'])

