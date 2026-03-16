from fastapi import FastAPI, Response, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db_manager import DbManager
from assistant import Assistant
from process import Process
import uvicorn
from models import OnLabResponse, OnLabRequest
from uuid import UUID


class AppData():
    def __init__(self) -> None:
        self._cur_id: int

    def get_id(self):
        return self._cur_id

    def set_id(self, cur_id: int):
        self._cur_id = cur_id

    cur_id = property(get_id, set_id)

router = APIRouter()
app = FastAPI(title="Ontology Lab")
app.state.dm = DbManager()
app.state.processes = []
app.state.cur_id = ""
app.state.assistant = Assistant()
app.state.user_id = app.state.dm.get_user_id_by_name("andrey")
app.mount("/static", StaticFiles(directory="src/static"), name="static")


def ID():
    data = app.state.fm.load_app_data()
    id_to_return = data["id"]
    data["id"] = id_to_return + 1
    app.state.fm.save_app_data(data)

    return id_to_return

# Процессы ============================
@router.post("/processes/create")
def create_process(request: OnLabRequest):
    # proc = await app.state.fm.create_process(ID(), request.pr_name, "07.03.2026")
    proc = app.state.dm.create_process(app.state.user_id, request.pr_name, "07.03.2026")
    app.state.processes.append(proc)

@router.post("/processes/rename")
def edit_process(request: OnLabRequest):
    proc = next(filter(lambda pr: pr.id == request.pr_id, app.state.processes))
    proc.name = request.new_name
    if app.state.dm.update_process(proc) is None:
        raise ValueError

@router.post("/processes/delete")
def delete_process(request: OnLabRequest):
    proc = next(filter(lambda pr: pr.id == request.pr_id, app.state.processes))
    app.state.processes.remove(proc)
    if app.state.dm.delete_process(request.pr_id) is None:
        raise ValueError

@router.post("/processes/set-option")
def set_option(request: OnLabRequest):
    proc = next(filter(lambda pr: pr.id == app.state.cur_id, app.state.processes))
    proc.option = request.option
    app.state.dm.update_process(proc)

@router.get("/processes", response_model=OnLabResponse)
def fetch_processes():
    # app.state.processes = await app.state.fm.get_processes()
    app.state.processes = app.state.dm.get_processes(app.state.user_id)
    procs = []
    for proc in app.state.processes:
        procs.append({
            "id": proc.id,
            "name": proc.name,
            "avatar": str.upper(proc.name[0]),
            "created": proc.created,
            "option": proc.option,
            "count": proc.count_elements()
        })

    return OnLabResponse(content=procs)

@router.post("/processes/select")
def select_process(request: OnLabRequest):
    app.state.cur_id = request.pr_id

# Ассистент ============================
@router.post("/processes/chat/send")
def send_message(request: OnLabRequest):
    proc = next(filter(lambda pr: pr.id == app.state.cur_id, app.state.processes))
    msg = {
        "text": request.text,
        "sender": "user",
        "time": request.time
    }
    proc.messages.append(msg)
    app.state.assistant.answer(request.text, proc)
    app.state.dm.update_process(proc)

@router.get("/processes/chat/")
def fetch_messages():
    proc = next(filter(lambda pr: pr.id == app.state.cur_id, app.state.processes))

    return OnLabResponse(content=proc.messages)

# XML ============================
@router.get("/processes/xml/")
def get_xml_document():
    proc = next(filter(lambda pr: pr.id == app.state.cur_id, app.state.processes))
    return OnLabResponse(structure={
        "content": proc.rdf.to_xml(),
        "isValid": True,
        "filename": "rdf.xml"
    })

@router.post("/processes/xml/save")
def save_xml_document(request: OnLabRequest):
    return OnLabResponse(structure={
        "success": True,
        "isValid": True,
        "error": "XML is invalid!"
    })
    # proc = next(filter(lambda pr: pr.id == app.state.cur_id, app.state.processes))
    # isValid = proc.validate_xml(request.content)
    # if isValid:
    #     app.state.fm.save_xml(app.state.cur_id, request.content)

    # return OnLabResponse(structure={
    #     "success": isValid,
    #     "isValid": isValid,
    #     "error": "XML is invalid!"
    # })

@router.post("/processes/xml/check")
def validate_xml(request: OnLabRequest):
    proc = next(filter(lambda pr: pr.id == app.state.cur_id, app.state.processes))
    return OnLabResponse(structure={"isValid": proc.validate_xml(request.content)})

# TABLE ============================
@router.get("/processes/table")
def get_table_data():
    proc = next(filter(lambda pr: pr.id == app.state.cur_id, app.state.processes))
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

    return OnLabResponse(content=table)

# STRUCTURE ============================
@router.get("/processes/stages")
def get_process_stages():
    proc = next(filter(lambda pr: pr.id == app.state.cur_id, app.state.processes))
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
    return OnLabResponse(content=result)

@router.post("/processes/params")
def get_stage_parameters(request: OnLabRequest):
    proc = next(filter(lambda pr: pr.id == app.state.cur_id, app.state.processes))
    stage = proc.stages[request.stage_id]
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
    return OnLabResponse(structure=result)

@router.post("/processes/params/info")
def get_param_info(request: OnLabRequest):
    info = {
        "id": 0,
        "name": request.name,
        "measure": '°C',
        "description": 'Описание параметра',
        "type": 'continuous',
        "value": 0,
        "unit": 'градус Цельсия',
        "constraints": '',
        "source": 'ГОСТ 1234.56'
    }

    proc = next(filter(lambda pr: pr.id == app.state.cur_id, app.state.processes))
    stage = proc.stages[request.stage_id]
    params = proc.params[stage][request.category]
    for param in params:
        if param["name"] == request.name:
            info["measure"] = param["unit"]
            info["unit"] = param["unit"]
            info["description"] = param["description"]
            info["type"] = "material" if param["unit"] == "-" else "continous"

            if request.category == "main":
                info["constraints"] = param["output_value"]
                info["value"] = "" if param["unit"] == "-" else param["output_value"]
            elif request.category == "control":
                info["constraints"] = param["input_value"]
                info["value"] = "" if param["unit"] == "-" else param["input_value"]
            elif request.category == "resource":
                info["constraints"] = param["expected_value"]
                info["condition"] = param["condition"]
                info["result"] = param["result"]
                info["value"] = "" if param["unit"] == "-" else param["expected_value"]
            else:
                info["constraints"] = param["input_value"]
                info["value"] = "" if param["unit"] == "-" else param["input_value"]

    return OnLabResponse(structure=info)

# GRAPHS ============================
@router.get("/processes/graph")
def get_graph_data():
    proc = next(filter(lambda pr: pr.id == app.state.cur_id, app.state.processes))
    triplets = []
    for s, p, o in proc.rdf.g:
        triplets.append({
            "node1": replace_rdf(s, proc.id),
            "edge": replace_rdf(p, proc.id),
            "node2": replace_rdf(o, proc.id)
        })
    return OnLabResponse(content=triplets)

@router.get("/processes/bifur")
def get_bifur_data():
    proc = next(filter(lambda pr: pr.id == app.state.cur_id, app.state.processes))
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
    return OnLabResponse(content=triplets)


def replace_rdf(el: str, pr_id: int) -> str:
    el = el.replace(f"http://{pr_id}/", "")
    el = el.replace("http://www.w3.org/1999/02/22-rdf-syntax-ns#", "")
    el = el.replace("http://www.w3.org/2001/XMLSchema#", "")
    el = el.replace("http://www.w3.org/2000/01/rdf-schema#", "")
    el = el.replace("http://www.w3.org/2002/07/owl#", "")

    return el


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8010)
