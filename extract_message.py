from extraction.utils import *


if __name__ == '__main__':
    DATA_PATH = 'multiwoz/data/MultiWOZ_2.1/data.json'
    REFERENCE_LIST_FILE = 'multiwoz/data/MultiWOZ_2.1/valListFile.txt'
    frames = iter_data(DATA_PATH, REFERENCE_LIST_FILE)
    frames = frames[:1]
    for frame in frames:
        print(frame.instruct_message)
        print(frame.iter_conv_history())
        print()
    