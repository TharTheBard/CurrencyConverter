from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from Converter.Converter import Converter
from Converter.currencyData import currencyData


app = Flask(__name__)
api = Api(app)

class ConvertCurrency(Resource):
    def get(self):
        args = request.args.to_dict()
        args['amount'] = float(args['amount'])
        if 'output_currency' not in args.keys():
            args['output_currency'] = 'ListAll'

        return jsonify(Converter().convert_currency(args['amount'], args['input_currency'], args['output_currency']))

api.add_resource(ConvertCurrency, '/currency_converter')

if __name__ == '__main__':
    app.run(debug=False)