#!/opt/python-2.7/bin/python2.7

# Andrea Kahn
# June 3, 2014
#
# This script takes an input file in the following format:
# <ID>\t<quote>\t<source>\t<target>
# It then prints this to an output file, tokenizing and lowercasing the quote.


from sys import argv
from sys import stderr
from nltk import sent_tokenize, word_tokenize


def main():
    in_file = argv[1]
    out_file = argv[2]
    
    in_file = open(in_file)
    out_file = open(out_file, 'w')
    
    for line in in_file:
        line_elements = line.strip().split('\t')
        if len(line_elements) != 4:
            stderr.write("Warning: Input file line not in expected format: %s\n" % line_elements)
            stderr.write("Skipping line\n")
        else:
#           stderr.write("DEBUG  Here is the quote before processing: %s\n" % line_elements[1])
#           stderr.write(str(type(quote))+'\n') # should be unicode
            id = line_elements[0].decode('UTF-8')
            source = line_elements[2].decode('UTF-8')
            target = line_elements[3].decode('UTF-8')

#           try:
            quote = line_elements[1].decode('UTF-8')
#           except UnicodeDecodeError:
#               stderr.write("Cannot decode quote: %s\n" % quote)

            quote = quote.lower()
            tokens = [word for sent in sent_tokenize(quote) for word in word_tokenize(sent)]
            quote = ' '.join(tokens)
#           stderr.write("DEBUG  Here is the processed quote: %s\n" % quote)
            out_file.write(id.encode('UTF-8')+'\t')

#           try:
            out_file.write(quote.encode('UTF-8')+'\t')
#           except UnicodeEncodeError:
#               stderr.write("Cannot decode quote: %s\n" % quote)

            out_file.write(source.encode('UTF-8')+'\t')
            out_file.write(target.encode('UTF-8')+'\n')
    
    in_file.close()
    out_file.close()
    
if __name__=='__main__':
    main()