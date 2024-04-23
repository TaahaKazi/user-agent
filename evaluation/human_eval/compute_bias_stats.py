from process_human_eval import *
import pandas as pd
import numpy as np

def convert_numeric(value):
    if isinstance(value, str):
        value = value.strip()
        if value.lower() == 'yes':
            return 1
        elif value.lower() == 'no':
            return 0
        elif value.isdigit():
            return int(value)
        else:
            print(value)
    else:
        print(value, type(value))
    return value

def main():
    # Read human evaluation results
    eval_files = ['batch1_human_eval.txt', 'batch2_human_eval.txt', 'batch3_human_eval.txt']
    eval_data = {}
    for idx, file_name in enumerate(eval_files, start=1):
        eval_data.update({f"{idx}.{key}": value for key, value in read_human_eval(file_name).items()})
        print(file_name + " loaded")
    # print(eval_data)

    # Read mapping files
    batch_to_model = read_batch_to_model('batch_to_model.txt')
    print(batch_to_model)
    model_to_batch = read_model_to_batch('model_to_batch.txt')
    print(model_to_batch)

    data = {'vanilla': [[], [], []], 'thought': [[], [], []], 'verbose': [[], [], []]}
    stats = {'vanilla': [None, None, None], 'thought': [None, None, None], 'verbose': [None, None, None]}
    models = ['vanilla', 'thought', 'verbose']
    for model in models:
        for conv_id, batch_id in model_to_batch[model].items():
            b, bc_id = batch_id.split('.')
            converted_data = {k: convert_numeric(v) for k, v in eval_data[batch_id].items()}
            data[model][int(b)-1].append(converted_data)
        for i in range(3):
            df = pd.DataFrame(data[model][i])
            stats[model][i] = df.agg(['mean', 'std'])
            print(f"model: {model}, batch: {i+1}, number of convs: {len(data[model][i])}")
            print(stats[model][i])

    

if __name__ == '__main__':
    main()