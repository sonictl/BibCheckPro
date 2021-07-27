#!/usr/bin/env python

"""
This is the sister code for 'field_check.py'
This code filters out the redundant field for bib items.

About implementation, this time, I read data into a construction for processing.


"""
import string
import re
import sys
from optparse import OptionParser

# Parse options
usage = sys.argv[
    0] + " [-b|--bib=<input.bib>]  [-o|--output=<filter_output.bib>]  [-h|--help]"
parser = OptionParser(usage)

parser.add_option("-b", "--bib", dest="bibFile",
                  help="Bib File", metavar="input.bib", default="input.bib")

parser.add_option("-o", "--output", dest="outputFile",
                  help="bib Output File after filtered", metavar="filter_output.bib", default="filter_output.bib")

(options, args) = parser.parse_args()

print("INFO: Reading references from '" + options.bibFile + "'")
try:
    fIn = open(options.bibFile, 'r', encoding="utf8")
except IOError as e:
    print("ERROR: Input bib file '" + options.bibFile +
          "' doesn't exist or is not readable")
    sys.exit(-1)

# =========================================
# =========================================

field_remain_dict = {}

'''>>>>>> configure the fields that need to retain for each type of bib item >>>>>'''
types_bib = {'techreport', 'inproceedings', 'article'}
field_remain_dict['techreport']     = {'title',
                                       'institution',
                                       'year',
                                       'author'}

field_remain_dict['inproceedings']  = {'pages',
                                       'title',
                                       'year',
                                       'author',
                                       'booktitle'}

field_remain_dict['article']        = {'journal',
                                       'pages',
                                       'volume',
                                       'title',
                                       'year',
                                       'author'}

'''<<<< configure the fields that need to retain for each type of bib item <<<<<<<<'''


set_bibType = set(types_bib)

# # === load the types of bib items ===
# set_bibType = set()
# for line in fIn:
#     line = line.strip("\n")
#     if line.startswith("@"):
#         # currentId = line.split("{")[1].rstrip(",\n")
#         currentType = line.split("{")[0].strip("@ ")
#         set_bibType.add(currentType)
#
# print('Types of bib items contained in this file: ', set_bibType)

# file writer for output the filter result
if options.outputFile:
    fo = open(options.outputFile, 'w', encoding="utf8")

# === by types, check the fileds' intersection and unionSet
lines_write = []
for type_i in set_bibType:

    print('For type: [[ ', type_i,  ' ]], check the fields\' intersec and Union' )

    '''============>>>> section of loop on each type =========='''
    lastId = ''  # for comparison for triggering between current ID and new ID.
    field_dict = {}

    fIn = open(options.bibFile, 'r', encoding="utf8")
    for line in fIn:
        linee = line.strip("\n")

        if linee.startswith("@"):
            currentId = linee.split("{")[1].rstrip(",\n")
            currentType = linee.split("{")[0].strip("@ ")

        if currentType == type_i:
            if linee.startswith("@"):
                # fo.write(line)
                lines_write.append(line)
            elif "=" in linee:
                field = linee.split("=")[0].strip().lower()
                if field in field_remain_dict[currentType]:
                    # fo.write(line)
                    lines_write.append(line)
            else:
                # fo.write(line)
                lines_write.append(line)

    '''<<<<<<<========== section of loop on each type =========='''

# check the ',\n{' in lines_write
for i_line in range(len(lines_write)):
    if lines_write[i_line] != '\n':
        if lines_write[i_line].strip("\n")[-1] == ',' and lines_write[i_line+1][0] == '}':
            # print(lines_write[i_line], end= ' >> ')
            lines_write[i_line] = lines_write[i_line][:-2] + '\n'
            # print(lines_write[i_line])

fo.writelines(lines_write)
