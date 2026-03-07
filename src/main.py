import eel
import requests
from file_manager import FileManager


eel.init('web')
fm = FileManager()
processes: list

def ID():
    data = fm.load_app_data()
    id_to_return = data["id"]
    data["id"] = id_to_return + 1
    fm.save_app_data(data)

    return id_to_return

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
            "id": proc["id"],
            "name": proc["name"],
            "avatar": str.upper(proc["name"][0]),
            "created": proc["created"]
        })

    return infos

@eel.expose
def create_new_process(pr_name: str):
    proc = fm.create_process(ID(), pr_name, "07.03.2026")

    return {
        "id": proc["id"],
        "name": proc["name"],
        "avatar": str.upper(proc["name"][0]),
        "created": proc["created"]
    }

if __name__ == "__main__":
    processes = fm.get_processes()
    eel.start('index.html', size=(3000, 2000))
