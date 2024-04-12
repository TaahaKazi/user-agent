"""
Read a jsonlines file and write the contents to a new file
"""
import json

file_path_1 = 'verbose.jsonl'
file_path_2 = 'vanilla.jsonl'
file_path_3 = 'thought.jsonl'

# read the 3 jsonl files
with open(file_path_1, 'r') as f1:
    data_1 = f1.readlines()
    data_1 = [json.loads(line) for line in data_1]

with open(file_path_2, 'r') as f2:
    data_2 = f2.readlines()
    data_2 = [json.loads(line) for line in data_2]

with open(file_path_3, 'r') as f3:
    data_3 = f3.readlines()
    data_3 = [json.loads(line) for line in data_3]

# Iterate over the data and write to a new file
output_file = 'combined_output.txt'
count = 0
for data_1_s, data_2_s, data_3_s in zip(data_1, data_2, data_3):
    sample_1 = data_1_s
    sample_2 = data_2_s
    sample_3 = data_3_s

    print(count)
    print("Initial message:")
    print(sample_1['initial_message'])

    print('\n')
    print("Verbose: [CoT + UserState Grounding]")
    conv_hist_1 = sample_1['conv_history']
    for turn in conv_hist_1:
        if turn['role'] == 'user_agent':
            print(turn['role'] + ":", turn['content'])
        elif turn['role'] == 'tod_system':
            print(turn['role'] + ":", turn['content'])
    print('\n')

    print("Vanilla:")
    conv_hist_1 = sample_2['conv_history']
    for turn in conv_hist_1:
        if turn['role'] == 'user_agent':
            print(turn['role'] + ":", turn['content'])
        elif turn['role'] == 'tod_system':
            print(turn['role'] + ":", turn['content'])
    print('\n')

    print("Only Thought: [CoT]")
    conv_hist_1 = sample_3['conv_history']
    for turn in conv_hist_1:
        if turn['role'] == 'user_agent':
            print(turn['role'] + ":", turn['content'])
        elif turn['role'] == 'tod_system':
            print(turn['role'] + ":", turn['content'])
    print("\n\n")
    count += 1