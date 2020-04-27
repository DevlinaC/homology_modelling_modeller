# Homology Models

Building models using modeller 9.23 and a single template
and scripts to generate models using single and multiple templates

**IMPORTANT** Before running, 
please change the **Path** in *making_models_single.py* and *making_models_mult_templates.py* 
to location where templates and models must be saved in 

## To run using single template 
```bash
python3 making_models_single.py 3qh7_A.pdb T1001.ali
```

## To run using multiple templates
```bash
python making_models_mult_templates.py T1001 list_templates.txt
```
Saves the outputs and models in T1001-models and T1001-mult-models for single and multiple template prediction respectively

To convert fasta to ali, use *convert_fileformat_modeller.py*, 
**NOTE**: there are other useful scripts in the scripts folder   
- For running PSI-BLAST and downloading associated PDB structures:
*run_psiblast.py* and *download_pdb_blastoutput.py*
- For running HHsearch and downloading associated PDB structures:
*run_hhsearch.py* and *download_pdb_hhroutput.py* 
- To read the outputs and download PDBs from the search outputs:
*combined_blast_hhr_templates.py* and *download_templates.py*
- For calculation of RMSD among the predictions and performing clustering:
 *calculate_rmsd.py*, *calculate_rmsd_biopython.py*, *AMC.py*, *HCS.py*

