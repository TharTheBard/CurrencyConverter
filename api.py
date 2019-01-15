from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from tools.converter import Converter
from tools.currencyData import currencyData


app = Flask(__name__)
api = Api(app)

class ConvertCurrency(Resource):
    def get(self):
        args = request.args.to_dict()

        try:
            args['amount'] = float(args['amount'])
        except ValueError:
            return jsonify({"Error": "Amount is not a number!"})

        if 'output_currency' not in args.keys():
            args['output_currency'] = 'ListAll'

        conversion = Converter().convert_currency(args['amount'], args['input_currency'], args['output_currency'])
        return jsonify(conversion)

api.add_resource(ConvertCurrency, '/currency_converter')

if __name__ == '__main__':
    app.run(debug=False)