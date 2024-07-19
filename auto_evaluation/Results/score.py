"""
Read a json file
Read the score of each conversation
Add the score from each conversation
Print the total score
Also print the total number of conversations
"""

import json

with open('tod_res_ua_gpt3_verbose_tod_gpt42024-06-25-14-13-17.jsonl', 'r') as file:
    idx = 0
    total_score = 0
    for line in file:
        entry = json.loads(line)
        print(f"Conversation {idx}")
        idx += 1
        print(entry['result'])
        print("\n")
        total_score += entry['result']
    print(f"Total score: {total_score}")
    print(f"Total number of conversations: {idx}")