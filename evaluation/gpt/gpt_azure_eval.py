import os
import json
import datetime
from openai import AzureOpenAI


class gpt3_azure():

    def __init__(self, key_filepath, usage_filepath) -> None:
        openai_key = json.load(open(key_filepath))['key']

        self.client = AzureOpenAI(
            azure_endpoint = "https://uiuc-convai.openai.azure.com/", 
            api_key=openai_key,
            api_version="2024-02-15-preview"
        )

        self.log = open(usage_filepath, 'w')
        self.log.write(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'\n')

    def eval_completion(self, user_goal='', dialogue=''):
        
        goal = "You are also provided with a user goal which states the specific requirement of the user. The user goal is as following: \n" + user_goal +'\n' if user_goal else ''
        
        message_text = [{
            "role": "system",
            "content": f"Given the following dialogue:\n {dialogue}\n Evaluate whether the task is completed successfully.\n \
            {goal} Please simplify your answer by only replying with Yes or No. Nothing else."
        }]
        
        completion = self.client.chat.completions.create(
            model="gpt-35-turbo",
            messages=message_text,
            temperature=0,
            max_tokens=10,
        )
        
        response = completion.choices[0].message.content
        self.log.write(str(completion.usage)+'\n')
        return response

    def eval_naturalness(self, dialogue='', agent='user simulator'):
        
        message_text = [{
            "role": "system",
            "content": f"Given the following task oriented dialogue:\n {dialogue}\n Evaluate the speech naturalness of the user and the system. \
            In this conversation, the user or the system could either be AI or human. \
            Please only reply numeric rating from 1 to 5, where 5 represents most likely human. Your result should contains two numbers, separated by a comma. \
            For example, 3,2 would be a valid response, where the first number should be the rating of the user."
        }]
        
        completion = self.client.chat.completions.create(
            model="gpt-35-turbo",
            messages=message_text,
            temperature=0,
            max_tokens=10,
        )
        
        response = completion.choices[0].message.content
        self.log.write(str(completion.usage)+'\n')
        return response


