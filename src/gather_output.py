#!/opt/python-3.1/bin/python3
#
# Claire Jaja
# Code last updated 6/9/2014
#
# Given a directory with MaxEnt and NaiveBayes results,
# this code will read in the stdout files
# and output the average, min, and max of trials 0 - 9

import sys

def main():
    # first argument is the input folder
    input_dir = sys.argv[1].rstrip("/")
    # write output to stdout
    output_file = sys.stdout

    MaxEnt_total = 0
    MaxEnt_min = float('inf')
    MaxEnt_max = float('-inf')

    # for MaxEnt, trials 0 - 9
    for n in range(10):
        filename = input_dir+"/MaxEnt."+str(n)+".stdout"
        results_file = open(filename,'r')
        results = results_file.readlines()
        results_file.close()
        last_line = results[-1].split()
        test_acc = float(last_line[5])
        MaxEnt_total += test_acc
        if test_acc < MaxEnt_min:
            MaxEnt_min = test_acc
        if test_acc > MaxEnt_max:
            MaxEnt_max = test_acc

    NaiveBayes_total = 0
    NaiveBayes_min = float('inf')
    NaiveBayes_max = float('-inf')

    # for NaiveBayes, trials 0 - 9
    for n in range(10):
        filename = input_dir+"/NaiveBayes."+str(n)+".stdout"
        results_file = open(filename,'r')
        results = results_file.readlines()
        results_file.close()
        last_line = results[-1].split()
        test_acc = float(last_line[5])
        NaiveBayes_total += test_acc
        if test_acc < NaiveBayes_min:
            NaiveBayes_min = test_acc
        if test_acc > NaiveBayes_max:
            NaiveBayes_max = test_acc

    output_file.write("system\taverage\tmin\tmax\n")
    output_file.write("MaxEnt\t"+str(MaxEnt_total/10)+"\t"+str(MaxEnt_min)+"\t"+str(MaxEnt_max)+"\n")
    output_file.write("NaiveBayes\t"+str(NaiveBayes_total/10)+"\t"+str(NaiveBayes_min)+"\t"+str(NaiveBayes_max)+"\n")

main()
