from openai import OpenAI
import json


class GPT3:
    def __init__(self, example=True):
        key_lookup = json.load(open('folder/user-agent/open_ai_key.json'))
        self.model = OpenAI(api_key=key_lookup['key'])
        # code to read text from a file and store it in a variable as string
        if example:
            self.example = str(open('folder/user-agent/model/openai/example.txt', 'r').read())
        else:
            self.example = ""
        self.log = open('folder/user-agent/model/openai/log.txt', 'w')

    def get_response(self, frame):

        # if the conversation history is empty, then we need to start the conversation
        if len(frame.conv_history) == 0:

            initial_msg = (
                    "You are a user chatting with a chatbot. You will be given a User Goal Instruction. You have to " \
                    "now act as if you are the user and start the conversation." + self.example + '\n\n' +
                    "Now do it for the following user goal" + "\n" + "User Goal Instruction: " +
                    "\n" + frame.instruct_message + "\n\n" + "Conversation:" + "\n" + "User: ")

            completion = self.model.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=initial_msg,
                temperature=0,
                max_tokens=30,
            )
            res = completion.choices[0].text
            res_str = res.split('\n')[0]
            return res_str

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
                    "\n" + frame.instruct_message + "\n\n" + "Conversation:" + "\n" + current_conv  +"User: ")
            completion = self.model.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=initial_msg,
                temperature=0,
                max_tokens=30,
                stop=["System:"]
            )
            res = completion.choices[0].text
            res_str = res.split('\n')[0]

            # log tokens called
            self.log.write(str(completion.usage)+ '\n')
            return res_str
