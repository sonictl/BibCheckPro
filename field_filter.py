#!/usr/bin/env python3

"""
This is the sister code for 'field_check.py'
This code filters out the redundant field for bib items.

Usage:
  configure in line43-60 before running
  ./field_filter.py -b input/input_real.bib -o output/filter_output.bib

"""
import string
import re
import sys
from optparse import OptionParser
from titlecase import titlecase    # pip install titlecase, for title into case proper.


# Parse options
usage = sys.argv[
    0] + " [-b|--bib=<input/input.bib>]  [-o|--output=<output/filter_output.bib>] [-t|--titlecase=<yes/no>] [-h|--help]"
parser = OptionParser(usage)

parser.add_option("-b", "--bib", dest="bibFile",
                  help="Bib File", metavar="input.bib", default="input_real.bib")

parser.add_option("-o", "--output", dest="outputFile",
                  help="bib Output File after filtered", metavar="output/filter_output.bib", default="output/filter_output.bib")

parser.add_option("-t", "--titlecase", dest="if_titlecase",
                  help="if titlecase the name of journal/proceedings: yes or no (default)", metavar="if title case", default='no')

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
                                       'booktitle',
                                       'publisher'}

field_remain_dict['article']        = {'journal',
                                       'pages',
                                       'volume',
                                       'number',
                                       'title',
                                       'year',
                                       'author'}

field_titlecase = ['journal', 'booktitle', 'institution']   # the fields that need to be converted into title case.

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
lines_write = []  # lines to write into file
currentType = ''
for type_i in set_bibType:

    print('For type: [[ ', type_i,  ' ]], filter the fields and remain:', field_remain_dict[type_i] )

    '''============>>>> section of loop on each type =========='''
    lastId = ''  # for comparison for triggering between current ID and new ID.
    field_dict = {}

    fIn = open(options.bibFile, 'r', encoding="utf8")   # opening file for each loop
    for line in fIn:
        linee = line.strip("\n")
        linee = linee.replace(" = ", "=")

        if linee.startswith("@"):
            currentId = linee.split("{")[1].rstrip(",\n")
            currentType = linee.split("{")[0].strip("@ ")

        if currentType!='' and currentType == type_i:   # carding by type_i
            if linee.startswith("@"):   # line of bibID
                lines_write.append(line)
            elif "=" in linee:          # lines of bib contents
                field = linee.split("=")[0].strip().lower()
                ''' upper case the journal name, reconstruct the line >>>> '''
                if (options.if_titlecase == 'yes') and (field in field_titlecase):
                    assert ',' in linee, 'The tail of this line is not \',\'! ' + linee
                    field_string = linee.split("=")[1].strip('{').strip('},')
                    field_string = titlecase(field_string)    # upper case the letters that meets title case req.
                    line = '  ' + field + '={' + field_string + '},\n'   # construct the line with titlecased string
                ''' <<< upper case the journal name: '''
                if field in field_remain_dict[currentType]:  # if field in remaining list,
                    lines_write.append(line)
            else:
                lines_write.append(line)

    '''<<<<<<<========== section of loop on each type =========='''

# check the ',\n{' in lines_write
for i_line in range(len(lines_write)):
    if lines_write[i_line] != '\n':
        if lines_write[i_line].strip("\n")[-1] == ',' and lines_write[i_line+1][0] == '}':
            lines_write[i_line] = lines_write[i_line][:-2] + '\n'

fo.writelines(lines_write)

print('\nFilter finished! The result is saved at:', options.outputFile, end='\n\n')
