import json

def process_jsonl_file(file_path):
    total_score = 0
    count = 0
    with open(file_path, 'r') as file:
        idx = 0
        for line in file:

            data = json.loads(line.strip())

            conversation_text = data.get('conversation_text', 'No conversation text provided.')
            score = data.get('score', 'No score provided.')
            reasoning = data.get('reasoning', 'No reasoning provided.')
            initial_message = data.get('initial_message', 'No initial message provided.')

            print(f"Conversation {idx}")
            idx += 1

            print("Initial Message:")
            print(initial_message)
            print("Conversation:")
            print(conversation_text)
            print("\nScore:")
            print(score)
            if score != 'NA':
                total_score += float(score)
                count += 1
            print("\nReasoning:")
            print(reasoning)
            print("\n" + "="*50 + "\n")

    print(f"Total score: {total_score}")
    print(f"Total number of conversations: {count}")

# Replace 'sample.jsonl' with the path to your JSONL file
file_path = 'ua_gpt3_verbose_tod_gpt32024-06-05-22-12-03_res.jsonl'
process_jsonl_file(file_path)

