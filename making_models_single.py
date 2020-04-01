import sys, os
import pathlib as pl

# input files are 3qh7_A.pdb T1001.ali #

from making_models.align2d import create_align
from making_models.model_single import run_automodel
from making_models.model_single import evaluate_model
from making_models.plot_profiles import plot_profiles

template_file = sys.argv[1]
query_file = sys.argv[2]

main_dir = pl.Path('/Users/dc1321/homology_modelling_modeller/T1001-models')
os.chdir(main_dir)  # move to directory where models and profiles should be saved

ali_res = create_align(template_file=template_file, query_file=query_file)
top_model = run_automodel(ali_res)

print(top_model)

alignment_file = ali_res['aln_file']

templ_code = ali_res['knowns']
query_code = ali_res['sequence']

# for the best model
input_file1 = top_model
output_file1 = query_code + ".profile"
evaluate_model(input_file1, output_file1)

# for the template
input_file2 = templ_code + ".pdb"
output_file2 = templ_code + ".profile"
evaluate_model(input_file2, output_file2)

# print(alignment_file,output_file2,templ_code,output_file1,query_code)

# aln_file, template_profile, template_code, model_profile, model_code
# are needed to run the nest steps

templ_code = pl.Path(template_file).stem
query_code = pl.Path(query_file).stem
aln_file = f"{query_code}-{templ_code}.ali"
templ_profile = f"{templ_code}.profile"
aln_file = f"{query_code}-{templ_code}.ali"
model_profile = f"{query_code}.profile"
plot_profiles(aln_file, templ_profile, templ_code, model_profile, query_code)
