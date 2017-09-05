from flask import Flask, jsonify
from flask_restplus import Api, Resource, fields, reqparse
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
api = Api(app, version='1.0', title='Recommendation Engine', validate=False)

ns = api.namespace('Recommend product to shoppers')

model_input=api.model('Format : ',{"request":fields.Raw})

port = int(os.getenv('PORT', 5000))

@ns.route('/predict')  # the endpoint
class Predict(Resource):
    @api.response(200, "Success",
                  model_input)  # return a formatted response
    @api.expect(model_input)  # expect the required the input data
    def post(self):  # prefer POST
        parser = reqparse.RequestParser()  # parse the args
        parser.add_argument('request', type=dict)  # get the data
        args = parser.parse_args()
        response = {}

        try:
            inp = args['request']
            print("Input recieved : ", inp)

        except Exception as e:
            print ("Inside Exception")
            response["response"] = {}
            response["response"]["Message"] = "Failure. Check input parameters"
            response["response"]["Values"] = {"RecommendedProduct": "NoResult"}
            return jsonify(response)

        else:
            # print("Exception due to {0}".format(e))
            #
            response["response"] = {}
            response["response"]["Values"] = "DEFAULT VALUE"
            response["response"]["Message"] = "Success"
            return jsonify(response)

# run
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True) # deploy with debug=False