#!/bin/sh

# NEG SPANISH
# Get the file paths
FILES=$(find /home2/cjaja/classwork/spring-2014/ling575/multilingual-sentiment/data/cine_processed_2000/neg -maxdepth 1 -type f)

# Get the number of files
NUM=$(echo "$FILES" | wc -l)
echo "Number of neg Spanish review files:" $NUM

# For each file:
for FILE in $FILES; do
    # Run the python script on the file
    OUT=$(./neg_tag_review.py "$FILE" es)
     
    F=$(echo $FILE | sed "s/\/home2\/cjaja\/classwork\/spring\-2014\/ling575\/multilingual\-sentiment\/data\/cine\_processed\_2000\/neg\/\([0-9]*\)\.txt/\1/")
    echo "Negation tagging neg Spanish review $F"
    echo $OUT > /home2/amkahn/workspace/575/multilingual-sentiment/data/cine_processed_2000_neg_tagged/neg/$F.txt
done


# POS SPANISH
# Get the file paths
FILES=$(find /home2/cjaja/classwork/spring-2014/ling575/multilingual-sentiment/data/cine_processed_2000/pos -maxdepth 1 -type f)
 
# Get the number of files
NUM=$(echo "$FILES" | wc -l)
echo "Number of pos Spanish review files:" $NUM
 
# For each file:
for FILE in $FILES; do
    # Run the python script on the file
    OUT=$(./neg_tag_review.py "$FILE" es)
      
    F=$(echo $FILE | sed "s/\/home2\/cjaja\/classwork\/spring\-2014\/ling575\/multilingual\-sentiment\/data\/cine\_processed\_2000\/pos\/\([0-9]*\)\.txt/\1/")
    echo "Negation tagging pos Spanish review $F"
    echo $OUT > /home2/amkahn/workspace/575/multilingual-sentiment/data/cine_processed_2000_neg_tagged/pos/$F.txt
done
