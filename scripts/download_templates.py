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


def download_pdb(in_file: Path, pdb_dir: Path):
    """
        read the input list and download pdb
    """
    pdb_lst = []
    print("parsing ",in_file)
    with open(in_file) as oF:
        for line in oF:
            line = line.strip()
            (q,p,rest)=line.split()
            rest=rest.strip(',')
            pdb_lst = rest.split(',')

    print(f"Will download {len(pdb_lst)} files")
    for i in pdb_lst:
        print(f"Getting {i}")
        pdb, chainid = i.split("_")
        pdbid = pdb.lower()
        file_name = pdbid + ".pdb"
        file_path = pdb_dir / file_name
        if file_path.is_file(): 
            print("file already downloaded!")
        else:
            url = "http://www.rcsb.org/pdb/files/" + pdbid + ".pdb.gz"
            try : 
                with urllib.request.urlopen(url) as response:
                    with gzip.GzipFile(fileobj=response) as uncompressed:
                        with open(file_path, 'wb') as out_file:
                            data = uncompressed.read()
                            out_file.write(data)
            except urllib.error.URLError as e:
                print(e)
                continue


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

    if fileout_path.is_file():
        print(file_out,end=" ")
        print("already exists!")
    else:
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
    (options, args) = options_parser.parse_args()
    # print(options.__dict__)
    inFile = Path(options.input_file)
    pdb_dir = Path(options.pdb_dir)
    download_pdb(inFile, pdb_dir)
