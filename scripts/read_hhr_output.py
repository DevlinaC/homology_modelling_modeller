#import sys
from pathlib import Path
import re
import itertools as itts
import json
import pandas as pd
import numpy as np

#inputfile = sys.argv[1]


def get_file_list(MainDir: Path = None):
    if MainDir is None:
        MainDir = Path("/Users/dc1321/testing_homology_modelling/hhr_files")
    return [F for F in MainDir.glob("*.hhr")]


def build_all_prob_dict(FileList: list = None, ResDir: Path = None):
    if FileList is None:
        FileList = get_file_list(ResDir)
    regex_sum = r"^\s*\d+\s+\w+"
    hhrDict = {}
    for resFile in FileList:
        print("parsing", resFile)
        with open(resFile, "r") as infile:
            i = 0
            for line in itts.islice(infile, 0, None):
                # print(line)
                i += 1
                # line = line.strip("\n")
                if line.startswith("Query"):
                    main_name = line.split()[1].split("_")[-1]
                    hhrDict[main_name] = {}
                    continue
                if line.startswith("No 1"):
                    break
                matches = re.match(regex_sum, line)
                if matches:
                    pdbname, rest = line[:35], line[35:]
                    pdbname = pdbname.strip().split()[1]
                    rest = rest.strip()
                    lst_parameters = re.split("\s+", rest)
                    prob = float(lst_parameters[0])
                    # if prob > 80:
                    if pdbname in hhrDict[main_name]:
                        continue
                    hhrDict[main_name][pdbname] = {}
                    pvalue = lst_parameters[1]
                    evalue = lst_parameters[2]
                    score = float(lst_parameters[3])
                    query_range = lst_parameters[6]
                    template_range = lst_parameters[7]
                    hhrDict[main_name][pdbname]["prob"] = float(prob)
                    hhrDict[main_name][pdbname]["pvalue"] = float(pvalue)
                    hhrDict[main_name][pdbname]["evalue"] = float(evalue)
                    hhrDict[main_name][pdbname]["score"] = float(score)
                    # hhrDict[name][pdbname]["query_range"] = query_range
                    # hhrDict[name][pdbname]["template_range"] = template_range
    return hhrDict


hhrDict = build_all_prob_dict()

with open('/Users/dc1321/testing_homology_modelling/results_hhr_all.json', 'w') as oF:
    json.dump(hhrDict, oF, indent=2)


def convert_to_dict(inDict: dict, par: str = "prob"):

    def _get_value(row, col, D: dict = inDict, par: str = par):
        if row in D:
            if col in D[row]:
                return D[row][col][par]
        if col in D:
            if row in D[col]:
                return D[col][row][par]
        return np.NaN

    all_rows = sorted(inDict.keys())
    all_columns = []
    for V in inDict.values():
        all_columns += [x for x in V.keys()]
    all_columns = sorted(set(all_columns))
    work_arr = np.zeros((len(all_rows), len(all_columns)))
    for ix, row in enumerate(all_rows):
        for iy, col in enumerate(all_columns):
            work_arr[ix][iy] = _get_value(row, col)

    return all_columns, all_rows, work_arr


cols, rows, data = convert_to_dict(hhrDict, "prob")
df_prob = pd.DataFrame(data, index=rows, columns=cols)
df_prob = df_prob.fillna(0)

outputfile = Path("/Users/dc1321/testing_homology_modelling/results_hhr_prob.csv")
df_prob.to_csv(str(outputfile))

cols, rows, data = convert_to_dict(hhrDict, "score")
df_score = pd.DataFrame(data, index=rows, columns=cols)
df_score = df_score.fillna(0)

outputfile = Path("/Users/dc1321/testing_homology_modelling/results_hhr_score.csv")
df_score.to_csv(str(outputfile))

