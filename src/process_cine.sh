#!/bin/sh

# Get the first 10 XML file paths
FILES=$(find /home2/amkahn/workspace/575/data/corpusCine/corpusCriticasCine -maxdepth 1 -type f -name '*.xml')

# Get the number of XML files
NUM=$(echo "$FILES" | wc -l)
echo "Number of files:" $NUM

# For each XML file:
for FILE in $FILES; do
    # Run the python script on the file
    OUT=$(./process_cine.py "$FILE")
    # Change the python script output to an array
    read -a arr <<<$OUT
    # First array element is the reviewer rating
    RATING=${arr[0]}
    # Rest of array is the pre-processed review text
    TEXT="${arr[@]:1}"
    
    F=$(echo $FILE | sed "s/\/home2\/amkahn\/workspace\/575\/data\/corpusCine\/corpusCriticasCine\/\([0-9]*\)\.xml/\1/")
#    echo "Here is the full file path:"
#    echo $FILE
#    echo "Here is the stripped filename:"
    echo $F
#    echo "Here is the rating:"
#    echo $RATING
#    echo "Here is the text:"
#    echo $TEXT

    # Write the review text to a TXT file in the appropriate pos/neg folder based on rating
    if [ "$RATING" = "1" ] || [ "$RATING" = "2" ]; then
#        echo "This is a negative review; writing to file in negative directory"
        echo $TEXT > /home2/amkahn/workspace/575/data/cine_processed/neg/$F.txt
    elif [ "$RATING" = "4" ] || [ "$RATING" = "5" ]; then
#        echo "This is a positive review; writing to file in positive directory"
        echo $TEXT > /home2/amkahn/workspace/575/data/cine_processed/pos/$F.txt
#    else
#        echo "This is a neutral review; throwing it out"  
    fi

done