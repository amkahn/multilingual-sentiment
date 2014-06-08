#!/opt/python-3.1/bin/python3
#
# Claire Jaja
# Code last updated 6/7/14
#
# The command line is ./run_maxent.py input_dir output_dir sentiment_lexicon
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
#
# The sentiment lexicon will be used for creating the feature vectors.

import sys
from collections import defaultdict, Counter 
import os
import re
import subprocess

def main():
    # first argument is the input directory
    input_dir = sys.argv[1]
    # second argument is the output directory
    output_dir = sys.argv[2]
    # third argument is the sentiment lexicon
    sentiment_lexicon = {}
    if len(sys.argv) > 3:
        sentiment_lexicon_file = open(sys.argv[3],'r')

        # read in sentiment lexicon
        for line in sentiment_lexicon_file:
            line = line.split()
            if line[0] in sentiment_lexicon:
                sys.stderr.write("Warning: Same term occurs more than once in sentiment lexicon: "+line[0]+"\n")
            else:
                sentiment_lexicon[line[0]] = line[1]
        sentiment_lexicon_file.close()

        sys.stderr.write("Sentiment lexicon has "+str(len(sentiment_lexicon.keys()))+" entries.\n") 

    # create output directory if it doesn't already exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    # create vectors from input_dir items
    sys.stderr.write("Creating vectors...\n")
    all_train_vectors,all_test_vectors = create_vectors(input_dir,sentiment_lexicon)

    if len(all_train_vectors) > 10:
        sys.stderr.write("ERROR: More than 10 training sets!!\n")
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


def create_vectors(input_dir,sentiment_lexicon):
    all_train_vectors = [list() for i in range(10)]
    all_test_vectors = [list() for i in range(10)]
    
    # to collect unigram counts
    # since we're using 10-fold cross validation
    # this will be a nested dictionary
    # first key is which trial it's part of the test set for (0 - 9)
    # second key is a tuple of (instance_name, label) for that particular vector
    # value is a set of unigrams in that instancce
    #all_unigrams = defaultdict(lambda:defaultdict(set))
    #all_bigrams = defaultdict(lambda:defaultdict(set))
    all_trigrams = defaultdict(lambda:defaultdict(set))
    # meanwhile keep track of training unigram counts for each trial
    # first key is which trial it's counting training unigrams for (0 - 9)
    # second key is the unigram, value is its count
    #training_unigram_counts = defaultdict(Counter)
    #training_bigram_counts = defaultdict(Counter)
    training_trigram_counts = defaultdict(Counter)

    # for each directory in the input directory
    possible_dir = [os.path.join(input_dir,x) for x in os.listdir(input_dir)]
    for dir in [x for x in possible_dir if os.path.isdir(x)]:
        # grab its name as the label for those files
        label = os.path.basename(dir)
        possible_files = [os.path.join(dir,x) for x in os.listdir(dir)]
        files = [x for x in possible_files if os.path.isfile(x)]

        # use first 90% files as train, last 10% as test
        ten_percent = int(len(files)*.1)

        for i in range(len(files)):
            # for each file, collect its counts
            instance_name = os.path.basename(files[i])
            current_file = open(files[i],'r')

            # figure out which trial it will be test set for
            trial = int(i/ten_percent)

            # unigram features
            #for line in current_file:
            #    for unigram in line.split():
            #        # add to the set for that vector in its test trial
            #        all_unigrams[trial][(instance_name,label)].add(unigram)
            #        # add to the count for the training for all other trials
            #        for n in range(10):
            #            if n != trial:
            #                training_unigram_counts[n][unigram] += 1

            # bigram features
            #for line in current_file:
            #    line = line.split()
            #    for j in range(1,len(line)):
            #        bigram = line[j-1]+"-"+line[j]
            #        # add to the set for that vector in its test trial
            #        all_bigrams[trial][(instance_name,label)].add(bigram)
            #        # add to the count for the training for all other trials
            #        for n in range(10):
            #            if n != trial:
            #                training_bigram_counts[n][bigram] += 1

            # trigram features
            for line in current_file:
                line = line.split()
                for j in range(2,len(line)):
                    trigram = line[j-2]+"-"+line[j-1]+"-"+line[j]
                    # add to the set for that vector in its test trial
                    all_trigrams[trial][(instance_name,label)].add(trigram)
                    # add to the count for the training for all other trials
                    for n in range(10):
                        if n != trial:
                            training_trigram_counts[n][trigram] += 1

            current_file.close()

    # for every trial, create its vectors
    # test vectors will be those in that trial
    # all others are train vectors for that trial
    cut_off = 3
    for trial in range(10):
        # generate a set of the unigrams that occurred > cut off in training data
        #training_unigrams = set()
        #training_bigrams = set()
        training_trigrams = set()
        #for unigram,count in training_unigram_counts[trial].items():
        #for bigram,count in training_bigram_counts[trial].items():
        for trigram,count in training_trigram_counts[trial].items():
            if count >= cut_off:
                #training_unigrams.add(unigram)
                #training_bigrams.add(bigram)
                training_trigrams.add(trigram)
        # generate vectors using set of unigrams
        #for n in all_unigrams: # loop through all trials
        #for n in all_bigrams: # loop through all trials
        for n in all_trigrams: # loop through all trials
            #for key,unigrams in all_unigrams[n].items(): # metadata and set of unigrams for a file
            #for key,bigrams in all_bigrams[n].items(): # metadata and set of unigrams for a file
            for key,trigrams in all_trigrams[n].items(): # metadata and set of unigrams for a file
                (instance_name,label) = key
                vector = [instance_name, label]
                #for unigram in unigrams:
                #    if unigram in training_unigrams: # if it met the cut off in the training data
                #        vector.append(unigram)
                #for bigram in bigrams:
                #    if bigram in training_bigrams: # if it met the cut off in the training data
                #        vector.append(bigram)
                for trigram in trigrams:
                    if trigram in training_trigrams: # if it met the cut off in the training data
                        vector.append(trigram)
                if n == trial: # test vector
                    all_test_vectors[trial].append(vector)
                else: # train vector
                    all_train_vectors[trial].append(vector)

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
