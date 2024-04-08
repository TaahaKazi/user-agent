from transformers import GPT2LMHeadModel, GPT2TokenizerFast
import torch
import numpy as np


def get_perplexity(dialogue='', model_ckpt='openai-community/gpt2-large', normalized=False):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = GPT2LMHeadModel.from_pretrained(model_ckpt).to(device)
    tokenizer = GPT2TokenizerFast.from_pretrained(model_ckpt)
    encodings = tokenizer(dialogue.strip(), return_tensors='pt')
    stride = 128
    max_length = model.config.n_positions
    seq_length = encodings.input_ids.size(1)
    
    nlls = []
    prev_end_loc = 0

    for begin_loc in range(0, seq_length, stride):
        end_loc = min(begin_loc + max_length, seq_length)
        trg_len = end_loc - prev_end_loc  # may be different from stride on last loop
        input_ids = encodings.input_ids[:, begin_loc:end_loc].to(device)
        target_ids = input_ids.clone()
        target_ids[:, :-trg_len] = -100

        with torch.no_grad():
            outputs = model(input_ids, labels=target_ids)

            # loss is calculated using CrossEntropyLoss which averages over valid labels
            # N.B. the model only calculates loss over trg_len - 1 labels, because it internally shifts the labels to the left by 1.
            neg_log_likelihood = outputs.loss

        nlls.append(neg_log_likelihood)

        prev_end_loc = end_loc
        if end_loc == seq_length:
            break

    ppl = torch.exp(torch.stack(nlls).mean()).detach().cpu().numpy()
    
    if normalized: return 1 / (1 + np.exp(-ppl))
    else: return ppl
    