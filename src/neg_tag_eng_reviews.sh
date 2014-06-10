#!/bin/sh

# NEG ENGLISH
# Get the file paths
FILES=$(find /home2/cjaja/classwork/spring-2014/ling575/multilingual-sentiment/data/txt_sentoken/neg -maxdepth 1 -type f)

# Get the number of files
NUM=$(echo "$FILES" | wc -l)
echo "Number of neg English review files:" $NUM

# For each file:
for FILE in $FILES; do
    # Run the python script on the file
    OUT=$(./neg_tag_review.py "$FILE" en)
     
    F=$(echo $FILE | sed "s/\/home2\/cjaja\/classwork\/spring\-2014\/ling575\/multilingual\-sentiment\/data\/txt\_sentoken\/neg\/\(cv[_0-9]*\)\.txt/\1/")
    echo "Negation tagging neg English review $F"
    echo $OUT > /home2/amkahn/workspace/575/multilingual-sentiment/data/sentoken_neg_tagged/neg/$F.txt
done


# POS ENGLISH
# Get the file paths
FILES=$(find /home2/cjaja/classwork/spring-2014/ling575/multilingual-sentiment/data/txt_sentoken/pos -maxdepth 1 -type f)
 
# Get the number of files
NUM=$(echo "$FILES" | wc -l)
echo "Number of pos English review files:" $NUM
 
# For each file:
for FILE in $FILES; do
    # Run the python script on the file
    OUT=$(./neg_tag_review.py "$FILE" en)
      
    F=$(echo $FILE | sed "s/\/home2\/cjaja\/classwork\/spring\-2014\/ling575\/multilingual\-sentiment\/data\/txt\_sentoken\/pos\/\(cv[_0-9]*\)\.txt/\1/")
    echo "Negation tagging pos English review $F"
    echo $OUT > /home2/amkahn/workspace/575/multilingual-sentiment/data/sentoken_neg_tagged/pos/$F.txt
done