#!/opt/python-3.1/bin/python3
#
# Claire Jaja
# Code last updated 6/1/14
#
# This script will take the tab separated German quotes
# and generate two files
# one with positive quotes, one with negative quotes
# only those agreed upon by annotators
#
# The output file will be in thei format
# <id>\t<quote>\t<source name>i\t<target name>

import sys

def main():
    # first argument is the tab separated quotes
    input_quotes = sys.stdin
    # write output to three files in current directory
    # one named "pos.txt" one named "neg.txt" one named "obj.txt"
    output_pos_quotes = open("pos.txt","w")
    output_neg_quotes = open("neg.txt","w")
    output_obj_quotes = open("obj.txt","w")

    # store my quotes in a list of tuples
    pos_quotes = []
    neg_quotes = []
    obj_quotes = []
    for line in input_quotes:
        line = line.strip().split("\t")[2:]
        #print(line)
        # last item says whether or not annotators agreed
        if line and line[-1] == "TRUE":
            # first item will be the id
            id = line[0]
            # second item will be the quote
            quote = line[1]
            # third item will be the source name
            source_name = line[2]
            # don't care about fourth and fifth items
            # sixth item will be the target name
            target_name = line[5]
            # 7th and 9th lines will be the annotated polarity
            annotated_polarity = [line[6],line[8]]
            if annotated_polarity[0] != annotated_polarity[1]:
                sys.stderr.write("Warning: Annotators didn't agree?\n"+str(annotated_polarity)+"\n")
            else:
                polarity = annotated_polarity[0]
                if polarity == "POS":
                    pos_quotes.append((id,quote,source_name,target_name))
                elif polarity == "NEG":
                    neg_quotes.append((id,quote,source_name,target_name))
                elif polarity == "OBJ":
                    obj_quotes.append((id,quote,source_name,target_name))
                else:
                    sys.stderr.write("Warning: Polarity other than POS, NEG, or OBJ\n"+polarity+"\n")

    for pos_quote in pos_quotes:
        output_pos_quotes.write("\t".join(pos_quote)+"\n")
    for neg_quote in neg_quotes:
        output_neg_quotes.write("\t".join(neg_quote)+"\n")
    for obj_quote in obj_quotes:
        output_obj_quotes.write("\t".join(obj_quote)+"\n")

    output_pos_quotes.close()
    output_neg_quotes.close()
    output_obj_quotes.close()


main()
