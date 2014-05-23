#!/bin/sh
# code mostly taken from Stack Overflow
# http://stackoverflow.com/questions/414164/how-can-i-select-random-files-from-a-directory-in-bash
# commented by me (Claire Jaja) 5/22/2014

# get 1000 random files
N=1000

# array of all files in directory passed as first argument
a=( $1/* )

# an array to hold them
randf=()

# loop up to N
for((i=0;i<N && ${#a[@]};++i))
do
    # pick random file
    ((j=RANDOM%${#a[@]}))
    # add to array of random files
    randf+=( "${a[j]}" )
    # remove from array of all files
    a=( "${a[@]:0:j}" "${a[@]:j+1}" )
done

# copy random files to directory given in second argument
for i in "${randf[@]}"
do
    cp $i $2
done

