import re
from optparse import OptionParser, OptionValueError
from pathlib import Path


"""
check options
"""

def _check_inputFile(option, opt_str, value, parser):
    f_path = Path(value)
    if not f_path.is_file():
        raise OptionValueError(f"Cannot get {str(f_path)} file")
    setattr(parser.values, option.dest, Path(f_path))
    parser.values.saved_infile = True


def _check_inputDir(option, opt_str, value, parser):
    f_path = Path(value)
    if not f_path.is_dir():
        raise OptionValueError(f"Cannot get {str(f_path)} file")
    setattr(parser.values, option.dest, Path(f_path))
    parser.values.saved_infile = True

"""
Read blast output to find sequences at a threshold of seqid
"""
def blast_templates(in_file: Path, threshold: float):
    """
        read the blast output and create list
    """
    pdb_lst = []
    with open(in_file) as oF:
        for line in oF:
            line = line.strip()
            if len(line) < 1:
                continue
            if line.startswith("Search "):  # skipping CONVERGED lines
                continue
            # to skip blank lines and the line stating search has CONVERGED #
            query, pdb, seqid, *rest = line.split()
            if float(seqid) >= threshold:
                pdb_lst.append(pdb)
    return pdb_lst

"""
Read HHsearch output to find templates at a threshold (prob score)

"""
def hhr_templates(in_file: Path, threshold: float):
    """
        read the hhr output and create a list of templates
        something to try : sort the list by coverage
    """
    pdb_lst = []
    regex_sum = r"^\s*\d+\s+\w+"
    #print("parsing ",in_file)
    with open(in_file) as oF:
        for line in oF:
            line = line.strip()
            if line.startswith("Query"):
                main_name = line.split()[1].split("_")[-1]
                print("Query",main_name,end=" ")
                continue
            if line.startswith("No 1"):
                break
            matches = re.match(regex_sum, line)
            if matches:
                pdbid, rest = line[:34], line[34:]
                pdbid = pdbid.strip().split()[1]
                rest = rest.strip()
                lst_parameters = re.split("\s+", rest)
                prob = float(lst_parameters[0])
                #print(prob)
                if float(prob) >= threshold:
                    pdb_lst.append(pdbid)
    return pdb_lst


"""
get combined lst of templates
without duplicates
"""
def combine_list(a:list,b:list):
    comb = set(a+b)
    return list(comb)

if __name__ == "__main__":
    options_parser = OptionParser()
    options_parser.add_option("-B", "--input_blast",
                              dest="input_file1", type='str',
                              help="input FILE blast",
                              metavar="FILE",
                              action='callback',
                              callback=_check_inputFile)
    options_parser.add_option("-H", "--input_hhr",
                              dest="input_file2", type='str',
                              help="input FILE hhr",
                              metavar="FILE",
                              action='callback',
                              callback=_check_inputFile)
    options_parser.add_option("-p", "--prob",
                              dest="probcut", type='float',
                              help="prob cutoff",
                              metavar="FLOAT")
    options_parser.add_option("-s", "--seqid",
                              dest="seqcut", type='float',
                              help="sequence id cutoff",
                              metavar="FLOAT")
    (options, args) = options_parser.parse_args()
    # print(options.__dict__)
    inFile1 = Path(options.input_file1)
    inFile2 = Path(options.input_file2)
    cutoff = float(options.seqcut)
    prob = float(options.probcut)
    lst1 =blast_templates(inFile1, cutoff)
    lst2 = hhr_templates(inFile2,prob)
    combined_lst = combine_list(lst1,lst2)
    for i in combined_lst[:10]:
        print(i,end=",")
    print()
