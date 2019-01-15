import click, json
from tools.jsonPrint import json_print
from tools.converter import Converter
from tools.currencyData import currencyData

@click.command()
@click.option('--amount', type = float, required = True, help = 'Amount of Input currency to be converted')
@click.option('--input_currency', required = True, help = 'Input currency as a 3-letter code or a currency symbol')
@click.option('--output_currency', default = 'ListAll', help = 'Output currency as a 3-letter code or a currency symbol [optional]')
def main(amount, input_currency, output_currency):
    conversion = Converter().convert_currency(amount, input_currency, output_currency)
    jsonOutput = json.dumps(conversion)
    return json_print(jsonOutput)


if __name__ == '__main__':
    main()
