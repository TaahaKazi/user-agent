import json
import datetime


def conv_json_to_text(output_file):
    """
    Writes the jsonl file to a text file for readability
    :param output_file: path to the jsonl file
    """

    txt_file = output_file[:6] + '.txt'
    with open(output_file, 'r') as f:
        with open(txt_file, 'a') as fa:
            lines = [json.loads(line) for line in f]
            for i, line in enumerate(lines):
                fa.write('Conversation ' + str(i + 1) + '\n')
                fa.write(line['initial_message'])
                fa.write('\n')
                for conv in line['conv_history']:
                    fa.write(conv['role'] + ': ' + conv['content'])
                    fa.write('\n')