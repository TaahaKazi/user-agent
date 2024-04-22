import os
import json
import datetime
from openai import AzureOpenAI


class gpt3_azure():

    def __init__(self, key_filepath, usage_filepath, output_store_dir="../output_store/") -> None:
        openai_key = json.load(open(key_filepath))['key']

        self.client = AzureOpenAI(
            azure_endpoint = "https://uiuc-convai.openai.azure.com/", 
            api_key=openai_key,
            api_version="2024-02-15-preview"
        )

        self.log = open(usage_filepath, 'a')
        current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.log.write(current_time+'\n')
        self.output_store = open(output_store_dir + current_time + '.txt', 'w')

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

    def eval_all(self, user_goal, dialogue):
        message_text = [{
            "role": "system",
            "content": f"""You are required to evaluate a task oriented dialogue on several metrics, \
            including task completion, naturalness, coherence and dialogue-level diversity.\n \
            Alongside the dialogue, you are also provided with a user goal which states the specific requirement of the user. \
            Notice that in the user goal, you may encounter formats like <span class='emphasis'> xxx </span>, where xxx represent needs or intentions from the user.
            Here is some detailed explanations for the metrics: \
            1. Task completion \n\
            You should check whether each intention in the user goal is fulfilled in the conversation. The task is completed ONLY if all the intentions are fulfilled. \
            This would be a binary metric and you should only response with Yes or No. \
            2. Naturalness \n\
            This metric measures the resemblance to human. \
            In the dialogue, the user or the system could either be AI or human. \
            You should report a numeric rating from 1 to 5, where 5 represents most likely to be human. \
            You are required to evaluate the naturalness of both the user and the system. \
            Here is some more detailed guidelines of naturalness for your reference: \n\
            1: The speaker continuously repeat itself, typical robotic behavior. Or the speech is hard to understand.
            2: The speaker repeat itself occasionally, the vocabulary is limited, like a robot.
            3: The speaker does not have repeated behaviors (unless for verifying information). Vocabulary is enough to communicate effectively, speech is easy to understand. But I am confident that human rarely speak like this.
            4: The speaker is likely to be a human. There is rarely logical inconsistency. But from some details I feel like the utterance is a bit weird and somewhat resembles AI.
            5: Can not really tell if this is AI or human. Human could probably say the same thing in real life. \n\
            3. Coherence \n \
            This metric measures the logical consistency within a dialogue. \
            You should report a numeric rating from 1 to 3, where 3 represents the best coherence. \
            Here is some detailed guidelines for coherence. \n \
            a. Locally, the utterances are coherent/logical based on previous turns of conversations. \n \
            b. Globally, the utterances reasonably and logically adhere to achieving the initial user goal step by step. \n \
            If both conditions a and b are satisfied, you should give a score of 3. If only one condition is satisfied, you should give a score of 2. Report 1 if none of the conditions are satisfied. \n \
            4. Dialogue-level diversity \n \
            In addition to trying to achieve the initial goal, does the user introduce some reasonable deviations from the normal conversation flow?
            Give a score from:
            3 (highest score): > 20% of the time (frequently deviate from normal flow of the conversation)
            2: 0% < deviation frequency < 20% (Normal)
            1 (lowest score): ~ 0% (too artificial, maximizing information exchange) \n \
            Note that for naturalness and coherence, you need to evaluate both the user and the system. For dialogue-level diversity, you only need to evaluate the user. \n \
            You should return 6 results in total, with the order of task completion, naturalness for the user, natualness for the system, coherence for the user, coherence for the system, diversity for the user. \
            Each evaluation results should be separated by commas. For example, 'Yes,5,3,3,1,2' will be a valid response.
            Please be strict on the format of your response. Do not include any other words like 'Sure!', 'Here is the result:'. Simply response with only the results. \n \
            The user goal is as following:\n {user_goal}\n \
            The dialogue to be evaluated is as following:\n {dialogue}\n"""
        }]
        completion = self.client.chat.completions.create(
            model="gpt-35-turbo",
            messages=message_text,
            temperature=0,
            max_tokens=100,
        )
        
        response = completion.choices[0].message.content
        self.log.write(str(completion.usage)+'\n')
        self.output_store.write(str(completion)+'\n')

        return response
