import urllib.request, json 

class CurrencyConverter:
    def convert(self, amount, inputCurrency, outputCurrency = 'ListAll'):
        rates = self.fetch_rates()

        #Gets currencies' international code if symbol is provided instead
        inputCurrency = {"code": self.if_symbol_update_to_code(inputCurrency, rates)}
        outputCurrency = {"code": self.if_symbol_update_to_code(outputCurrency, rates)}

        #Returns an Error if input/output currency is not recognized
        if inputCurrency["code"] == None:
            return {"Error": "Input currency not recognized"}
        if outputCurrency["code"] == None:
            return {"Error": "Output currency not recognized"}

        outputCurrencyList = self.list_output_currencies(outputCurrency["code"], rates)
 
        jsonOutput = { "input": {}, "output": {} }
        jsonOutput["input"] = { "amount": amount, "currency": inputCurrency["code"] }
        jsonOutput["output"] = self.get_conversions(amount, inputCurrency["code"], outputCurrencyList, rates)
        return jsonOutput

    def fetch_rates(self):
        #This API returns only 32 currencies and updates once a day, however it is easy to maintain as it doesn't require an Access key
        #... and should be enough for demonstration purposes
        with urllib.request.urlopen("https://ratesapi.io/api/latest") as url:
            rates = json.loads(url.read().decode())['rates']
            rates["EUR"] = 1
            return rates


    def get_price(self, currency, rates):
        return rates[currency]


    #The symbol translation should work even if the Rates API is exchanged for the more robust one
    def if_symbol_update_to_code(self, currencyString, rates):
        #Check whether the string is already a currency code in the current rates dictionary, return it if yes
        if currencyString.upper() in rates.keys():
            return currencyString.upper()
        elif currencyString == 'ListAll':
            return currencyString
        #If not, find the symbol and return a currency code corresponding to it (provided it is in the rates dictionary)
        else:
            currencyData = self.open_currency_data()
            for currency in currencyData.values():
                if currency["symbol"].lower() == currencyString.lower() and currency["code"] in rates.keys():
                    return currency["code"]
            return None

    def open_currency_data(self):
        with open('tools/currencyData.json', encoding="utf8") as json_file:  
            return json.load(json_file)


    def list_output_currencies(self, outputCurrencyString, rates):
        if outputCurrencyString == 'ListAll':
            return list(rates.keys())
        else:
            return [ outputCurrencyString ]


    def get_conversions(self, amount, inputCurrency, outputCurrencyList, rates):
        output = {}

        inputCurrencyPrice = self.get_price(inputCurrency, rates)
        priceInEur = amount / inputCurrencyPrice

        for currency in outputCurrencyList:
            if currency != inputCurrency:
                conversion = priceInEur * self.get_price(currency, rates)
                output[currency] = self.two_decimals(conversion)
        return output

    def two_decimals(self, num):
        return int(num * 100) / 100
