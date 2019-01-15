from tools.currencyData import currencyData
import urllib.request, json 

class Converter:
    def convert_currency(self, amount, inCurrencyString, outCurrencyString = 'ListAll'):
        rates = self.fetch_rates()

        #Gets currencies' international code if symbol is provided instead
        inputCurrency = {"code": self.if_symbol_update_to_code(inCurrencyString, rates)}
        outputCurrency = {"code": self.if_symbol_update_to_code(outCurrencyString, rates)}

        #Returns an Error if input/output currency is not recognized
        if inputCurrency["code"] == None:
            return {"Error": "Input currency not recognized"}
        if outputCurrency["code"] == None and outCurrencyString != 'ListAll':
            return {"Error": "Output currency not recognized"}

        #Initializing .json output 
        jsonOutput = { "input": {}, "output": {} }
        jsonOutput["input"] = { "amount": amount, "currency": inputCurrency["code"] }

        inputCurrency['price'] = self.get_price(inputCurrency, rates)

        #Runs when output currency is not specified
        if outCurrencyString == 'ListAll':
            jsonOutput["output"] = self.get_all_conversions(amount, inputCurrency, rates)
            return jsonOutput
        #Runs when output currency IS specified
        else:
            outputCurrency["price"] = self.get_price(outputCurrency, rates)

            jsonOutput["output"] = self.get_single_conversion(amount, inputCurrency, outputCurrency)
            return jsonOutput


    def fetch_rates(self):
        #This API returns only 32 currencies and updates once a day, however it is easy to maintain as it doesn't require an Access key
        #... and should be enough for demonstration purposes
        with urllib.request.urlopen("https://ratesapi.io/api/latest") as url:
            rates = json.loads(url.read().decode())['rates']
            rates["EUR"] = 1
            return rates


    def get_price(self, currency, rates):
        return rates[currency["code"]]


    #The symbol translation should work even if the Rates API is exchanged for the more robust one
    def if_symbol_update_to_code(self, currencyString, rates):
        #Check whether the string is already a currency code in the current rates dictionary, return it if yes
        if currencyString.upper() in rates.keys():
            return currencyString.upper()
        #If not, find the symbol and return a currency code corresponding to it (provided it is in the rates dictionary)
        else:
            for currency in currencyData.values():
                if currency["symbol"].lower() == currencyString.lower() and currency["code"] in rates.keys():
                    return currency["code"]
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