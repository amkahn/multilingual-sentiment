#!/bin/sh

# Get the first 10 XML file paths
FILES=$(find /home2/amkahn/workspace/575/data/corpusCine/corpusCriticasCine -maxdepth 1 -type f -name '*.xml' | head -10)

# Get the number of XML files
# echo "$FILES" | wc -l

# For each XML file
for f in $FILES; do
    # Run the python script on the file
    OUT=$(./process_cine.py "$f")
    # Change the python script output to an array
    read -a arr <<<$OUT
    # First array element is the reviewer rating
    RATING=${arr[0]}
    # Rest of array is the pre-processed review text
#    TEXT=$arr{@:2}
    echo "Here is the rating:"
    echo $RATING
    echo "Here is the text:"
#    echo $TEXT
done