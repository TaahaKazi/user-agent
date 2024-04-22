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
    dir_convs = '../results/'
    vanilla_file = dir_convs + 'vanilla_50.txt'
    thought_file = dir_convs + 'thought_50.txt'
    verbose_file = dir_convs + 'verbose_50.txt'

    # evaluate task completion and language naturalness using gpt
    # eval_model = gpt3()
    key_filepath = '../azure_openai_key.json'
    usage_filepath = '../azure_openai_usage_log.txt'
    eval_model = gpt3_azure(key_filepath, usage_filepath)

    
    output_dir = "../eval_results/"
    os.makedirs(output_dir, exist_ok=True)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    all_convs = {"vanilla": vanilla_file, "thought": thought_file, "verbose": verbose_file}
    for model, results_file in all_convs.items():
        convs = parse_convs_txt(results_file)
        """ for conv_id, conv in convs.items():
            print(conv_id)
            print(conv[0][:100])
            print(conv[1][:100])
        break """
        # results file
        results = {}
        output_txt_file = os.path.join(output_dir, "eval_res_" + model + current_time + '.txt')
        output_json_file = os.path.join(output_dir, "eval_res_" + model + current_time + '.json')
        for conv_id, conv in convs.items():
            user_goal = conv[0]
            dialogue = conv[1]

            # compute the diversity score
            user_speech, tod_speech = parse_conv_new(dialogue)
            user_words = user_speech.split()
            tod_words = tod_speech.split()
            if len(user_words) < 30:
                print(conv_id, user_words)
            if len(tod_words) < 30:
                print(conv_id, tod_words)

            response = eval_model.eval_all(user_goal, dialogue)
            res_list = response.split(',')
            if len(res_list) == 6:
                task_completion, naturalness_user, naturalness_llm, coherence_user, coherence_llm, diversity_user = res_list
            else:
                task_completion, naturalness_user, naturalness_llm, coherence_user, coherence_llm, diversity_user = 0, 0, 0, 0, 0, 0
                print("Invalid response for conv ", conv_id)
                print(response)

            

            results[conv_id] = [conv_id, task_completion, naturalness_user, naturalness_llm, coherence_user, coherence_llm, diversity_user, \
                       mtld(user_words), hdd(user_words), mtld(tod_words), hdd(tod_words)]

        # store the results
        with open(output_json_file, 'w') as js_file:
            json.dump(results, js_file)
        print(f"Results saved to {output_json_file}")
        with open(output_txt_file, 'w') as txt_file:
            for conv_id, res in results.items():
                txt_file.write(f"Conversation {conv_id}\n")
                for item in res:
                    txt_file.write(f"{item} ")
                txt_file.write("\n")
        print(f"Results saved to {output_txt_file}")