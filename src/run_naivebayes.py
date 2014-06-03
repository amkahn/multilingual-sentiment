#!/opt/python-3.1/bin/python3
#
# Claire Jaja
# Code last updated 6/3/14
#
# The command line is ./run_naivebayes.py dir
#
# This assumes the experiment has already been run with run_maxent.py
# and will use the train and test vectors from the given directory
# It will add the following output files:
# NaiveBayes.model
# NaiveBayes.out
# NaiveBayes.err

import sys
from collections import Counter
import os
import re
import subprocess

def main():
    # first argument is the directory
    dir = sys.argv[1]

    # run mallet commands
    sys.stderr.write("Running Naive Bayes...\n")
    mallet_naivebayes(dir,10)

def mallet_naivebayes(directory,n):
    for i in range(n):
        sys.stderr.write("Trial #"+str(i)+"\n")

    	# use vectors2classify to train and test model
	    # input: train.n.vectors, test.n.vectors
    	# output: model, training accuracy, testing accuracy
        subprocess.call(["vectors2classify","--training-file",directory+"/train."+str(i)+".vectors","--testing-file",directory+"/test."+str(i)+".vectors","--trainer","NaiveBayes","--report","test:raw","test:accuracy","test:confusion","train:accuracy","train:confusion","--output-classifier",directory+"/NaiveBayes."+str(i)+".model"],stdout=open(directory+"/NaiveBayes."+str(i)+".stdout",'w'),stderr=open(directory+"/NaiveBayes."+str(i)+".stderr",'w'))


main()
