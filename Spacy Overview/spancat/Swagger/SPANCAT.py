def find_spans(doc, nlp, span_lst):
    m = 0
    span_lst = []
    #print(span_lst)
    import spacy
    from spacy import displacy
    from spacy.tokens import Span

    i = 0

    for i in range(0, len(doc)):
        j = i + 1
        for j in range(i + 1, len(doc) + 1):
            tdoc = nlp(doc[i:j].text)
            for ent in tdoc.ents:
                label = ent.label_
                s = ent.start + i
                t = ent.end + i
                span = Span(doc, s, t, label)
                if span not in span_lst:
                    span_lst.append(span)
    #print("span_lst = ", span_lst)
    span_dic = {}
    for span in span_lst:
        span_dic[str(span)] = str(span.label_)
    return span_lst, span_dic

