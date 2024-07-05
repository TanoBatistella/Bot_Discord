import requests

def get_weather(city):
    api_key = 'tu api de wheater'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=es'
    response = requests.get(url)
    return response.json()

def get_weather_message(member):
    city = 'Cordoba,ar'  
    weather = get_weather(city)
    temp = weather['main']['temp']
    description = weather['weather'][0]['description']

    if temp < 20:
        advice = "Si sales, abrígate que hace frío."
    else:
        advice = "Si sales, lleva ropa ligera que está caluroso."

    return f"Actualmente en {city} hace {temp}°C con {description}. {advice}"
