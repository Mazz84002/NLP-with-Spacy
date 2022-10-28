# Libraries Required
from flask import Flask
from flask_restful import Resource, Api
import yaml

#from flask_limiter.util import get_remote_address
#from flask_limiter import Limiter

from flasgger import Swagger # used for swagger API
from flasgger.utils import swag_from
from flask_restful_swagger import swagger #flasgger


# ------------------------------------------------------
 # Spacy Libraries

import spacy

nlp = spacy.load("en_core_web_md")

# ------------------------------------------------------
 # Importing from other files

from SPANCAT import *
from loadSpancat import *

# -----------------------------------------------------

app = Flask(__name__)
api = Api(app)

#limiter = Limiter(app, key_func=get_remote_address)
#limiter.init_app(app)

api = swagger.docs(Api(app), apiVersion='0.1', api_spec_url='/docs') # this is the swagger route


class NER(Resource):

    # Initialising swagger api
    @swagger.model
    @swagger.operation(notes='Extract entities')
    #@swag_from('./templates/config.yaml')
    # Define post request
    def post(self, text):
        doc = nlp(text)
        ent_dic = {}
        for ent in doc.ents:
            ent_dic[str(ent)] = str(ent.label_)
        return ent_dic


api.add_resource(NER, '/ent/<string:text>') # input defined in the route


class SpanCat(Resource):

    # Initialise swagger api
    @swagger.model
    @swagger.operation(notes='Extract spans')
    # Define post request
    def post(self, text):
        doc = nlp(text)
        span_dic = {}
        load_spancat(doc, nlp)
        span_lst = doc.spans["sc"]
        doc.spans["sc"], result = find_spans(doc, nlp, span_lst)
        return result


api.add_resource(SpanCat, '/span/<string:text>')  # input defined in the route

if __name__ == '__main__':
    app.run(debug=True)
