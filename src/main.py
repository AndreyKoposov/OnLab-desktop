import eel
import requests
from file_manager import FileManager


class AppData():
    def __init__(self) -> None:
        self._cur_id: int

    def get_id(self):
        return self._cur_id

    def set_id(self, cur_id: int):
        self._cur_id = cur_id

    cur_id = property(get_id, set_id)


eel.init('web')
fm = FileManager()
processes: list
data = AppData()


def ID():
    data = fm.load_app_data()
    id_to_return = data["id"]
    data["id"] = id_to_return + 1
    fm.save_app_data(data)

    return id_to_return

@eel.expose
def create_process(pr_name: str):
    proc = fm.create_process(ID(), pr_name, "07.03.2026")
    processes.append(proc)

@eel.expose
def edit_process(pr_id: int, new_name: str):
    proc = next(filter(lambda pr: pr["id"] == pr_id, processes))
    proc["name"] = new_name
    fm.save_process(proc)

@eel.expose
def delete_process(pr_id: int):
    proc = next(filter(lambda pr: pr["id"] == pr_id, processes))
    processes.remove(proc)
    fm.delete_process(pr_id)

@eel.expose
def set_option(option: int):
    proc = next(filter(lambda pr: pr["id"] == data.cur_id, processes))
    proc["option"] = option
    fm.save_process(proc)

@eel.expose
def fetch_processes():
    procs = []

    for proc in processes:
        procs.append({
            "id": proc["id"],
            "name": proc["name"],
            "avatar": str.upper(proc["name"][0]),
            "created": proc["created"],
            "option": proc["option"]
        })

    return procs

@eel.expose
def select_process(pr_id: int):
    data.cur_id = pr_id

@eel.expose
def ask_gigachat():
    response = requests.get(
        'http://90.156.155.241/api/gigachat',
        timeout=10
    )
    print(response.json()["content"])
    return response.json()["content"]

@eel.expose
def send_message(text: str, time: str):
    proc = next(filter(lambda pr: pr["id"] == data.cur_id, processes))
    msg = {
        "text": text,
        "sender": "user",
        "time": time
    }
    proc["messages"].append(msg)
    msg = {
        "text": "Hello, user. My name is GigaChat!",
        "sender": "assistant",
        "time": time
    }
    proc["messages"].append(msg)
    fm.save_process(proc)

@eel.expose
def fetch_messages():
    proc = next(filter(lambda pr: pr["id"] == data.cur_id, processes))

    return proc["messages"]


if __name__ == "__main__":
    processes = fm.get_processes()
    eel.start('index.html', size=(3000, 2000))
