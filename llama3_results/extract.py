"""
Read a jsonlines file and write the contents to a new file
"""
import json

# file_path_1 = '50_vanilla_output_2024-04-17-18-56-08.jsonl'     # UA_35_TOD_35.txt
# file_path_1 = 'llama3_llama32024-04-20-17-15-20.jsonl'    # UA_llama3_70b_llama3_70b.txt
# file_path_1 = 'llama3_2024-04-20-16-04-30.jsonl'    # UA_llama3_TOD_35.txt
file_path_1 = 'gpt3_llama32024-04-20-18-10-42.jsonl'    # UA_35_TOD_llama3_70b.txt

# read the 3 jsonl files
with open(file_path_1, 'r') as f1:
    data_1 = f1.readlines()
    data_1 = [json.loads(line) for line in data_1]

for i, data in enumerate(data_1):
    print("Conversation: ", i)
    print(data['initial_message'])
    for conv in data['conv_history']:
        if conv['role'] == 'user_agent':
            print("User:", conv['content'])
        if conv['role'] == 'tod_system':
            print("System:", conv['content'])
    print("\n")