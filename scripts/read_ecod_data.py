import json
import pathlib
from pathlib import Path
import itertools as itts


# reads ecod data file #
def read_description(inFile: Path = None):
    if inFile is None:
       loc = Path("/Users/dc1321/testing_domain_contacts/old_files") # change to working directory
       inFile = loc / "ecod.latest.domains.txt" # to get this file from 
                                                # http://prodata.swmed.edu/ecod/distributions/ecod.latest.domains.txt

    out_data = []
    with open(inFile) as oF:
        for line in itts.islice(oF, 0, None):
           #print(line)
           if line.startswith("#uid"):
               header = line.rstrip()[1:].split("\t")
               #print(header)
           if not line.startswith("#"):
               coins = [x.replace('"', "") for x in line.rstrip().split("\t")]
               curr_dict = {
                   k: v
                   for k, v in zip(header, coins)
                   if k not in {"ligand", "asm_status"}
               }
               if curr_dict["t_name"] == "NO_T_NAME":
                   curr_dict["t_name"] = curr_dict["f_name"]
               if curr_dict["h_name"] == "NO_H_NAME":
                   curr_dict["h_name"] = curr_dict["t_name"]
               if curr_dict["x_name"] == "NO_X_NAME":
                   curr_dict["x_name"] = curr_dict["h_name"]
                   out_data.append(curr_dict)
    return out_data

# only get info for pdb you want #
input_file = "list_pdb.txt" # included a test file to play with #
set_tokeep = set()

with open (input_file) as IF:
    for line in IF:
        line=line.strip('\n')
        set_tokeep.add(line)

all_data = read_description()
# get the info #
to_keep = [k for k in all_data if k['pdb'] in set_tokeep]
# save it to JSON
data_json = json.dumps(to_keep, sort_keys=True,indent=4)
print(data_json)
