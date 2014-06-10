#!/opt/python-3.1/bin/python3
#
# Claire Jaja
# Code last updated 6/9/2014
#
# Given a directory with MaxEnt and NaiveBayes results,
# this code will read in the stdout files
# and output the misclassified files
# in the format <instance name>\t<real label>\t<sys label>

import sys

def main():
    # first argument is the input folder
    input_dir = sys.argv[1].rstrip("/")
    # write output to stdout
    output_file = sys.stdout

    # hacky way of finding correct lines
    possible_labels = ["pos","neg","subj_tok","obj_tok"]

    output_file.write("Misclassified files for "+str(input_dir)+"\n\n")

    # for MaxEnt, trials 0 - 9
    for x in ["MaxEnt","NaiveBayes"]:
        output_file.write("With "+x+"\n\n")
        output_file.write("instance name\treal label\tsys label\n")
        for n in range(10):
            filename = input_dir+"/"+x+"."+str(n)+".stdout"
            results_file = open(filename,'r')
            for line in results_file:
                line = line.split()
                if len(line) == 4 and line[1] in possible_labels:
                    real_label = line[1]
                    label_1,weight_1 = line[2].split(":")
                    label_2,weight_2 = line[3].split(":")
                    weight_1 = float(weight_1)
                    weight_2 = float(weight_2)

                    if weight_1 > weight_2:
                        sys_label = label_1
                    else:
                        sys_label = label_2

                    if sys_label != real_label:
                        output_file.write(line[0]+"\t"+real_label+"\t"+sys_label+"\n")

            results_file.close()

        output_file.write("\n")


main()
