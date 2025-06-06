import requests
import ollama
import time

def get_weather(city="Taipei"):
    api_key = "你的API金鑰"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=zh_tw"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        humidity = data['main']['humidity']

        weather_info = f"城市: {city}\n天氣: {weather}\n溫度: {temp} °C\n濕度: {humidity}%"
        return weather_info
    else:
        return f"取得天氣資料失敗：{response.status_code}"

def generate_message(weather_info):
    response = ollama.chat(model='llama3.2:3b', messages=[        
        {
            'role': 'user',
            'content': f"請根據以下天氣資訊創造一則有趣的短訊：\n{weather_info}",
        },
    ])
    return response['message']['content']

interval = 3600 
city_name = "Taipei"

while True:
    weather_info = get_weather(city=city_name)
    funny_message = generate_message(weather_info)
    print("=" * 50)
    print("當前天氣有趣資訊:\n", funny_message)
    time.sleep(interval)