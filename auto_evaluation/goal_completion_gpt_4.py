import json
import os
from openai import AzureOpenAI
import argparse

def main():


    # Constants and templates for the script
    ABS_SYSTEM_PROMPT = "You are a fair judge assistant tasked with providing clear, objective feedback based on specific criteria, ensuring each assessment reflects the absolute standards set for performance."
    ABSOLUTE_PROMPT_WO_REF = """###Task Description:
An instruction (might include an Input inside it), a response to evaluate, and a score rubric representing an evaluation criteria are given.
1. Write a detailed feedback that assess the quality of the response strictly based on the given score rubric, not evaluating in general.
2. After writing a feedback, write a score that is an integer either 0 or 1. You should refer to the score rubric.
3. The output format should look as follows: "Feedback: (write a feedback for criteria) [RESULT] (an integer either 0 or 1)"
4. Please do not generate any other opening, closing, and explanations.
    
###The instruction to evaluate:
{instruction}
    
###Response to evaluate:
{response}
    
###Score Rubrics:
{rubric}
    
###Feedback: """

    # Initialize Azure OpenAI client
    client = AzureOpenAI(
        azure_endpoint="https://uiuc-convai-sweden.openai.azure.com/",
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version="2024-02-15-preview"
    )


    def extract_and_enhance_dialogues(file_path, output_file_path, client, debug=False):
        with open(file_path, 'r') as file, open(output_file_path, 'w') as outfile:
            for line in file:
                entry = json.loads(line)
                conversation = []
                for message in entry['conv_history']:
                    if message['role'] in ['user_agent', 'tod_system']:
                        conversation.append(f"{message['role']}: {message['content']}")
                if any('user_agent' in msg for msg in conversation) and any('tod_system' in msg for msg in conversation):
                    dialogue = "\n".join(conversation)
                    rubric_data = {
                        "instruction": "Placeholder values like [name] and [destination] are allowed. Evaluate the conversation between a user-agent and a system. Has the system completed all the tasks given to it? In the Feedback section, evaluate every response of the system.",
                        "response": dialogue,
                        "rubric": "Score 0: The model did not complete all the tasks given to it. Even if it completed some tasks but not all mark it as 0\nScore 1: The model completed all the tasks given to it"
                    }
                    user_content = ABS_SYSTEM_PROMPT + "\n\n" + ABSOLUTE_PROMPT_WO_REF.format(**rubric_data)
                    messages = [{"role": "user", "content": user_content}]
                    completion = client.chat.completions.create(
                        model="UIUC-ConvAI-Sweden-GPT4-Gokhan",
                        messages=messages,
                        temperature=0,
                        max_tokens=1000,
                        frequency_penalty=0,
                        presence_penalty=0,
                        stop=None
                    )
                    feedback_text = completion.choices[0].message.content.split("[RESULT]")[0].strip()
                    print(user_content)
                    print(feedback_text)
                    result = int(completion.choices[0].message.content.split("[RESULT]")[1].strip())
                    print(result)
                    entry['feedback'] = feedback_text
                    entry['result'] = result
                    json_line = json.dumps(entry)
                    outfile.write(json_line + '\n')
                    if debug:
                        break  # Only process the first entry if debug is True

    # Input and output file paths
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file_path", type=str, help="Original JSONL file path")
    parser.add_argument("--output_file_path", type=str, help="New JSONL file with feedback and result")
    args = parser.parse_args()
    input_file_path = args.input_file_path
    output_file_path = args.output_file_path

    # Extract dialogues, enhance them with feedback, and write to a new JSONL file
    extract_and_enhance_dialogues(input_file_path, output_file_path, client, debug=False)


if __name__ == "__main__":
    main()