class Frame:
    """
    This class defines a conversational frame. It will be used to store the state of the conversation.
    """

    def __init__(self, instruct_message, conv_history):
        self.user_agent = None
        self.mode = None
        self.instruct_message = instruct_message
        self.conv_history = conv_history

    def get_initial_msg(self):
        """
        This method gets the state of the frame.
        """
        print(self.instruct_message)
        return

    def iter_conv_history(self):
        """
        This method iterates over the conversation history.
        Odd indices are system messages and even indices are user messages.
        """
        for i, msg in enumerate(self.conv_history):
            if i % 2 == 0:
                print("User: ", msg['content'])
            else:
                print("System: ", msg['content'])
        return

    def update_frame(self, response):
        self.conv_history.append(response)