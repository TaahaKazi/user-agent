import json
from convframe.frame import Frame


def iter_data(data_path, reference_list_file, initial_msg_flag=True, conv_hist_flag=True):
    """
    Iterate over multiwoz data and extract the initial message and conversation history.
    """
    frames = []

    with open(data_path, 'r') as f:
        data = json.load(f)

    with open(reference_list_file, 'r') as f:
        reference_list = f.readlines()
        for reference in reference_list:
            reference = reference.strip()

            # Extract Initial Message
            initial_msg = ""
            if initial_msg_flag:
                for line in data[reference]['goal']['message']:
                    initial_msg = initial_msg + line + " "

            # Extract Conversation History
            conv_history = []
            if conv_hist_flag:
                for logs in data[reference]['log']:
                    conv_history.append(logs['text'])

            # Create Frame
            current_frame = Frame(initial_msg, conv_history)

            # Append Frame to List
            frames.append(current_frame)

    return frames
