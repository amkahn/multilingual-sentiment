#!/opt/python-2.7/bin/python2.7

# Andrea Kahn
# June 9, 2014
#
# This script takes as arguments an input filename and one of {en, es, de} (the language of
# the input file) and writes to standard out a version of the input file with negation-
# tagging.


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
        if token.encode('utf-8') in neg_words[lang]:
            negate = True
        elif punct.match(token):
            negate = False

        if negate:
            neg_tokens.append('NOT_'+token)
        else:
            neg_tokens.append(token)

    return ' '.join(neg_tokens)   


def main():
    review_file = open(argv[1])
    language = argv[2]
    
    for line in review_file:
        line = line.strip().decode('UTF-8')
#       stderr.write("Here is the line before tagging: %s\n" % line.encode('UTF-8'))
        neg_line = neg_tag(line, language)
#       stderr.write("Here is the line after tagging: %s\n" % neg_line.encode('UTF-8'))
        print neg_line.encode('UTF-8')

    review_file.close()


if __name__=='__main__':
    main()