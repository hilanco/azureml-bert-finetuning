from transformers import BertForTokenClassification, BertTokenizerFast, BertConfig
import torch
import numpy as np

config = BertConfig.from_json_file('config.json')
model = BertForTokenClassification.from_pretrained(
    'pytorch_model.bin', config=config)
tokenizer = BertTokenizerFast.from_pretrained(".", do_lower_case=False)

tag_values = ['1-LOC', '1-MISC', '1-ORG', '1-PER', 'B-LOC', 'B-MISC', 'B-ORG', 'B-PER',
              'E-LOC', 'E-MISC', 'E-ORG', 'E-PER', 'I-LOC', 'I-MISC', 'I-ORG', 'I-PER', 'O']


def predict(sentence):

    tokenized_sentence = tokenizer.encode_plus(
        sentence, return_offsets_mapping=True)
    input_ids = torch.tensor([tokenized_sentence['input_ids']])

    with torch.no_grad():
        output = model(input_ids)

    label_indices = np.argmax(output[0].to('cpu').numpy(), axis=2)

    tokens = tokenizer.convert_ids_to_tokens(input_ids.to('cpu').numpy()[0])

    new_tokens, new_labels, offset_start, offset_end = [], [], [], []
    for token, label_idx, offset in zip(tokens, label_indices[0], tokenized_sentence['offset_mapping']):
        if token.startswith("##"):
            new_tokens[-1] = new_tokens[-1] + token[2:]
            offset_end[-1] = offset[1]
        else:
            if "CLS" in token or "SEP" in token:
                continue
            new_labels.append(tag_values[label_idx])
            new_tokens.append(token)
            offset_start.append(offset[0])
            offset_end.append(offset[1])

    return offset_start, offset_end, new_labels
