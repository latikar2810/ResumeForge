import spacy

nlp = spacy.load("en_core_web_sm")

text = "Looking for a Python Developer with Flask, SQL and React experience."

doc = nlp(text)

for token in doc:
    print(token.text, token.pos_)