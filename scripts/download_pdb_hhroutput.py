import gzip
import re
import urllib.request
from optparse import OptionParser, OptionValueError
from pathlib import Path


"""
Read HHsearch output to find templates at a threshold (prob score)

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


def download_pdb(in_file: Path, threshold: float, pdb_dir: Path):
    """
        read the hhr output and download pdbid
    """
    pdb_lst = []
    regex_sum = r"^\s*\d+\s+\w+"
    print("parsing ",in_file)
    with open(in_file) as oF:
        for line in oF:
            line = line.strip()
            if line.startswith("Query"):
                main_name = line.split()[1].split("_")[-1]
                print("Query",main_name)
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

    print(f"Will dowload {len(pdb_lst)} files")
    for i in pdb_lst:
        print(f"Getting {i}")
        pdbid, chainid = i.split("_")
        file_name = pdbid + ".pdb"
        file_path = pdb_dir / file_name
        url = "http://www.rcsb.org/pdb/files/" + pdbid + ".pdb.gz"
        with urllib.request.urlopen(url) as response:
            with gzip.GzipFile(fileobj=response) as uncompressed:
                with open(file_path, 'wb') as out_file:
                    data = uncompressed.read()
                    out_file.write(data)

        clean_pdb(chainid, pdbid, pdb_dir)


def clean_pdb(chainid: str, pdbid: str, pdb_dir: Path):
    """
    clean the pdb file to have only ATOM records and specific chain, 
    with TER at the end
    """
    file_out = pdbid.lower() + "_" + chainid + ".pdb"
    file_in = pdbid.lower() + ".pdb"
    fileout_path = pdb_dir / file_out
    filein_path = pdb_dir / file_in

    coord_re = re.compile("^ATOM")
    with open(fileout_path, 'w+') as pdbfhout,\
            open(filein_path, 'r') as pdbfhin:
        for line in pdbfhin:
            line=line.strip('\n')
            if coord_re.match(line) and line[21] in chainid:
                pdbfhout.write(line + "\n")
        pdbfhout.write("TER\n")


if __name__ == "__main__":
    options_parser = OptionParser()
    options_parser.add_option("-i", "--input",
                              dest="input_file", type='str',
                              help="input FILE",
                              metavar="FILE",
                              action='callback',
                              callback=_check_inputFile)
    options_parser.add_option("-d", "--pdb_dir",
                              dest="pdb_dir", type='str',
                              help="path to PDB DIR",
                              metavar="DIR",
                              action='callback',
                              callback=_check_inputDir)
    options_parser.add_option("-p", "--prob",
                              dest="probcut", type='float',
                              help="prob cutoff",
                              metavar="FLOAT")
    (options, args) = options_parser.parse_args()
    # print(options.__dict__)
    inFile = Path(options.input_file)
    pdb_dir = Path(options.pdb_dir)
    cutoff = float(options.probcut)
    download_pdb(inFile, cutoff, pdb_dir)
