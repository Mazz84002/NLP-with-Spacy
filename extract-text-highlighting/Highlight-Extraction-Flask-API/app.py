from flask import Flask, request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
from flask_restful import Resource, Api
from flask_restful_swagger import swagger

from excel_extraction import excel_extraction
from pdf_extraction import pdf_extraction

app = Flask(__name__)
app.json_encoder = LazyJSONEncoder

# ------------------------ Creating a swagger-ui template --------------------------
swagger_template = dict(
    info={
        'title': LazyString(lambda: 'Extracting Highlighted Text from files'),
        'version': LazyString(lambda: '0.1'),
        'description': LazyString(lambda: 'Highlighted Text Extraction'),
    },
    host=LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'highlights',
            "route": '/highlights.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

# ------------------------------Defining Swagger UI-------------------------------------

swagger = Swagger(app, template=swagger_template, config=swagger_config)

# ------------------------ Defining path --------------------------------------

def filetype_identifier(file):
    pass

@app.route('/highlights/', endpoint='highlights', methods=['POST'])
@swag_from("config.yaml", methods=['POST'], endpoint='highlights')
def extract_highlights():
    # define the filename and filetype
    if request.method == 'POST':
        data = request.files
        #print("Data = ")
        #print(data)
        file = data['filename']
        #print(file)
        #print(type(file))
        #print(dir(file))
        filename = str(file.filename)
        filetype = filename[len(filename)-4:len(filename)]
        if filetype == '.pdf':
            output = pdf_extraction(file)
            print(output)
            return output
        else:
            output = excel_extraction(file)
            print(output)
            return output



if __name__ == '__main__':
    app.run(debug=True)
