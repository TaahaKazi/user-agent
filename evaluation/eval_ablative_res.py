import os
import sys
import json
import datetime

from gpt.gpt_eval import gpt3
from gpt.gpt_azure_eval import gpt3_azure
from utils import *
from mtld.lexical_diversity.lexical_diversity import *

if __name__ == '__main__':
    # load conversations file to be evaluated
    conv_dir = '../ablative_res/'
    conv_path = conv_dir + 'ablative.txt'
    abl_res = parse_abl_res(conv_path)

    # evaluate task completion and language naturalness using gpt
    # eval_model = gpt3()
    key_filepath = '../azure_openai_key.json'
    usage_filepath = '../azure_openai_usage_log.txt'
    eval_model = gpt3_azure(key_filepath, usage_filepath)

    results = {}
    
    for conv_id, convs in abl_res.items():
        user_goal = convs["goal"]
        variants = ["verbose", "vanilla", "CoT"]
        results[conv_id] = {}
        for v in variants:
            # evaluate task completion
            response_completion = eval_model.eval_completion(user_goal, convs[v])
            task_completion = "Yes" if 'yes' in response_completion.lower() else "No"
            # print(v, convs[v])

            # evaluate language naturalness of each agent
            naturalness_user, naturalness_llm = eval_model.eval_naturalness(convs[v]).split(",")

            # task_completion, naturalness_user, naturalness_llm = 1, 1, 1

            # compute the diversity score
            user_speech, tod_speech = parse_conv(convs[v])
            user_words = user_speech.split()
            tod_words = tod_speech.split()

            # store the results
            results[conv_id][v] = {
                'Task Completion': task_completion,
                'Speech naturalness of User Simulator': naturalness_user,
                'Speech naturalness of TOD System': naturalness_llm,
                'MTLD of User Simulator': mtld(user_words),
                'HD-D of User Simulator': hdd(user_words),
                'MTLD of TOD System': mtld(tod_words),
                'HD-D of TOD System': hdd(tod_words)
            }
    
    # save the results
    output_dir = "../eval_results"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "abl_res" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.txt')

    with open(output_file, 'w') as file:
        for conv_id, v_results in results.items():
            file.write(f"Conversation {conv_id}\n")
            for mode, result in v_results.items():
                file.write(f"{mode}:\n")
                for key, value in result.items():
                    file.write(f"{key}: {value}\n")
            file.write("\n")

    print(f"Results saved to {output_file}")