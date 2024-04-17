from openai import OpenAI
import json
import regex as re


class GPT4Verbose:
    def __init__(self, example=True):
        key_lookup = json.load(open('open_ai_key.json'))
        self.model = OpenAI(api_key=key_lookup['key'])
        # code to read text from a file and store it in a variable as string
        if example:
            self.example = str(open('model/GPT/example_verbose_tracking_repitition_gpt4.txt', 'r').read())
        else:
            self.example = ""
        self.log = open('model/GPT/log.txt', 'w')

    def get_response(self, frame):

        # if the conversation history is empty, then we need to start the conversation
        if len(frame.conv_history) == 0:

            initial_msg = (
                    "You are a user chatting with a chatbot. You will be given a User Goal Instruction. You have to " \
                    "now act as if you are the user and start the conversation." + self.example + '\n\n' +
                    "Now do it for the following user goal" + "\n" + "User Goal Instruction: " +
                    "\n" + frame.instruct_message + "\n\n" + "Converting it into a dictionary:")

            try:
                completion = self.model.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[
                        {"role": "user", "content": initial_msg}
                    ],
                    temperature=0,
                    max_tokens=3000,
                    stop=["System:"]
                )

                res = completion.choices[0].message.content

                # print(res)
                # Code to extract "User: " response and Thought response
                # Define regex pattern to match User messages
                user_pattern = r'(.*)(User:\s*(.*))'

                # Find all matches of User messages in the conversation
                matches = re.findall(user_pattern, res)

                match = matches[-1]

                if match:
                    before_user = initial_msg + res.split(match[1])[0]
                    after_user = match[2]
                else:
                    print("The pattern 'User: ' was not found in the text.")
                    before_user = ""
                    after_user = ""

                # log tokens called
                self.log.write(str(completion.usage) + '\n')

            except Exception as e:

                print(e)
                before_user = "My engine failed"
                after_user = "Use my previous response"

            return before_user, after_user

        else:
            current_conv = ""
            for msg in frame.conv_history:
                if msg['role'] == 'user_agent':
                    msg_str = "User: " + msg['content'] + "\n"
                    current_conv = current_conv + msg_str

                if msg['role'] == 'tod_system':
                    msg_str = "System: " + msg['content'] + "\n" + "\n"
                    current_conv = current_conv + msg_str

                if msg['role'] == 'thought':
                    msg_str = "Thought: " + msg['content']
                    current_conv = current_conv + msg_str

            current_conv = current_conv + "Thought: "

            try:

                completion = self.model.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[
                        {"role": "user", "content": current_conv}
                    ],
                    temperature=0,
                    max_tokens=3000,
                    stop=["System:"]
                )

                res = completion.choices[0].message.content
                # Code to extract "User: " response and Thought response
                # Define regex pattern to match User messages
                user_pattern = r'(.*)(User:\s*(.*))'

                # Find all matches of User messages in the conversation
                matches = re.findall(user_pattern, res)

                match = matches[-1]

                if match:
                    before_user = res.split(match[1])[0]
                    after_user = match[2]
                else:
                    print("The pattern 'User: ' was not found in the text.")
                    before_user = ""
                    after_user = ""

                # log tokens called
                self.log.write(str(completion.usage) + '\n')

            except:
                before_user = ""
                after_user = ""
            return before_user, after_user
