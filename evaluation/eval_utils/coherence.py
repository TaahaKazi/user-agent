
import torch
import numpy as np
from openai import OpenAI
import json
import re

def extract_numbers(text):
    numbers = re.findall(r"[+-]?\d+(?:\.\d+)?", text)
    return [float(num) if '.' in num else int(num) for num in numbers]


def parse_dialogue(dialogue_str):
    utterances = [line.strip() for line in dialogue_str.split('\n') if line.strip()]
    
    parsed_dialogue = []
    for utterance in utterances:
        first_colon_index = utterance.find(":")
        if first_colon_index != -1:
            speaker = utterance[:first_colon_index].strip()
            content = utterance[first_colon_index + 1:].strip()
            parsed_dialogue.append([speaker, content])
    
    return parsed_dialogue


class GPT():

    def __init__(self) -> None:
        openai_key = json.load(open('open_ai_key.json'))
        self.model = OpenAI(api_key=openai_key['key'])

    def get_response(self, prompt):

        completion = self.model.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            temperature=0,
            max_tokens=10,
        )
        
        response = completion.choices[0].text
        return response
    
    

def get_coherence(dialogue='', user_goal='', llm_model=None, utterance_group=2):
    utterances = parse_dialogue(dialogue_str=dialogue)
    
    coherence_scores = []
    

    for group_id in range(0, len(utterances), utterance_group):
        utterance_group_list = utterances[group_id: group_id + utterance_group]
        
        utterance_group_string = ""
        for utterance in utterance_group_list: utterance_group_string += f"{utterance[0]}: {utterance[1]}\n"
        llm_response = llm_model.get_response(prompt=f"Given the user goal of dialogue as: {user_goal} and given the following part of dialogue:\n{utterance_group_string}\n Give a score from [1, 2, 3] to evaluate if the part of conversation is coherent in turns of addressing the overall goal while maintaining natural human-style communication. Note 3 means the metric is well satisfied while 1 means the metric far from satisfied at all.")
        
        coherence_scores.append(float(extract_numbers(text=llm_response)[0]))
        
    return float(np.mean(coherence_scores))
