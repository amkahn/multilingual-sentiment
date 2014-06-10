#!/opt/python-2.7/bin/python2.7

# Andrea Kahn
# June 9, 2014
#
# This script takes as arguments an input filename and one of {en, es, de} (the language of
# the input file) and writes to standard out a version of the input file with negation-
# tagging.
#
# This script expects an input file in the following format:
# <ID>\t<quote>\t<source>\t<target>
# It only performs negation tagging on the <quote> portion.


from sys import argv
from sys import stderr
import re


# This function takes a string of text and a language ('en', 'es', or 'de'} as input and
# returns a neg-tagged version of the string.

def neg_tag(text, lang):
    neg_words = {'en': ['not', 'n\'t', 'no', 'nothing', 'nobody', 'never', 'nowhere', 'neither'],
'es': ['no', 'ning\xc3n', 'ninguna', 'ninguno', 'nada', 'nadie', 'nie', 'ni'],
'de': ['nicht', 'kein', 'keinen', 'keinem', 'keine', 'keines', 'keiner', 'nichts', 'niemand', \
'niemanden', 'niemandem', 'niemands', 'nie', 'niemals', 'nimmer', 'nirgendwo', 'weder']}
    punct = re.compile(r'\W+$')
    tokens = text.split()
    
    neg_tokens = []
    negate = False
    
    for token in tokens:
        if token in neg_words[lang]:
            negate = True
        elif punct.match(token):
            negate = False

        if negate:
            neg_tokens.append('NOT_'+token)
        else:
            neg_tokens.append(token)

    return ' '.join(neg_tokens)            


def main():
    quote_file = open(argv[1])
    language = argv[2]
    
    for line in quote_file:
        line_elements = line.strip().split('\t')
        if len(line_elements) != 4:
            stderr.write("Warning: Input file line not in expected format: %s\n" % line_elements)
            stderr.write("Skipping line\n")
        else:
            id = line_elements[0].decode('UTF-8')
            try:
                quote = line_elements[1].decode('UTF-8')
            except UnicodeDecodeError:
                quote = line_elements[1]
                stderr.write("Warning: Cannot decode quote: %s\n" % quote)
            source = line_elements[2].decode('UTF-8')
            target = line_elements[3].decode('UTF-8')

#           stderr.write("Here is the quote before tagging: %s\n" % quote.encode('UTF-8'))
            neg_quote = neg_tag(quote, language)
#           stderr.write("Here is the quote after tagging: %s\n" % neg_quote.encode('UTF-8'))
            try:           
                print id.encode('UTF-8')+'\t'+neg_quote.encode('UTF-8')+'\t'+\
source.encode('UTF-8')+'\t'+target.encode('UTF-8')
            except UnicodeDecodeError:
                stderr.write("Warning: Cannot encode quote: %s\n" % quote)
                print id.encode('UTF-8')+'\t'+neg_quote+'\t'+\
source.encode('UTF-8')+'\t'+target.encode('UTF-8')

    quote_file.close()


if __name__=='__main__':
    main()