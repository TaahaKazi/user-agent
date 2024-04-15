import os
import json
import datetime
from openai import OpenAI

# openai.api_key = ''

class gpt3():

    def __init__(self) -> None:
        openai_key = json.load(open('open_ai_key.json'))
        self.model = OpenAI(api_key=openai_key['key'])

        self.log = open('usage_log.txt', 'w')
        self.log.write(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'\n')

    def eval_completion(self, user_goal='', dialogue=''):
        
        goal = "You are also provided with a user goal which states the specific requirement of the user. The user goal is as following: \n" + user_goal +'\n' if user_goal else ''
        
        prompt_completion = "Given the following task oriented dialogue:\n {}\n Evaluate whether the task is completed successfully.\n \
            {} Please simplify your answer by only replying with Yes or No. Nothing else.".format(dialogue, goal)
        
        completion = self.model.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt_completion,
            temperature=0,
            max_tokens=10,
        )
        
        response = completion.choices[0].text
        self.log.write(str(completion.usage)+'\n')
        return response

    def eval_naturalness(self, dialogue='', agent='user simulator'):
        
        prompt_naturalness = "Given the following task oriented dialogue:\n {}\n Evaluate the speech naturalness of the user and the system. \
            In this conversation, the user or the system could either be AI or human. \
            Please only reply numeric rating from 1 to 5, where 5 represents most likely human. Your result should contains two numbers, separated by a comma. \
            For example, 3,2 would be a valid response, where the first number should be the rating of the user.".format(dialogue)
        
        completion = self.model.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt_naturalness,
            temperature=0,
            max_tokens=10,
        )
        
        response = completion.choices[0].text
        self.log.write(str(completion.usage)+'\n')
        return response


