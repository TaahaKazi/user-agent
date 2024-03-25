# print the output.jsonl file to a output txt file
import json
import datetime

# set file_name to current date and time
output_file = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.txt'

with open('output.jsonl', 'r') as f:
    with open(output_file, 'a') as fa:
        lines = [json.loads(line) for line in f]
        for i, line in enumerate(lines):
            fa.write('Conversation ' + str(i+1) + '\n')
            fa.write(line['initial_message'])
            fa.write('\n')
            for conv in line['conv_history']:
                fa.write(conv['role'] + ': ' + conv['content'])
                fa.write('\n')