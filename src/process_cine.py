#!/opt/python-2.7/bin/python2.7

# Andrea Kahn
# May 2, 2014
#
# This script takes a review file as input and prints the rating and the tokenized text separated by a space.


from bs4 import BeautifulSoup
from sys import argv
from sys import stderr
from nltk import sent_tokenize, word_tokenize


def main():
    xml_file = open(argv[1])
    rating, text = extract_review_attributes(xml_file)
    print rating,
    # Perform pre-processing (tokenization, case collapsing) on the review text
#    stderr.write("ORIGINAL REVIEW TEXT:\n%s\n" % text)
    text = text.lower()
#    stderr.write("LC REVIEW TEXT:\n%s\n" % text)
#    stderr.write(str(type(text))) # should be unicode
    text = text.encode('UTF-8')
    tokens = [word for sent in sent_tokenize(text) for word in word_tokenize(sent)]
    text = ' '.join(tokens)
#    stderr.write("TOKENIZED REVIEW TEXT:\n%s\n" % text)
    print text
    xml_file.close()


# This method takes a review file as input and returns a 2-tuple of the review rating and text.

def extract_review_attributes(file):
    parsed = BeautifulSoup(file)
    
# FIXME: This causes an error -- not sure why? Also make sure stderr will print from shell
# Make sure that the review rating is out of 5
    if parsed.review['maxrank']!='5':
        stderr.write("WARNING: Rating is not out of 5 in file %s\n" % argv[1])

    rating = parsed.review['rank']
    # FIXME: This includes the summary text.
    text = parsed.review.get_text()
    return (rating, text)


if __name__ == '__main__':
	main()