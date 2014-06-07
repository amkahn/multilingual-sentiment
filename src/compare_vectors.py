#!/opt/python-3.1/bin/python3
#
# Claire Jaja
# 6/7/14
#
# This script will read in two files of vectors
# store the data
# then tell you where there are differences

import sys
from collections import defaultdict

def main():
    # first argument is one of the vectors files
    vectors_1_file = open(sys.argv[1],'r')
    # second argument is second vectors files
    vectors_2_file = open(sys.argv[2],'r')

    vectors_1 = process_vectors(vectors_1_file)
    vectors_2 = process_vectors(vectors_2_file)

    vectors_1_file.close()
    vectors_2_file.close() 

    compare_vectors(vectors_1,vectors_2)

def process_vectors(vectors_file):
    # key is (instance name, label) tuple, value is set of (feature,value) tuples
    vectors = defaultdict(set)
    for line in vectors_file:
        line = line.split()
        instance_name = line[0]
        label = line[1]
        for i in range(2,len(line),2): # every other item is a feature
            vectors[(instance_name, label)].add((line[i],line[i+1]))
    return vectors

def compare_vectors(vectors_1,vectors_2):
    # check that all same instances included
    if vectors_1.keys() != vectors_2.keys():
        print("Different instances included!")
    else:
        for k,v in vectors_1.items():
            if vectors_2[k] != v:
                print("Different features included!")
                for feature in v:
                    if feature not in vectors_2[k]:
                        print(feature)

main()
