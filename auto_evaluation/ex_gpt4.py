import argparse
import json
import re
import os
from openai import AzureOpenAI
import ast
from tqdm import tqdm
import time

def extract_and_check_emphasis_texts(file_path, output_file):
    # Initialize a list to store results
    results = []

    client = AzureOpenAI(
        azure_endpoint="https://uiuc-convai-sweden.openai.azure.com/",
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version="2024-02-15-preview",
    )
    # Count the number of lines to set up the tqdm progress bar
    with open(file_path, 'r') as file:
        total_lines = sum(1 for _ in file)

    # Read the file and process each line with progress tracking


    # Read the file and process each line
    with open(file_path, 'r') as file:
        for line in tqdm(file, total=total_lines, desc="Processing lines", unit="line"):
            # Parse each line as a JSON object
            data = json.loads(line)

            # Extract the initial_message field
            initial_message = data.get('initial_message', '')

            # Find text within <span class='emphasis'> </span>
            emphasis_pattern = re.compile(r"<span class='emphasis'>(.*?)</span>")
            matches = emphasis_pattern.findall(initial_message)

            # If matches are found, process the conversation
            if matches:
                # Extract conversation history
                conv_history = data.get('conv_history', [])

                # Combine all relevant messages in the conversation with roles 'user_agent' and 'tod_system'
                conversation_text = ''.join(
                    entry['role'].strip(' ') + ': ' + entry['content'] + '\n' for entry in conv_history
                    if entry['role'] in ['user_agent', 'tod_system']
                )

                # Reading extractor.txt file into a string
                with open('extractor.txt', 'r') as file_r:
                    extractor = file_r.read()
                    prompt = extractor.format(list_user=str(matches), conversation=conversation_text)
                    message_text = [
                        {"role": "user", "content": prompt}]

                    try:
                        start_time = time.time()  # Start timing the API call
                        completion = client.chat.completions.create(
                            model="UIUC-ConvAI-Sweden-GPT4-Gokhan",
                            messages=message_text,
                            temperature=0,
                            max_tokens=1000,
                            seed=0,
                            stop=None
                        )
                        response = completion.choices[0].message.content
                        end_time = time.time()  # End timing the API call
                        api_call_duration = end_time - start_time
                        print(f"API call duration: {api_call_duration:.2f} seconds")


                        # Split the response into two parts:
                        # 1. The part before "Based on this the final check_list should be:"
                        # 2. The part after "Based on this the final check_list should be:"
                        try:
                            split_response = response.split("Based on this the final check_list should be:")
                            if len(split_response) > 1:
                                reasoning = split_response[0]
                                result = split_response[1].strip('\n')
                            else:
                                conversation_text = response
                                reasoning = ["NaN"]
                                result = [0]
                        except:
                            conversation_text = response
                            reasoning = ["NaN"]
                            result = [0]
                        #print(reasoning)
                        #print(result)

                        # result is a string list of the form [1,1,0]
                        # convert it to a list of integers
                        try:
                            result_list = ast.literal_eval(result)
                        except:
                            result_list = [0]
                        # result_list = [int(i) for i in result.split(",")]

                        # scoring result_list percentage
                        score = sum(result_list) / len(result_list)
                        print(score)

                        # Count how many matches are found in the conversation
                        match_count = {match: conversation_text.count(match) for match in matches}
                        # Store the result into an output json file
                        with open(output_file, 'a') as file_w:
                            result_dict = {
                                "initial_message": initial_message,
                                "matches": matches,
                                "match_count_in_conversation": result_list,
                                "conversation_text": conversation_text,
                                "reasoning": reasoning,
                                "result": result,
                                "score": score
                            }
                            file_w.write(json.dumps(result_dict))
                            file_w.write('\n')
                            print("File written")
                    except Exception as e:
                        with open(output_file, 'a') as file_w:
                            result_dict = {
                                "initial_message": initial_message,
                                "matches": "NA",
                                "match_count_in_conversation": "NA",
                                "conversation_text": "NA",
                                "reasoning": "NA",
                                "result": "NA",
                                "score": "NA"
                            }
                            file_w.write(json.dumps(result_dict))
                            file_w.write('\n')
                            print("File written")

if __name__ == "__main__":
    # Set up argparse to handle command-line arguments
    parser = argparse.ArgumentParser(description='Extract and process emphasis texts from a JSONL file.')
    parser.add_argument('file_path', type=str, help='The path to the input JSONL file.')
    parser.add_argument('output_file', type=str, help='The path to the output JSON file.')

    # Parse the arguments
    args = parser.parse_args()

    # Extract the emphasis texts and check their occurrences in conversation
    extract_and_check_emphasis_texts(args.file_path, args.output_file)
