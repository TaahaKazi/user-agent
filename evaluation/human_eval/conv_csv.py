import csv

# read a csv file
with open(file='Human_Eval_Batch_3.csv', mode='r') as file:
    data = file.read()

# Read the data using csv.reader
reader = csv.reader(data.strip().split('\n'))

# Skipping the first two lines which are headers
next(reader)
next(reader)

# Process each line
for line in reader:
    idx = line[0]
    task_completion = line[2]
    naturalness_user = line[5]
    naturalness_tod = line[6]
    coherence_user = line[3]
    coherence_tod = line[4]
    dialogue_diversity = line[7]

    print(f"Conversation: {idx}")
    print(f"Task Completion: {task_completion}")
    print(f"Naturalness for user simulator: {naturalness_user}")
    print(f"Naturalness for TOD system: {naturalness_tod}")
    print(f"Coherence for user simulator: {coherence_user}")
    print(f"Coherence for TOD system: {coherence_tod}")
    print(f"Dialogue-level diversity for user simulator: {dialogue_diversity}")
    print()