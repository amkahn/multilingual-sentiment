#!/opt/python-2.7/bin/python2.7

from sys import argv
from sys import stderr


# This script takes as arguments the path to a file to be processed and the path to the
# desired output file.
#
# Input file format:
# Entry\tSource\tPositiv\tNegativ\tPstv\tAffil\tNgtv
# w1_1\ts1\tPositiv\t\t\t\t
# w1_2\ts2\t\tNegativ\t\t\t
# w2_1\ts3\t\tNegativ\t\tNgtv
# w3_1\ts4\tPositiv\t\t\t\t
# w4_1\ts5\t\t\t\t\t
# etc.
#
# Output file format:
# w2_1\tneg
# w3_1\tpos
#
# I.e., throw out words that:
# -have no senses that are classified as Positiv, Pstv, Negativ, or Ngtv
# -are classified as both (Positiv or Pstv) and (Negativ or Ngtv)
# -have multiple senses, at least one of which is classified as (Positiv or Pstv) and at
# leave one of which is classified as (Negativ or Ngtv)
#
# Note: Words are also lowercased in output file.


def main():
    in_file = argv[1]
    out_file = argv[2]
    
    in_file = open(in_file)
    out_file = open(out_file, 'w')
    
    # Skip first line (headers) (though nothing would be written to out_file for this
    # line anyway given code below)
    line = in_file.readline()
    
    line = in_file.readline()
    line = line.strip().split('\t')
    
    while line != ['']:       
        to_classify = []
        split_word = line[0].split('#')
        
        if len(split_word) == 1:
            # No # means there's only one line corresponding with this word; go ahead and
            # classify it
            to_classify.append(line)
            # First, read in next line and strip/split it (to match else block, which will
            # also end one line ahead)
            line = in_file.readline()
            line = line.strip().split('\t')
            
        else:
            # There is going to be at least one more line for this word; keep reading file
            # until you've appended all corresponding lines to the to_classify list
            curr_word = split_word[0]
            line_word = curr_word
            
            while line_word == curr_word:
                to_classify.append(line)
                # Check whether next line has same word; if so, append to to_classify list
                line = in_file.readline()
                line = line.strip().split('\t')
                split_word = line[0].split('#')
                line_word = split_word[0]
            
        output = classify_word(to_classify)
        if output != None:
            out_file.write(output)
    
    in_file.close()
    out_file.close()


# This function takes the lines from the input file corresponding with the sense(s) of a
# particular word and returns the corresponding line that should be printed to the output
# file, or None if the word is neither positive nor negative.

def classify_word(lines):
    stderr.write("Processing word %s\n" % lines[0][0].split('#')[0])
    
    pos = False
    neg = False
    
    for line in lines:
        if line[2] != '' or line[4] != '':
            stderr.write("Found evidence of positive\n")
            pos = True
        
        if line[3] != '' or line[6] != '':
            stderr.write("Found evidence of negative\n")
            neg = True
        
    if pos and not neg:
        stderr.write("Returning positive\n")
        return lines[0][0].split('#')[0].lower()+'\tpos\n'
    elif neg and not pos:
        stderr.write("Returning negative\n")
        return lines[0][0].split('#')[0].lower()+'\tneg\n'
#    elif pos and neg:
#        stderr.write("Word %s has evidence of negative and positive; return None\n")
#        return None
    else:
        return None


if __name__=='__main__':
    main()