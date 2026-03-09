from requests import post, get
from json import dumps
from urllib.parse import unquote


class ApiManager():
    url = 'http://90.156.155.241/api/'
    #url = 'http://localhost:8000/api/'

    @staticmethod
    def request(prompt: str, path: str):
        payload = {"prompt": dumps(prompt)}
        headers = {
            'accept': 'application/json',
            "Content-Type": "application/json",
        }
        response = post(
            ApiManager.url + path,
            headers=headers,
            json=payload,
            timeout=120
        )
        print(response.json()["content"])
        return response.json()["content"]


# Фотолитография — метод получения рисунка на поверхности материала. 
# На подложку наносится фоторезист, который засвечивается через фотошаблон, 
# проявляется, а затем используется для травления или напыления. 
# Фотолитография начинается с нанесения фоторезиста на подложку. 
# Затем происходит засвечивание через фотошаблон, проявление и 
# использование для травления или напыления.
