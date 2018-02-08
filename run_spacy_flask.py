#!/usr/bin/python3
import json

import spacy
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class NLPToolkit:
    nlp = None

    def __init__(self, lang="en"):
        self.nlp = spacy.load(lang)

    def process(self, text):
        return self.nlp(u"%s" % text)

    def tokenize_text(self, text):
        found_tokens = []
        tokens = self.process(text)
        for token in tokens:
            found_tokens.append(
                {
                    "text": token.text, # Original word text
                    "lemma": token.lemma_, # The Lemmatized text
                    "pos": token.pos_, # Simple part-of-speech tag
                    "tag": token.tag_, # Detailed part-of-speech tag
                    "dep": token.dep_, # Syntactic dependency, i.e.: relation between tokens
                    "shape": token.shape_, # Word shape
                    "alpha": token.is_alpha, # Is a alpha character
                    "stop": token.is_stop, # Is a stopword
                    "head_text": token.head.text if token.head else None, # The head text
                    "head_pos": token.head.pos_ if token.head else None, # The head part-of-speech tag
                    #"childs": [child for child in token.children] # Dependants
                }
            )
        return found_tokens

nlp_es = NLPToolkit('es')
nlp_en = NLPToolkit('en')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/en')
def home_en():
    words = request.args.get('text', default=None)
    tokens = nlp_en.tokenize_text(words)
    return render_template('search.html', language="en", text=words, tokens=tokens)

@app.route('/es')
def home_es_json():
    words = request.args.get('text', default=None)
    tokens = nlp_es.tokenize_text(words)
    return render_template('search.html', language="es", text=words, tokens=tokens)

@app.route('/json/en')
def home_en_json():
    words = request.args.get('text', default=None)
    tokens = nlp_en.tokenize_text(words)
    return jsonify(tokens)

@app.route('/json/es')
def home_es():
    words = request.args.get('text', default=None)
    tokens = nlp_es.tokenize_text(words)
    return jsonify(tokens)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=3000,
        debug=True
    )