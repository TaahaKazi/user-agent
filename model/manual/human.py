class ManualUser:
    def __init__(self):
        pass

    def get_response(self, frame):
        frame.iter_conv_history()
        res_str = str(input("Enter your response: "))
        return res_str
