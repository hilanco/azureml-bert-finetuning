from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from nltk.tokenize import sent_tokenize, word_tokenize
import ner

app = Flask(__name__)

CORS(app)


@app.route('/', methods=['POST'])
def pred():

    text = request.json['text']
    new_ents = []
    sentences = sent_tokenize(text)

    sent_len = 0
    for sent in sentences:

        starts, ends, ents = ner.predict(sent)

        for start, end, ent in zip(starts, ends, ents):
            new_ents.append(
                {'label': ent, 'start_char': sent_len + start, 'end_char': sent_len + end})

        sent_len = sent_len + len(sent)

    return jsonify(new_ents)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
