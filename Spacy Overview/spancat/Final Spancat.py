import string
import spacy
from spacy import displacy
nlp = spacy.load("en_core_web_md")
spancat = nlp.add_pipe("spancat")

from spacy.tokens import Doc
from spacy.training import Example

from spacy.vocab import Vocab
vocab = Vocab(strings=["Appy", "some", "sunscreen"])

def get_examples():
    predicted = Doc(vocab, words=["Apply", "some", "sunscreen"])
    token_ref = ["Apply", "some", "sun", "screen"]
    tags_ref = ["VERB", "DET", "NOUN", "NOUN"]
    example = Example.from_dict(predicted, {"words": token_ref, "tags": tags_ref})
    yield example

spancat.add_label("SPANCAT")
spancat.initialize(get_examples, nlp=nlp)

text = str(input(("text: ")))
text = text.translate(str.maketrans('', '', string.punctuation))
doc = nlp(text)

from spacy.tokens import Span
doc.spans["sc"] = [] 

# pass after removing colons 
def find_spans(doc):
    for i in range(0, len(doc)):
        for j in range(i+1, len(doc)+1):
            tdoc = nlp(doc[i:j].text)
            for ent in tdoc.ents:
                label = ent.label_                       # O(n^3) :(
                s = ent.start + i
                t = ent.end + i
                span = Span(doc, s, t, label)
                if span not in doc.spans["sc"]:
                    doc.spans["sc"].append(span)

find_spans(doc)
print(doc.spans["sc"])
displacy.serve(doc, style="span")