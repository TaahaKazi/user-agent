from extraction.utils import *
from model.pptod.pptod import PPtod
from model.openai.gpt3 import GPT3
if __name__ == '__main__':

    # Collect list of frames from multiwoz data
    DATA_PATH = 'multiwoz/data/MultiWOZ_2.1/data.json'
    REFERENCE_LIST_FILE = 'multiwoz/data/MultiWOZ_2.1/valListFile.txt'
    frames = iter_data(DATA_PATH, REFERENCE_LIST_FILE, initial_msg_flag=True, conv_hist_flag=False)

    # Initialize the TOD model
    client_model = PPtod()

    # Initialize the user-agent model
    user_model = GPT3()

    debug = True

    if debug:
        frames = frames[:1]

    # Iterate over frames
    for frame in frames:
        # Alternate between user and client model
        while True:
            # Get user model response
            user_response = user_model.get_response(frame)
            print("User: ", user_response)
            # Update frame
            frame.update_frame({"role": "user_agent", "content": user_response})

            # Get client model response
            client_response = client_model.get_response(frame)
            print("System: ", client_response)
            # Update frame
            frame.update_frame({"role": "tod_system", "content": client_response})

            # Check if the conversation is over
            if debug:
                if len(frame.conv_history) == 6:
                    break
