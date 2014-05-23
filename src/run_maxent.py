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
    sys.stderr.write("Creating vectors...\n")
    all_train_vectors,all_test_vectors = create_vectors(input_dir)

    if len(all_train_vectors) > 10:
        sys.stderr.write("ERROR: More than 10 train vectors!!\n")
        sys.exit()

    # print train vectors to train.n.vectors.txt in output_dir
    for i in range(len(all_train_vectors)):
        sys.stderr.write("Printing vector "+str(i)+"...\n")
        train_vectors = all_train_vectors[i]
        train_vectors_file = open(output_dir+'/train.'+str(i)+'.vectors.txt','w')
        for vector in train_vectors:
            #sys.stderr.write("Here is a training vector: "+str(vector)+"\n")
            # first two items are instance name and label
            # because of issue with Mallet, replace "," with "comma"
            instance_name = re.sub(',','comma',vector[0])
            label = re.sub(',','comma',vector[1])
            train_vectors_file.write(instance_name+" "+label+" ")
            for feature in vector[2:]:
                feature = re.sub(',','comma',feature)
                train_vectors_file.write(feature+" 1 ")
            train_vectors_file.write("\n")
        train_vectors_file.close()

        # print test vectors to test.vectors.txt in output_dir
        test_vectors = all_test_vectors[i]
        test_vectors_file = open(output_dir+'/test.'+str(i)+'.vectors.txt','w')
        for vector in test_vectors:
            # first two items are instance name and label
            # because of issue with Mallet, replace "," with "comma"
            instance_name = re.sub(',','comma',vector[0])
            label = re.sub(',','comma',vector[1])
            test_vectors_file.write(instance_name+" "+label+" ")
            for feature in vector[2:]:
                feature = re.sub(',','comma',feature)
                test_vectors_file.write(feature+" 1 ")
            test_vectors_file.write("\n")
        test_vectors_file.close()

    # run mallet commands
    sys.stderr.write("Running MaxEnt...\n")
    mallet_maxent(output_dir,len(all_train_vectors))


def create_vectors(input_dir):
    all_train_vectors = [list() for i in range(10)]
    all_test_vectors = [list() for i in range(10)]
    # for each directory in the input directory
    possible_dir = [os.path.join(input_dir,x) for x in os.listdir(input_dir)]
    for dir in [x for x in possible_dir if os.path.isdir(x)]:
        # grab its name as the label for those files
        label = os.path.basename(dir)
        possible_files = [os.path.join(dir,x) for x in os.listdir(dir)]
        files = [x for x in possible_files if os.path.isfile(x)]


        # use first 90% files as train, last 10% as test
        #train_test_split = int(len(files)*.9)
        #    if i < train_test_split:
        #        train_vectors.append(vector)
        #    else:
        #        test_vectors.append(vector)



        ten_percent = int(len(files)*.1)

        for i in range(len(files)):
            # for each file, build a vector
            instance_name = os.path.basename(files[i])
            vector = [instance_name,label]
            current_file = open(files[i],'r')

            # unigram features
            unigrams = Counter()
            for line in current_file:
                for unigram in line.split():
                    unigrams[unigram] += 1
            for unigram_feature in unigrams.keys():
                vector.append(unigram_feature)

            current_file.close()

            # add to appropriate training and test vectors
            # for each cross-validation trial
            for n in range(10):
                # if this vector is in the 10% of files for test for that trial
                if i >= n*ten_percent and i < (n+1)*ten_percent:
                    #sys.stderr.write("Adding vector for file #"+str(i)+": "+str(files[i])+" to test for trial #"+str(n)+"\n")
                    # use as test for this trial, train for all others
                    all_test_vectors[n].append(vector)
                    for j in range(10):
                        if j != n:
                            all_train_vectors[j].append(vector)

    return all_train_vectors,all_test_vectors


def mallet_maxent(directory,n):
	# use mallet import-file to convert vectors into binary format
	# input: final_train.vectors.txt, final_test.vectors.txt
	# will create: final_train.vectors, final_test.vectors
    for i in range(n):
        sys.stderr.write("Trial #"+str(i)+"\n")
        subprocess.call(["mallet","import-file","--input "+directory+"/train."+str(i)+".vectors.txt","--output "+directory+"/train."+str(i)+".vectors"])
        subprocess.call(["mallet","import-file","--input "+directory+"/test."+str(i)+".vectors.txt","--output "+directory+"/test."+str(i)+".vectors","--use-pipe-from "+directory+"/train."+str(i)+".vectors"])

    	# use vectors2classify to train and test model
	    # input: final_train.vectors, final_test.vectors
    	# output: me_model, training accuracy, testing accuracy
        subprocess.call(["vectors2classify","--training-file",directory+"/train."+str(i)+".vectors","--testing-file",directory+"/test."+str(i)+".vectors","--trainer","MaxEnt","--report","test:raw","test:accuracy","test:confusion","train:accuracy","train:confusion","--output-classifier",directory+"/MaxEnt."+str(i)+".model"],stdout=open(directory+"/MaxEnt."+str(i)+".stdout",'w'),stderr=open(directory+"/MaxEnt."+str(i)+".stderr",'w'))


main()
