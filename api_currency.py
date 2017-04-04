import osa
import glob
import os.path
import codecs

def processing_files(file):
    with codecs.open(file,'r','utf-8') as original_file:
        file_content = original_file.readlines()
        return file_content

def average_temp(file_content,url):
    average_temp_sum = 0
    client = osa.client.Client(url)
    for temp_value in file_content:
        average_temp_sum += client.service.ConvertTemp(Temperature=temp_value[0:2], FromUnit='degreeFahrenheit', ToUnit='degreeCelsius')
    average_temp_sum = round((average_temp_sum / 7),2)
    return average_temp_sum


def get_distanse_km(file_content,url):
    destination_sum = 0
    client = osa.client.Client(url)
    for current_record in file_content:
        for value in current_record.split(": "):
            if value.find("-") == -1:
                measure_amount = value[:value.find(" ")]
                destination_sum += client.service.ChangeLengthUnit(LengthValue = measure_amount.replace(",",""),fromLengthUnit = 'Miles', toLengthUnit = 'Kilometers')
    return destination_sum

def get_currency_prices(file_content,url):
    price_tickets_sum = 0
    client = osa.client.Client(url)
    response = client.service.Currencies()
    for currency_record in file_content:
        for value in currency_record.split(": "):
            if value.find("-") == -1:
             from_currency = value[value.find(" ")+1:]
             amount_value =  value[:value.find(" ")]
             from_currency = (from_currency.strip("\n\r")).strip(" ")
             price_tickets_sum += client.service.ConvertToNum(toCurrency='RUB', fromCurrency=from_currency, amount=amount_value, rounding = True)
    return round(price_tickets_sum,0)

def retrieve_files(pattern):
    files = glob.glob(os.path.join('', pattern))
    return files

def main():
    files = retrieve_files('*txt')
    for file in files:
     file_content = processing_files(file)
     if file == 'temps.txt':
      url = 'http://www.webservicex.net/ConvertTemperature.asmx?WSDL'
      average_temp_seven_days = average_temp(file_content, url)
      print('Cреднее арифметическое температуры за неделю по Цельсию - ', average_temp_seven_days)
     elif file == 'currencies.txt':
      url = 'http://fx.currencysystem.com/webservices/CurrencyServer4.asmx?WSDL'
      price_tickets_sum = get_currency_prices(file_content,url)
      print('Мы потратим на поездку: ',price_tickets_sum, ' рублей')
     else:
       url = 'http://www.webservicex.net/length.asmx?WSDL'
       destination_sum = get_distanse_km(file_content,url)
       print('Суммарное расстояние в пути в километрах - ', destination_sum)
main()