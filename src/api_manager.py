from requests import post, get
from urllib.parse import unquote


class ApiManager():
    #url = 'http://90.156.155.241/api/'
    url = 'http://localhost:8000/api/'

    @staticmethod
    def get_entities(prompt: str):
        data = {"prompt": prompt}
        headers = {
            'accept': 'application/json',
            "Content-Type": "application/json",
        }
        response = post(
            ApiManager.url + 'entities',
            headers=headers,
            data=data,
            timeout=120
        )
        print(response.json())


# Фотолитография — метод получения рисунка на поверхности материала. 
# На подложку наносится фоторезист, который засвечивается через фотошаблон, 
# проявляется, а затем используется для травления или напыления. 
# Фотолитография начинается с нанесения фоторезиста на подложку. 
# Затем происходит засвечивание через фотошаблон, проявление и 
# использование для травления или напыления.
