#!/usr/bin/env python3

'''
  If there are too many authors, you can just take the first few authors and add "and others" at the end, and Latex will automatically generate 'et al.'
  if the bibliography list contains items that has more than three authors, make the authors overflow as 'and others'
  for example:
    Danon et al.(2005)Danon, Diaz-Guilera, Duch, and Arenas] Danon L, Diaz-Guilera A, Duch J, Arenas A (2005) Comparing community structure identification. Journal of Statistical Mechanics: Theory and Experiment 2005(09):P09008

    should be referenced as:

    [Danon et al.(2005)] Danon L, Diaz-Guilera A, Duch J et al. (2005) Comparing community structure identification. Journal of Statistical Mechanics: Theory and Experiment 2005(09):P09008


  Environment requirement for latex:
    - use biblatex as the bibliography management package
    - \bibliographystyle{apalike} % or {spbasic} for spring latex template
    - \bibliography{mybibfile}    % with mybibfile.bib affiliated


Usage:
  ./count_authors.py -b tests/input_real.bib
'''

import sys
from optparse import OptionParser


# Parse options
usage = sys.argv[
    0] + " [-b|--bib=<input.bib>] [-o|--output=<output/filter_output.bib>]  [-h|--help]"

parser = OptionParser(usage)

parser.add_option("-b", "--bib", dest="bibFile",
                  help="Bib File", metavar="input.bib", default="input_real.bib")

parser.add_option("-o", "--output", dest="outputFile",
                  help="bib Output File after filtered", metavar="output/filter_output.bib", default="output/filter_output.bib")

(options, args) = parser.parse_args()

# load the bib file
print("INFO: Reading references from '" + options.bibFile + "'")
try:
    fIn = open(options.bibFile, 'r', encoding="utf8")
except IOError as e:
    print("ERROR: Input bib file '" + options.bibFile +
          "' doesn't exist or is not readable")
    sys.exit(-1)

# file writer for output the filter result
if options.outputFile:
    fo = open(options.outputFile, 'w', encoding="utf8")
lines_write = []
# =========================================
# =========================================

count_ands = 0
positive_toomanyAth = 0
for line in fIn:
    # preprocess
    linee = line.strip("\n")
    linee = linee.replace(" = ", "=")

    # process line with ID
    if linee.startswith("@"):
        currentId = linee.split("{")[1].rstrip(",\n")
        currentType = linee.split("{")[0].strip("@ ")
        lines_write.append(line)

    elif "=" in linee:  # lines of bib contents
        field = linee.split("=")[0].strip().lower()
        '''  process field of authors >>> '''
        if field == 'author':
            assert ',' in linee, 'The tail of this line is not \',\'! ' + linee
            count_ands += 1
            field_string = linee.split("=")[1].strip('{').strip('},')
            field_string_andsplit = field_string.split(' and ')
            # print(field_string_andsplit)
            if len(field_string_andsplit) > 3:
                positive_toomanyAth += 1
                print('  >> The too many authors in bibID:', currentId)
                fsar = field_string_andsplit[:3]  # field string andsplit remained
                # build linee # construct the line with remained authors:
                linee = '  ' + field + '={' + fsar[0] + ' and ' + fsar[1] + ' and ' + fsar[2] + ' and others' + '},'

        '''  <<< process field of authors '''
        lines_write.append(linee + '\n')
    else:  # line with no = , no @
        lines_write.append(line)


print()
print('How many of author_fields have been counted (positive/total):', positive_toomanyAth, '/', count_ands)

# check the ',\n}' in lines_write
for i_line in range(len(lines_write)):
    if lines_write[i_line] != '\n':
        if lines_write[i_line].strip("\n")[-1] == ',' and lines_write[i_line+1][0] == '}':
            lines_write[i_line] = lines_write[i_line][:-2] + '\n'

fo.writelines(lines_write)

print('\nFilter finished! The result is saved at:', options.outputFile, end='\n\n')

