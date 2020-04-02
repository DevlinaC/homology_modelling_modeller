import sys, os
import pathlib as pl

# inputs are a list of templates and the model code, T1001 #

# get input list of target name and template list
query_code = sys.argv[1] # T1001
template_lst_file = sys.argv[2] # list of templates to use for modelling
template_files = []
with open(template_lst_file,'r') as InFile:
    for line in InFile:
        line=line.strip('\n')
        template_files.append(line)

#template_files = ('2x0i_A', '2x0j_A','3qh7_A')

from making_models_mult.salign import create_salign
from making_models_mult.align2d_mult import create_align
from making_models_mult.model_mult import run_automodel
from making_models_mult.model_mult import evaluate_model
from making_models_mult.plot_profiles_mult import plot_profiles


output_filename = 'temp_mult' # the prefix where the alignments of all templates
                              # to each other would be saved
aligned_temp = create_salign(template_files=template_files, output_filename=output_filename)
#print(aligned_temp)

main_dir = pl.Path('/Users/dc1321/homology_modelling_modeller/T1001-mult-models')
os.chdir(main_dir)  # move to directory where models and profiles should be saved
                    # modeller only saves the model where it runs!

target_file = f"{query_code}.ali"
alignment_file = create_align(aligned_temp,target_file)
#print(alignment_file)

top_model = run_automodel(template_files,alignment_file,5)

#print(top_model)

# get energy profiles for all
# for the best model
input_file1 = top_model
output_file1 = query_code + ".profile" # T1001.profile
evaluate_model(input_file1, output_file1)

# for the templates
for templ_code in template_files:
    input_file2 = templ_code + ".pdb"
    output_file2 = templ_code + ".profile"
    evaluate_model(input_file2, output_file2)


#print(alignment_file,template_files,output_file1,query_code)
plot_profiles(alignment_file,template_files,output_file1,query_code)

print("best model vs. templates plotted, see dope_profile_best_model.png")
