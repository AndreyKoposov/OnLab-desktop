import eel
from file_manager import FileManager
from config import ROOT
from assistant import Assistant
from process import Process


class AppData():
    def __init__(self) -> None:
        self._cur_id: int

    def get_id(self):
        return self._cur_id

    def set_id(self, cur_id: int):
        self._cur_id = cur_id

    cur_id = property(get_id, set_id)


eel.init(str(ROOT/'web'))
fm = FileManager()
processes: list[Process]
data = AppData()
assistant = Assistant()


def ID():
    data = fm.load_app_data()
    id_to_return = data["id"]
    data["id"] = id_to_return + 1
    fm.save_app_data(data)

    return id_to_return

# Процессы ============================
@eel.expose
def create_process(pr_name: str):
    proc = fm.create_process(ID(), pr_name, "07.03.2026")
    processes.append(proc)

@eel.expose
def edit_process(pr_id: int, new_name: str):
    proc = next(filter(lambda pr: pr.id == pr_id, processes))
    proc.name = new_name
    fm.save_process(proc)

@eel.expose
def delete_process(pr_id: int):
    proc = next(filter(lambda pr: pr.id == pr_id, processes))
    processes.remove(proc)
    fm.delete_process(pr_id)

@eel.expose
def set_option(option: int):
    proc = next(filter(lambda pr: pr.id == data.cur_id, processes))
    proc.option = option
    fm.save_process(proc)

@eel.expose
def fetch_processes():
    procs = []

    for proc in processes:
        procs.append({
            "id": proc.id,
            "name": proc.name,
            "avatar": str.upper(proc.name[0]),
            "created": proc.created,
            "option": proc.option,
            "count": proc.count_elements()
        })

    return procs

@eel.expose
def select_process(pr_id: int):
    data.cur_id = pr_id

# Ассистент ============================
@eel.expose
def send_message(text: str, time: str):
    proc = next(filter(lambda pr: pr.id == data.cur_id, processes))
    msg = {
        "text": text,
        "sender": "user",
        "time": time
    }
    proc.messages.append(msg)
    assistant.answer(text, proc)
    fm.save_process(proc)

@eel.expose
def fetch_messages():
    proc = next(filter(lambda pr: pr.id == data.cur_id, processes))

    return proc.messages

# XML ============================
@eel.expose
def get_xml_document():
    return {
        "content": fm.load_xml(data.cur_id),
        "isValid": True,
        "filename": "rdf.xml"
    }

@eel.expose
def save_xml_document(content: str):
    proc = next(filter(lambda pr: pr.id == data.cur_id, processes))
    isValid = proc.validate_xml(content)
    if isValid:
        fm.save_xml(data.cur_id, content)

    return {
        "success": isValid,
        "isValid": isValid,
        "error": "XML is invalid!"
    }

@eel.expose
def validate_xml(content: str):
    proc = next(filter(lambda pr: pr.id == data.cur_id, processes))
    return {"isValid": proc.validate_xml(content)}

# TABLE ============================
@eel.expose
def get_table_data():
    proc = next(filter(lambda pr: pr.id == data.cur_id, processes))
    params = proc.params

    table = []
    index = 0
    for item in params.items():
        for param_type in item[1].keys():
            for param in item[1][param_type]:
                entry = {}
                entry["param"] = param["name"]
                entry["feature"] = f"feature_{index}"
                entry["transformation"] = "one-hot encoding" if param["unit"] == '-' else "Стандартизация (z-score)"

                if param_type == "resource":
                    branch_entry = {}
                    branch_entry["param"] = f"Точка бифуркации: {param['name']}"
                    branch_entry["feature"] = "branching_flag"
                    branch_entry["transformation"] = "Условная ветвь"
                    table.append(branch_entry)


                table.append(entry)
                index += 1

    return table

# STRUCTURE ============================
@eel.expose
def get_process_stages():
    proc = next(filter(lambda pr: pr.id == data.cur_id, processes))
    result = []
    stages = proc.stages
    for stage in stages:
        try:
            entry = {
                "id": stages.index(stage), 
                "name": stage,
                "description": '...',
                "paramCount": proc.get_stage_params_count(stage) }
            result.append(entry)
        except KeyError as err:
            pass
    return result

@eel.expose
def get_stage_parameters(stage_id: int):
    proc = next(filter(lambda pr: pr.id == data.cur_id, processes))
    stage = proc.stages[stage_id]
    params = proc.params[stage]

    result = {
        "input": [],
        "control": [],
        "resource": [],
        "main": []

    }
    index = 0
    for param_type in params.keys():
        for param in params[param_type]:
            try:
                entry = {}
                entry["id"] = index
                entry["name"] = param["name"]
                entry["type"] = "int" if param["unit"] != '-' else "string"

                if param_type == "main":
                    result["main"].append(entry)
                elif param_type == "control":
                    result["control"].append(entry)
                elif param_type == "input":
                    result["input"].append(entry)
                else:
                    result["resource"].append(entry)

                index += 1
            except KeyError:
                pass
    return result

@eel.expose
def get_param_info(stage_id: int, name: str, category: str):
    info = {
        "id": 0,
        "name": name,
        "measure": '°C',
        "description": 'Описание параметра',
        "type": 'continuous',
        "value": 0,
        "unit": 'градус Цельсия',
        "constraints": '',
        "source": 'ГОСТ 1234.56'
    }

    proc = next(filter(lambda pr: pr.id == data.cur_id, processes))
    stage = proc.stages[stage_id]
    params = proc.params[stage][category]
    for param in params:
        if param["name"] == name:
            info["measure"] = param["unit"]
            info["unit"] = param["unit"]
            info["description"] = param["description"]
            info["type"] = "material" if param["unit"] == "-" else "continous"

            if category == "main":
                info["constraints"] = param["output_value"]
                info["value"] = "" if param["unit"] == "-" else param["output_value"]
            elif category == "control":
                info["constraints"] = param["input_value"]
                info["value"] = "" if param["unit"] == "-" else param["input_value"]
            elif category == "resource":
                info["constraints"] = param["expected_value"]
                info["condition"] = param["condition"]
                info["result"] = param["result"]
                info["value"] = "" if param["unit"] == "-" else param["expected_value"]
            else:
                info["constraints"] = param["input_value"]
                info["value"] = "" if param["unit"] == "-" else param["input_value"]

    return info

@eel.expose
def get_graph_data():
    proc = next(filter(lambda pr: pr.id == data.cur_id, processes))
    triplets = []
    for s, p, o in proc.rdf.g:
        triplets.append({
            "node1": replace_rdf(s, proc.id),
            "edge": replace_rdf(p, proc.id),
            "node2": replace_rdf(o, proc.id)
        })
    return triplets

@eel.expose
def get_bifur_data():
    proc = next(filter(lambda pr: pr.id == data.cur_id, processes))
    triplets = []

    # Stages
    for i, _ in enumerate(proc.stages):
        if i+1 < len(proc.stages):
            triplets.append({
                "node1": proc.stages[i],
                "edge": "✅",
                "node2": proc.stages[i+1]
            })

    # Resources
    for stage in proc.stages:
        for param in proc.params[stage]["resource"]:
            triplets.append({
                "node1": f"res:{param['name']}",
                "edge": param["condition"],
                "node2": stage
            })

    # Bifurcations
    for stage in proc.stages:
        for param in proc.params[stage]["resource"]:
            triplets.append({
                "node1": stage,
                "edge": "❌",
                "node2": f"bif:{param['result']}"
            })
    return triplets

def replace_rdf(el: str, pr_id: int) -> str:
    el = el.replace(f"http://{pr_id}/", "")
    el = el.replace("http://www.w3.org/1999/02/22-rdf-syntax-ns#", "")
    el = el.replace("http://www.w3.org/2001/XMLSchema#", "")
    el = el.replace("http://www.w3.org/2000/01/rdf-schema#", "")
    el = el.replace("http://www.w3.org/2002/07/owl#", "")

    return el


if __name__ == "__main__":
    processes = fm.get_processes()
    eel.start('index.html', mode="default", size=(3000, 2000), port=8100)
