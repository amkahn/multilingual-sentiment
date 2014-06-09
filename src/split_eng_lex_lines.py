#!/opt/python-2.7/bin/python2.7

# Andrea Kahn
# June 7, 2014
#
# This script takes as arguments the path to a lexicon file to be processed, the path to
# the desired output file for the lexicon terms, and a path to the desired output file for
# the lexicon tags.
#
# Input file format:
# w1\tneg
# w2\tpos
#
# Output file #1 format:
# w1
# w2
#
# Output file #2 format:
# neg
# pos

from sys import argv
from sys import stderr

def main():
    lex_file = open(argv[1])
    term_file = open(argv[2], 'w')
    tag_file = open(argv[3], 'w')
    
    for line in lex_file:
        term_tag_pair = line.strip().split('\t')
        if len(term_tag_pair) != 2:
            stderr.write("DEBUG  Bad input file line format; wrong number of tokens: %s\n" % term_tag_pair)
        else:
            term_file.write(term_tag_pair[0]+'\n')
            tag_file.write(term_tag_pair[1]+'\n')
    
    lex_file.close()
    term_file.close()
    tag_file.close()

if __name__ == '__main__':
    main()