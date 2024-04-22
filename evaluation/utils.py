import json
import re

def parse_txt(txt_filepath):
    convs = {}
    current_conv = None
    current_goal = ''
    conversation_text = ''

    with open(txt_filepath, 'r') as txt_file:
        for line in txt_file:
            if line.startswith('Conversation'):
                # Save the previous conversation before starting a new one
                if current_conv is not None:
                    convs[current_conv] = (current_goal.strip(), conversation_text.strip())

                # Reset variables for the new conversation
                current_conv = line.strip().split(' ')[1]
                current_goal = ''
                conversation_text = ''
            elif current_conv is not None:
                if not current_goal:
                    # The first line after 'Conversation n' is the user goal
                    current_goal = line.strip()
                else:
                    # Append the rest of the conversation text
                    conversation_text += line

        # save the last conversation
        if current_conv is not None:
            convs[current_conv] = (current_goal.strip(), conversation_text.strip())

    return convs


def parse_conv(conv):
    # Split the conversation into lines and initialize speech containers
    lines = conv.split('\n')
    user_speech = []
    tod_system_speech = []

    for line in lines:
        # Identify the speaker and strip the tags and mask
        if line.startswith('user_agent:'):
            speech = re.sub(r'\[.*?\]', '', line[12:]).strip()
            if speech != '<COMPLETE_CONVERSATION>':
                user_speech.append(speech)
        elif line.startswith('tod_system:'):
            speech = re.sub(r'\[.*?\]', '', line[12:]).strip()
            tod_system_speech.append(speech)

    # Return the concatenated speech for each agent
    return [' '.join(user_speech), ' '.join(tod_system_speech)]

def parse_conv_new(conv):
    # Split the conversation into lines and initialize speech containers
    lines = conv.split('\n')
    user_speech = []
    system_speech = []

    for line in lines:
        # Identify the speaker and strip the tags and mask
        if line.startswith('User:'):
            speech = re.sub(r'\[.*?\]', '', line[12:]).strip()
            if speech != '<COMPLETE_CONVERSATION>':
                user_speech.append(speech)
        elif line.startswith('System:'):
            speech = re.sub(r'\[.*?\]', '', line[12:]).strip()
            system_speech.append(speech)

    # Return the concatenated speech for each agent
    return [' '.join(user_speech), ' '.join(system_speech)]

def parse_abl_res(filepath):
    results = {}
    current_key = None
    mode = None
    buffer = []

    def add_to_dict():
        if current_key is not None and mode and buffer:
            # Join the buffer into a single string and strip extra newlines
            results[current_key][mode] = '\n'.join(buffer).strip()
            buffer.clear()

    with open(filepath, 'r') as file:
        for line in file:
            # print("current_key:", current_key, mode)
            # if results: print(results[0])
            line = line.strip()
            if line.isdigit():  # This is the conv_id
                if current_key is not None:
                    add_to_dict()  # Save the last section before resetting
                current_key = int(line)
                results[current_key] = {}
                mode = None
            elif line.startswith('Initial message:'):
                if mode: add_to_dict()
                mode = 'goal'
            elif line.startswith('Verbose:'):
                if mode: add_to_dict()
                mode = 'verbose'
            elif line.startswith('Vanilla:'):
                if mode: add_to_dict()
                mode = 'vanilla'
            elif line.startswith('Only Thought:'):
                if mode: add_to_dict()
                mode = 'CoT'
            elif line:
                buffer.append(line)

        # Add the last buffered section to the dictionary
        if mode: add_to_dict()
    
    '''
    for conv_id, v_results in results.items():
        print(conv_id)
        for v, result in v_results.items():
            print(v)
            print(result[:100])
    '''
    # print(results[0])

    return results

def parse_convs_txt(filepath):
    conversations = {}
    current_conv_id = None
    user_goal = None
    dialogue = []

    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('Conversation:'):
                if current_conv_id is not None:
                    # Save the previous conversation before starting a new one
                    conversations[current_conv_id] = (user_goal, '\n'.join(dialogue))
                    dialogue = []  # Reset dialogue list for the next conversation

                # Extract conversation ID and initialize the dialogue
                current_conv_id = int(line.split(':')[1].strip())
                user_goal = None
            elif line.startswith('User:') or line.startswith('System:'):
                # Collect dialogue lines
                dialogue.append(line)
            elif user_goal is None:
                # The first line after the conversation ID should be the user goal
                user_goal = line

        # Save the last conversation if the file doesn't end with a new "Conversation:" line
        if current_conv_id is not None and user_goal is not None:
            conversations[current_conv_id] = (user_goal, '\n'.join(dialogue))

    return conversations
