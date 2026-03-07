import eel
import requests
from file_manager import FileManager


eel.init('web')
fm = FileManager()
processes: list

@eel.expose
def ask_gigachat():
    response = requests.get(
        'http://90.156.155.241/api/gigachat',
        timeout=10
    )
    print(response.json()["content"])
    return response.json()["content"]

@eel.expose
def get_processes_list():
    infos = []

    for proc in processes:
        infos.append({
            "name": proc["name"],
            "avatar": str.upper(proc["name"][0]),
            "created": proc["created"]
        })

    return infos


if __name__ == "__main__":
    processes = fm.get_processes()
    eel.start('index.html', size=(3000, 2000))
