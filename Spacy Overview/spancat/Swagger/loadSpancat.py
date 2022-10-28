def load_spancat(doc, nlp):
    if "spancat" not in nlp.pipe_names:
        import spacy
        from spacy.tokens import Span
        doc.spans["sc"] = []
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

    #return nlp, doc.spans["sc"]