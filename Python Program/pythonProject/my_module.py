import requests

城市 = "上海"
api = "43021a1c1e84c7947d51807ce22fa020"
网址 = f"https://api.openweathermap.org/data/2.5/weather?q={城市}&appid={api}"
天气资料 = requests.get(网址)
print(天气资料)