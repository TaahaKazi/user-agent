import re

def clean_first_line_of_conversation(conversation):
    lines = conversation.split('\n', 2)  # Split only on the first newline
    # Apply regex to remove angle brackets from the first line
    lines[1] = re.sub(r'<[^>]*>', '', lines[1])
    lines[1] = add_periods_to_sentences(lines[1])
    return '\n'.join(lines)

def add_periods_to_sentences(text):
    # Regex to find a space followed by an uppercase letter and prepend a period if needed
    processed_text = re.sub(r' ([A-Z])', r'. \1', text.strip())
    # Ensure the string ends with a period if it does not already
    if not processed_text.endswith('.'):
        processed_text += '.'
    return processed_text

def process_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read().strip()
    
    # Split conversations assuming each starts with "Conversation n:"
    conversations = content.split('\n\n')
    cleaned_conversations = [clean_first_line_of_conversation(conv) for conv in conversations]

    # Write the cleaned conversations back to the file
    with open(file_path, 'w') as file:
        file.write('\n\n'.join(cleaned_conversations))

def main():
    batch_files = ['batch1.txt', 'batch2.txt', 'batch3.txt']
    for file in batch_files:
        process_file(file)

if __name__ == '__main__':
    main()
