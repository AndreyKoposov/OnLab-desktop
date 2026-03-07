import eel
import requests

# Инициализация Eel с папкой с веб-файлами
eel.init('web')  # папка с index.html, style.css, script.js

# Функция, которая будет доступна из JavaScript
@eel.expose
def ask_gigachat():
    # Здесь ваш код для обращения к вашему промежуточному сервису
    # или напрямую к GigaChat (но лучше через ваш сервис)
    response = requests.get(
        'http://90.156.155.241/api/gigachat',
        timeout=10
    )
    print(response.json()["content"])
    return response.json()["content"]


if __name__ == "__main__":
    # Запуск приложения
    eel.start('index.html')
