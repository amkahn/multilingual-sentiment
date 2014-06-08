#!/opt/python-2.7/bin/python2.7

# Andrea Kahn
# June 7, 2014
#
# This script takes as arguments the path to a file of Spanish lexicon terms, the path to
# a file of lexicon tags, and a path to the desired output file for the new Spanish lexicon.
#
# Input file #1 format:
# w1
# w2
#
# Input file #2 format:
# neg
# pos
#
# Output file format:
# w1\tneg
# w2\tpos

from sys import argv
from sys import stderr

def main():
    term_file = open(argv[1])
    tag_file = open(argv[2])
    lex_file = open(argv[3], 'w')
    
    for line in term_file:
        term = line.strip().decode('UTF-8')
        term = term.lower()
        tag = tag_file.readline().strip()
        lex_file.write(term.encode('UTF-8')+'\t'+tag+'\n')
    
    lex_file.close()
    term_file.close()
    tag_file.close()

if __name__ == '__main__':
    main()