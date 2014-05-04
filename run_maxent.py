#!/opt/python-3.1/bin/python3
#
# Claire Jaja
# Code last updated 4/30/14
#
# The command line is ./run_maxent.py input_dir output_dir
#
# input_dir is a directory where each sub-directory represents a class
# The files in the directory are text documents that belong to that class
#
# output_dir is a directory that stores the output files from the tagger
# it will include the following:
# train.vectors.txt
# test.vectors.txt
# train.vectors
# test.vectors
# MaxEnt.model
# MaxEnt.out
# MaxEnt.err

import sys
from collections import Counter
import os
import re
import subprocess

def main():
	# first argument is the input directory
	input_dir = sys.argv[1]
	# second argument is the output directory
	output_dir = sys.argv[2]

    # create output directory if it doesn't already exist
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

    # create vectors from input_dir items
    train_vectors,test_vectors = create_vectors(input_dir)

    # print train vectors to train.vectors.txt in output_dir
	train_vectors_file = open(output_dir+'/train.vectors.txt','w')
	for vector in train_vectors:
		# first two items are instance name and label
        # because of issue with Mallet, replace "," with "comma"
		instance_name = re.sub(',','comma',vector[0])
		label = re.sub(',','comma',vector[1])
		train_vectors_file.write(instance_name+" "+label+" ")
		for feature in train_vectors[2:]:
			feature = re.sub(',','comma',feature)
			train_vectors_file.write(feature+" 1 ")
		train_vectors_file.write("\n")
	train_vectors_file.close()

    # print test vectors to test.vectors.txt in output_dir
	test_vectors_file = open(output_dir+'/test.vectors.txt','w')
	for vector in test_vectors:
		# first two items are instance name and label
        # because of issue with Mallet, replace "," with "comma"
		instance_name = re.sub(',','comma',vector[0])
		label = re.sub(',','comma',vector[1])
		test_vectors_file.write(instance_name+" "+label+" ")
		for feature in test_vectors[2:]:
			feature = re.sub(',','comma',feature)
			test_vectors_file.write(feature+" 1 ")
		test_vectors_file.write("\n")
	test_vectors_file.close()

    # run mallet commands
    mallet_maxent(output_dir)


def create_vectors(input_dir):
    train_vectors = []
    test_vectors = []
    # for each directory in the input directory
    possible_dir = [os.path.join(input_dir,x) for x in os.listdir(input_dir)]
    for dir in [x for x in possible_dir if os.path.isdir(x)]:
        # grab its name as the label for those files
        label = os.path.basename(dir)
        possible_files = [os.path.join(dir,x) for x in os.listdir(dir)]
        files = [x for x in possible_files if os.path.isfile(x)]
        # use first 90% files as train, last 10% as test
        train_test_split = int(len(files)*.9)
        for i in range(len(files)):
            # for each file, build a vector
            instance_name = os.path.basename(files[i])
            vector = [instance_name,label]
            current_file = open(files[i],'r'):

                # unigram features
                unigrams = Counter()
                for line in current_file:
                    for unigram in line.split():
                        unigrams[unigram] += 1
            for unigram_feature in unigrams.keys():
                vector.append(unigram_feature)

            current_file.close()

            if i < train_test_split:
                train_vectors.append(vector)
            else:
                test_vectors.append(vector)

    return train_vectors,test_vectors


def mallet_maxent(directory):
	# use mallet import-file to convert vectors into binary format
	# input: final_train.vectors.txt, final_test.vectors.txt
	# will create: final_train.vectors, final_test.vectors	
	subprocess.call(["mallet","import-file","--input "+directory+"/train.vectors.txt","--output "+directory+"/train.vectors"])
	subprocess.call(["mallet","import-file","--input "+directory+"/test.vectors.txt","--output "+directory+"/test.vectors","--use-pipe-from "+directory+"/train.vectors"])

	# use vectors2classify to train and test model
	# input: final_train.vectors, final_test.vectors
	# output: me_model, training accuracy, testing accuracy
	subprocess.call(["vectors2classify","--training-file",directory+"/train.vectors","--testing-file",directory+"/test.vectors","--trainer","MaxEnt","--report","test:raw","test:accuracy","test:confusion","train:accuracy","train:confusion","--output-classifier",directory+"/MaxEnt.model"],stdout=open(directory+"/MaxEnt.stdout",'w'),stderr=open(directory+"/MaxEnt.stderr",'w'))


main()
