class Frame:
    """
    This class defines a conversational frame. It will be used to store the state of the conversation.
    """

    def __init__(self, instruct_message, conv_history):
        self.user_agent = None
        self.mode = None
        self.instruct_message = instruct_message
        self.conv_history = conv_history
        self.verbose = None

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

        current_conv = ""
        for msg in self.conv_history:
            if msg['role'] == 'user_agent':
                msg_str = "User: " + msg['content'] + "\n"
                current_conv = current_conv + msg_str

            if msg['role'] == 'tod_system':
                msg_str = "System: " + msg['content'] + "\n" + "\n"
                current_conv = current_conv + msg_str

            if msg['role'] == 'thought':
                msg_str = "Thought: " + msg['content'] + "\n"
                current_conv = current_conv + msg_str


        print(current_conv)
        return

    def update_frame(self, response):
        self.conv_history.append(response)

    def update_verbose_frame(self, response):
        # Add the verbose response to the verbose list
        self.verbose.append(response)
        return