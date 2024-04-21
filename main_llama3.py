from extraction.utils import *
from model.GPT.gpt3 import GPT3
from model.GPT.llama3 import LLAMA3
import sys
import os
from utils import conv_json_to_text
import datetime
current_directory = os.getcwd()
full_path = os.path.join(current_directory, 'model')
full_path = os.path.join(full_path, 'bot')
sys.path.append(full_path)

from model.bot.tod_gpt import TODSystem


if __name__ == '__main__':
    # Collect list of frames from multiwoz data
    DATA_PATH = 'multiwoz/data/MultiWOZ_2.1/data.json'
    REFERENCE_LIST_FILE = 'multiwoz/data/MultiWOZ_2.1/valListFile.txt'
    frames = iter_data(DATA_PATH, REFERENCE_LIST_FILE, initial_msg_flag=True, conv_hist_flag=False)

    # Initialize the user-agent model
    user_model = LLAMA3()

    debug = True

    if debug:
        frames = frames[150:200]

    # Iterate over frames
    for i,frame in enumerate(frames):

        print("Frame: ", i)
        # Alternate between user and client model
        client_model = TODSystem(
            cache_dir="",
            model_name="gpt-3.5-turbo-instruct",
            faiss_db="model/bot/multiwoz-context-db.vec",
            num_examples=2,
            dials_total=100,
            database_path="model/bot/multiwoz_database",
            dataset="multiwoz",
            context_size=3,
            ontology="model/bot/ontology.json",
            output="results",
            run_name="",
            use_gt_state=False,
            use_gt_domain=False,
            use_zero_shot=False,
            verbose=True,
            goal_data=None,
            debug=False,
        )

        while True:
            # Get user model response
            try:
                user_response = user_model.get_response(frame)

                # Update frame
                frame.update_frame({"role": "user_agent", "content": user_response})

                # Check if the conversation is over
                if user_response == ' <COMPLETE_CONVERSATION>' or user_response == '<COMPLETE_CONVERSATION>':
                    break
                if user_response == ' <REPETITION>' or user_response == '<REPETITION>':
                    break
                if not user_response:
                    break
            # Get client model response
            except Exception as e:
                print(e)
                user_response = "Use my previous response"
                break
            print("User: ", user_response)

            try:
                client_response = client_model.run(frame.conv_history[-1]['content'])
                print("System: ", client_response)
                # Update frame
                frame.update_frame({"role": "tod_system", "content": client_response})
                print("\n")

            except Exception as e:
                print(e)
                client_response = "Use my previous response"
                break
            # Check if the conversation is over
            if debug:
                if len(frame.conv_history) == 30:
                    break

    print("Frames over")

    # Save the frames to a file
    output_file = 'output_store/llama3_' + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.jsonl'
    with open(output_file, 'w') as f:
        for frame in frames:
            out_dict = {"initial_message": frame.instruct_message, "conv_history": frame.conv_history}
            f.write(json.dumps(out_dict))
            f.write('\n')

    # Convert the jsonl file to a text file
    conv_json_to_text(output_file)