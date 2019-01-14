from Converter.currencyData import currencyData
import urllib.request, json 

class Converter:
    def convert_currency(self, amount, inCurrency, outCurrency = 'ListAll'):
        rates = self.fetch_rates()

        #Gets currencies' international code if symbol is provided instead
        inputCurrency = {"code": self.if_symbol_update_to_code(inCurrency, rates)}
        outputCurrency = {"code": self.if_symbol_update_to_code(outCurrency, rates)}

        #Returns an Error if input/output currency is not recognized
        if inputCurrency["code"] == None:
            return {"Error": "Input currency not recognized"}
        if outputCurrency["code"] == None and outCurrency != 'ListAll':
            return {"Error": "Output currency not recognized"}

        #Initializing .json output 
        jsonOutput = {"input": {}, "output": {}}
        jsonOutput["input"]["amount"] = amount
        jsonOutput["input"]["currency"] = self.if_symbol_update_to_code(inCurrency, rates)


        inputCurrency['price'] = self.get_price(inputCurrency, rates)

        #Runs when output currency is not specified
        if outCurrency == 'ListAll':
            jsonOutput["output"] = self.get_all_conversions(amount, inputCurrency, rates)
            return jsonOutput
        #Runs when output currency IS specified
        else:
            outputCurrency["price"] = self.get_price(outputCurrency, rates)

            jsonOutput["output"] = self.get_single_conversion(amount, inputCurrency, outputCurrency)
            return jsonOutput


    def fetch_rates(self):
        with urllib.request.urlopen("https://ratesapi.io/api/latest") as url:
            rates = json.loads(url.read().decode())['rates']
            rates["EUR"] = 1
            return rates

    def get_price(self, currency, rates):
        return rates[currency["code"]]

    def if_symbol_update_to_code(self, currency, rates):
        if currency.upper() in rates.keys():
            return currency.upper()
        else:
            for key in currencyData:
                if currencyData[key]["symbol"].lower() == currency.lower():
                    return currencyData[key]["code"]
            return None

    def get_single_conversion(self, amount, inputCurrency, outputCurrency):
        output = {}
        priceInEur = amount / inputCurrency['price']
        conversion = self.two_decimals(priceInEur * outputCurrency["price"])
        output[outputCurrency["code"]] = conversion
        return output

    def get_all_conversions(self, amount, inputCurrency, rates):
        output = {}
        priceInEur = amount / inputCurrency['price']
        for code in rates:
            output[code] = self.two_decimals(priceInEur * rates[code])
        return output

    def two_decimals(self, num):
        return int(num * 100) / 100