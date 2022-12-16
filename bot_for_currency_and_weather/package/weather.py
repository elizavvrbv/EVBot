from requests import get

apikey = 'de62457187d9ae5d6978448607040ce5'


def get_weather(lat, lon):
    j = get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apikey}&lang=ru&units=metric"
    )
    data = j.json()
    weather = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    temp_feels = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    answer = f"Сейчас на улице {weather}, температура {temp}. \nОщущается как {temp_feels} \n" \
             f"Влажность {humidity}%. \nДанные предоставлены службой openweather"
    return answer
