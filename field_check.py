#!/usr/bin/env python3

"""
check the fields of each bib item under diff types of bibitems.
usage:
  ./field_check.py -b tests/input.bib

"""
import string
import re
import sys
from optparse import OptionParser

# Parse options
usage = sys.argv[0] + " [-b|--bib=<input.bib>] [-h|--help]"

parser = OptionParser(usage)

parser.add_option("-b", "--bib", dest="bibFile",
                  help="Bib File", metavar="input.bib", default="input.bib")

(options, args) = parser.parse_args()

print("INFO: Reading references from '" + options.bibFile + "'")
try:
    fIn = open(options.bibFile, 'r', encoding="utf8")
except IOError as e:
    print("ERROR: Input bib file '" + options.bibFile +
          "' doesn't exist or is not readable")
    sys.exit(-1)

# === load the types of bib items ===
set_bibType = set()
for line in fIn:
    line = line.strip("\n")
    if line.startswith("@"):
        # currentId = line.split("{")[1].rstrip(",\n")
        currentType = line.split("{")[0].strip("@ ")
        set_bibType.add(currentType)

print('Types of bib items contained in this file: ', set_bibType)

# === by types, check the fileds' intersection and unionSet
for type_i in set_bibType:

    print('\nFor type: [[ ', type_i,  ' ]], check the fields\' intersec and Union' )

    '''============>>>> section of loop on each type =========='''
    lastId = ''  # for comparison for triggering between current ID and new ID.
    field_dict = {}

    fIn = open(options.bibFile, 'r', encoding="utf8")
    for line in fIn:
        line = line.strip("\n")

        if line.startswith("@"):
            currentId = line.split("{")[1].rstrip(",\n")
            currentType = line.split("{")[0].strip("@ ")

        if currentType == type_i:
            if currentId == lastId:
                if "=" in line:
                    # biblatex is not case sensitive
                    field = line.split("=")[0].strip().lower()
                    field_dict[lastId].add(field)
            else:
                lastId = currentId
                field_dict[lastId] = set()


    # fields loaded, do union and itersection
    list_field = [field_dict[key] for key in field_dict.keys()]
    interSecFields = list_field[0].intersection(*list_field)
    unionFields = list_field[0].union(*list_field)

    print('For Type ', type_i, '. The intersection of fields are:', interSecFields,
          '\n                     The union of fields are:', unionFields
          )
    '''<<<<<<<========== section of loop on each type =========='''

