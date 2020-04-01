"""
since modeller requires a special format .ali, .fasta can be
easily converted to .ali

usage: python convert_fileformat_modeller.py <input_file> <output_file>

"""

from modeller import *
import sys

e = environ()
input_file = sys.argv[1]
output_file = sys.argv[2]
a = alignment(e, file=input_file, alignment_format='FASTA')
a.write(file=output_file, alignment_format='PIR')
