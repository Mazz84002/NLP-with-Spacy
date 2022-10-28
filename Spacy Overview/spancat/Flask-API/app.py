from flask import Flask, redirect, url_for, render_template, request
import spacy
from spacy import displacy
from loadSpancat import *
from SPANCAT import *

from flaskext.markdown import Markdown


nlp = spacy.load("en_core_web_md")
app = Flask(__name__)
Markdown(app) # pass app around markdown

# needs a global initiator
result = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        result = []
        # Defining doc
        text = request.form["text"]
        print(text)
        doc = nlp(text)

        # Extracting NER
        result.append(displacy.render(doc, style="ent"))

        # Extracting SPANCAT
        load_spancat(doc, nlp)
        print("pipes = ", nlp.pipe_names)
        span_lst = doc.spans["sc"]
        doc.spans["sc"] = find_spans(doc, nlp, span_lst)
        result.append(displacy.render(doc, style="span"))

        #if request.form["submit_button"] == "Extract Entities": # Grey out this if block (and shift-tab content for Postman)
        return render_template("results.html", NER=result[0], SPANCAT=result[1])

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)

