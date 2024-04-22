import json
import re

def read_human_eval(filename):
    eval_data = {}
    with open(filename, 'r') as file:
        current_conv_id = None
        for line in file:
            line = line.split('#')[0].strip()  # Ignore comments
            if line.startswith('Conversation:'):
                current_conv_id = int(line.split(':')[1].strip())
                eval_data[current_conv_id] = {}
            elif current_conv_id is not None and line:
                if ':' in line:
                    key, value = line.split(':')
                    value = value.strip().replace('2a', '2').replace('2b', '2')
                    eval_data[current_conv_id][key.strip()] = value
                else:
                    print(filename, current_conv_id)
    return eval_data

def read_model_to_batch(filename):
    mapping = {}
    with open(filename, 'r') as file:
        for line in file:
            if '->' in line:
                key, value = line.split('->')
                mapping[int(key.strip())] = value.strip()
    return mapping

def read_batch_to_model(filename):
    mapping = {}
    with open(filename, 'r') as file:
        for line in file:
            if ':' in line:
                batch_conv_id, model_info = line.strip().split(':')
                mapping[batch_conv_id.strip()] = model_info.strip()
    return mapping

def main():
    # Read human evaluation results
    eval_files = ['batch1_human_eval.txt', 'batch2_human_eval.txt', 'batch3_human_eval.txt']
    eval_data = {}
    for idx, file_name in enumerate(eval_files, start=1):
        eval_data.update({f"{idx}.{key}": value for key, value in read_human_eval(file_name).items()})
        print(file_name + " loaded")

    # Read mapping files
    batch_to_model = read_batch_to_model('batch_to_model.txt')
    print(batch_to_model)

    # Map evaluation results back to models and original conversation IDs
    results = {}
    for batch_conv_id, evals in eval_data.items():
        if batch_conv_id in batch_to_model:
            model_info = batch_to_model[batch_conv_id]
            model, conv_id = model_info.split('-')
            conv_id = int(conv_id)
            if model not in results:
                results[model] = {}
            results[model][conv_id] = evals

    # Save results to JSON file
    with open('human_eval_results.json', 'w') as json_file:
        json.dump(results, json_file, indent=4)

    # Save results to TXT file
    with open('human_eval_results.txt', 'w') as txt_file:
        for model, convs in results.items():
            txt_file.write(f'Model: {model}\n')
            for conv_id in sorted(convs.keys()):
                txt_file.write(f'Conversation {conv_id}:\n')
                for key, value in evals.items():
                    txt_file.write(f'  {key}: {value}\n')
                txt_file.write('\n')

if __name__ == '__main__':
    main()
