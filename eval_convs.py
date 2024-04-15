import os
import sys
import json
import datetime

from evaluation.gpt.gpt_eval import gpt3
from evaluation.gpt.gpt_azure_eval import gpt3_azure
from evaluation.utils import *
from evaluation.mtld.lexical_diversity.lexical_diversity import *

if __name__ == '__main__':
    # load conversations file to be evaluated
    eval_dir = 'evluation/'
    conv_path = eval_dir + 'conv_examples.txt'
    convs = parse_txt(conv_path)

    # evaluate task completion and language naturalness using gpt
    # eval_model = gpt3()
    eval_model = gpt3_azure()

    results = {}
    
    for conv_id, (user_goal, conv) in convs.items():
        # evaluate task completion
        response_completion = eval_model.eval_completion(user_goal, conv)
        task_completion = "Yes" if 'yes' in response_completion.lower() else "No"

        # evaluate language naturalness of each agent
        naturalness_user, naturalness_llm = eval_model.eval_naturalness(conv).split(",")

        # compute the diversity score
        user_speech, tod_speech = parse_conv(conv)
        user_words = user_speech.split()
        tod_words = tod_speech.split()

        # store the results
        results[conv_id] = {
            'Task Completion': task_completion,
            'Speech naturalness of User Simulator': naturalness_user,
            'Speech naturalness of TOD System': naturalness_llm,
            'MTLD of User Simulator': mtld(user_words),
            'HD-D of User Simulator': hdd(user_words),
            'MTLD of TOD System': mtld(tod_words),
            'HD-D of TOD System': hdd(tod_words)
        }
    
    # save the results
    output_dir = "results"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.txt')

    with open(output_file, 'w') as file:
        for conv_id, result in results.items():
            file.write(f"Conversation {conv_id}\n")
            for key, value in result.items():
                file.write(f"{key}: {value}\n")
            file.write("\n")

    print(f"Results saved to {output_file}")