import spacy
from spacy import displacy


def ner(text):
    nlp = spacy.load("en_core_web_md")
    doc = nlp(text)
    return displacy.render(doc, style="ent")