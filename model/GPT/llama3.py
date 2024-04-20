from openai import OpenAI
import json
import regex as re
import os
import requests
from together import Together

class LLAMA3:
    def __init__(self, example=True):
        key_lookup = json.load(open('together_ai_key.json'))
        self.model = Together(api_key=key_lookup['key'])
        # code to read text from a file and store it in a variable as string
        if example:
            self.example = str(open('model/GPT/example_repetition.txt', 'r').read())
        else:
            self.example = ""
        self.log = open('model/GPT/log.txt', 'w')

    def get_response(self, frame):

        # if the conversation history is empty, then we need to start the conversation
        if len(frame.conv_history) == 0:

            initial_msg = (
                    "You are a user chatting with a chatbot. You will be given a User Goal Instruction. You have to "\
                    "now act as if you are the user and start the conversation." + self.example + '\n\n' +
                    "Now do it for the following user goal" + "\n" + "User Goal Instruction: " +
                    "\n" + frame.instruct_message + "\n\n" + "Conversation:" + "\n" + "User: ")

            try:

                res = self.model.chat.completions.create(
                    model="meta-llama/Llama-3-70b-chat-hf",
                    # model="meta-llama/Llama-3-8b-chat-hf",
                    messages=[{"role": "user", "content": initial_msg}],
                    max_tokens=100,
                    temperature=0,
                    stop=["System: ", "assistant"]
                )
                res = res.choices[0].message.content
                res = res.split("assistant")[0]
                res_str = res
                # log tokens called

                return res_str


            except Exception as e:

                print(e)

                after_user = "Use my previous response"

                return after_user

        else:
            current_conv = ""
            for msg in frame.conv_history:
                if msg['role'] == 'user_agent':
                    msg_str = "User: " + msg['content'] + "\n"
                    current_conv = current_conv + msg_str

                if msg['role'] == 'tod_system':
                    msg_str = "System: " + msg['content'] + "\n"
                    current_conv = current_conv + msg_str

            initial_msg = (
                    "You are a user chatting with a chatbot. You will be given a User Goal Instruction. You have "
                    "to ""now act as if you are the user and continue the conversation." + self.example + '\n\n' +
                    "Now do it for the following user goal" + "\n" + "User Goal Instruction: " +
                    "\n" + frame.instruct_message + "\n\n" + "Conversation:" + "\n" + current_conv + "User: ")

            try:

                res = self.model.chat.completions.create(
                    model="meta-llama/Llama-3-70b-chat-hf",
                    # model="meta-llama/Llama-3-8b-chat-hf",
                    messages=[{"role": "user", "content": initial_msg}],
                    max_tokens=100,
                    temperature=0,
                    stop=["System: ", "assistant"]
                )
                res = res.choices[0].message.content

                res = res.split("assistant")[0]
                res_str = res

                # log tokens called
                return res_str

            except:
                before_user = ""
                after_user = ""
            return  after_user
