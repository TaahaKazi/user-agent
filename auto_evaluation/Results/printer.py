"""
Read a jsonl file and print the conversation and the score of each conversation
"""

import json

with open('tod_res_ua_gpt3_vanilla_tod_gpt32024-06-05-19-43-15.jsonl', 'r') as file:
    idx = 0
    for line in file:
        entry = json.loads(line)
        #print(f"Conversation: {idx}")
        idx += 1
        print(entry['result'])

        print(f"Score: {entry['result']}")
        print("\n")

        # print the conversation
        conv_history = entry.get('conv_history', [])
        conversation_text = ''.join(
            entry['role'].strip(' ') + ': ' + entry['content'] + '\n' for entry in conv_history
            if entry['role'] in ['user_agent', 'tod_system']
        )
        print(conversation_text)
        print(entry['feedback'])
        if idx == 50:
            break
        #print(conversation_text)

    print(f"Total number of conversations: {idx}")