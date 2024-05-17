import telebot
import requests
import json

bot = telebot.TeleBot('5532422953:AAHJK9jVpP8zahLcupzvkzGS65VK-o7pRGs')
API_weather_key ='abe94cb9-3315-4922-91c0-374bfd533b49'
API_geocode_key ='97f7d0e7-f90b-4f2c-b1d5-fa6c38d1d35a'
headers_weather = {"X-Yandex-API-Key":API_weather_key}

def str_to_num_from_data(location):
    pos_space = location.index(' ')
    #lon = float(location[:pos_space])
    #lat = float(location[pos_space:])
    return float(location[:pos_space]),float(location[pos_space:])
    #print(f'flat:{lat}, lon:{lon}')
def str_to_str_from_data(location):
    pos_space = location.index(' ')
    return location[:pos_space], location[pos_space:]

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Привет, рад тебя видеть!Напиши название населенного пункта:')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    
    response_geo = requests.get(f'https://geocode-maps.yandex.ru/1.x/?apikey={API_geocode_key}&geocode={city}&format=json')
    data = json.loads(response_geo.text)
    #print(response_geo.json())
    bot.reply_to(message,f'твои координаты: {data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]}')
    
    location = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
    lon,lat = str_to_str_from_data(location)# два float числа через пробел в строке 
    print(f'lat:{lat},lon:{lon}')
    
    
    
    #response = requests.post('https://api.weather.yandex.ru/graphql/query', headers=headers, json={'query': query})
    #print(response.content)
    #lat=52.3715&lon=4.89388',headers=headers_weather)
    #response_weather = requests.get(f'https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon{lon}', headers=headers_weather)
    #bot.reply_to(message,lat)
    
    query = """{
    weatherByPoint(request: { lat:"""+lat +",lon:" + lon + """ }) {
        now {
        cloudiness
        humidity
        precType
        precStrength
        pressure
        temperature
        windSpeed
        windDirection
        }
    }
    }"""
    response = requests.post('https://api.weather.yandex.ru/graphql/query', headers=headers_weather, json={'query': query})
    print(response.content)
    #print(json.loads(response_weather.text))


#    print(response_geo.json())



bot.polling(none_stop=True)
