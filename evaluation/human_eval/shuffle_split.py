import random

def read_conversations(file_path):
    conversations = []
    with open(file_path, 'r') as file:
        # Skip the "Conversation n:" line and trim any trailing newlines/spaces
        conversation_blocks = file.read().strip().split('\n\n')
    # print(len(conversation_blocks))
    for block in conversation_blocks:
        lines = block.strip().split('\n')
        conv_id_line = lines[0]
        # print(conv_id_line)
        if conv_id_line.startswith("Conversation:"):
            conversations.append('\n'.join(lines[1:]))  # Exclude the first line
    return conversations

def write_conversations(conversations, file_path):
    with open(file_path, 'w') as file:
        for i, conv in enumerate(conversations, 1):
            file.write(f"Conversation {i}:\n{conv}\n\n")

def main():
    dir_original_convs = "../../results/"
    vanilla_file = dir_original_convs + 'vanilla_50.txt'
    thought_file = dir_original_convs + 'thought_50.txt'
    verbose_file = dir_original_convs + 'verbose_50.txt'
    vanilla = read_conversations(vanilla_file)
    thought = read_conversations(thought_file)
    verbose = read_conversations(verbose_file)
    # print(len(vanilla))
    # print(vanilla[:5])

    # Combine all conversations into one list with tags
    combined = [(conv, 'vanilla', i) for i, conv in enumerate(vanilla)] + \
               [(conv, 'thought', i) for i, conv in enumerate(thought)] + \
               [(conv, 'verbose', i) for i, conv in enumerate(verbose)]

    # print(combined[:2])
    random.shuffle(combined)

    # Divide shuffled list into three batches
    batch1, batch2, batch3 = combined[:50], combined[50:100], combined[100:]

    # Write batches to files
    dir_processed = "./"
    write_conversations([c[0] for c in batch1], dir_processed + 'batch1.txt')
    write_conversations([c[0] for c in batch2], dir_processed + 'batch2.txt')
    write_conversations([c[0] for c in batch3], dir_processed + 'batch3.txt')

    # Save indices files
    batches = [batch1, batch2, batch3]
    model_to_batch = {'vanilla': [], 'thought': [], 'verbose': []}

    for i, batch in enumerate(batches):
        for j, (conv, model, orig_idx) in enumerate(batch):
            index_key = f"{i+1}.{j+1}"
            model_to_batch[model].append((orig_idx, index_key))
    # print(model_to_batch)
    
    with open('batch_to_model.txt', 'w') as btm, open('model_to_batch.txt', 'w') as mtb:

        for i, batch in enumerate(batches):
            for j, (conv, model, orig_idx) in enumerate(batch):
                btm.write(f"{i+1}.{j+1}: {model}-{orig_idx}\n")
        
        for model, indices in model_to_batch.items():
            # print(indices)
            indices.sort()
            mtb.write(f"{model}:\n")
            for orig_idx, batch_index in indices:
                mtb.write(f"{orig_idx}->{batch_index}\n")

if __name__ == '__main__':
    main()
