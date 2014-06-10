cut_off = 1

executable = run_maxent.py
getenv = true
arguments = /home2/amkahn/workspace/575/multilingual-sentiment/data/sentoken_neg_tagged/ ../output/imdb_neg_trigram_$(cut_off)cutoff $(cut_off)
output = run_maxent.out
log = run_maxent.log
error = run_maxent.err
transfer_executable = false
request_memory = 1024
Queue

cut_off = 2
Queue

cut_off = 3
Queue
