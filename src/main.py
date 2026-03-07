import eel
import requests
from file_manager import FileManager


eel.init('web')
fm = FileManager()
processes: list
cur_id: int = 0

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
    processes.append(proc)
    return {
        "id": proc["id"],
        "name": proc["name"],
        "avatar": str.upper(proc["name"][0]),
        "created": proc["created"]
    }

@eel.expose
def rename_process(pr_id: int, new_name: str):
    proc = next(filter(lambda pr: pr["id"] == pr_id, processes))
    proc["name"] = new_name
    fm.save_process(proc)

    return {
        "id": proc["id"],
        "name": proc["name"],
        "avatar": str.upper(proc["name"][0]),
        "created": proc["created"]
    }

@eel.expose
def select_process(pr_id: int):
    global cur_id
    cur_id = pr_id

@eel.expose
def add_message(text: str, sender: str, date: str):
    proc = next(filter(lambda pr: pr["id"] == cur_id, processes))
    msg = {
        "text": text,
        "user": sender,
        "date": date
    }
    proc["messages"].append(msg)

@eel.expose
def load_messages():
    proc = next(filter(lambda pr: pr["id"] == cur_id, processes))

    return proc["messages"]


if __name__ == "__main__":
    processes = fm.get_processes()
    eel.start('index.html', size=(3000, 2000))
