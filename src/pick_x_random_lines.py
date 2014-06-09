#!/opt/python-3.1/bin/python3
#
# Claire Jaja
# Code last updated 6/8/2014
#
# This code will take in a file
# and generate a new file
# that contains a random x lines from the input file

import sys
import random

def main():
    # first argument is the input file
    input_file = open(sys.argv[1],'r')
    # second argument is the number of random lines to take
    x = int(sys.argv[2])
    # write output to stdout
    output_file = sys.stdout

    # first, read in entire file
    file_contents = input_file.readlines()
    input_file.close()

    # then get x random lines from file contents
    random_lines = random.sample(file_contents,x)

    # then take those lines and print to stdout
    for random_line in random_lines:
        output_file.write(random_line)

main()
