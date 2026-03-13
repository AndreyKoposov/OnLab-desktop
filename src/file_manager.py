from pathlib import Path
from json import load, dump
from config import ROOT
from os import makedirs
from process import Process


class FileManager():
    work_dir = ROOT/"processes"
    suffix = ".onlab"

    def __init__(self) -> None:
        if not Path.exists(self.work_dir):
            makedirs(self.work_dir)

    async def get_processes(self) -> list[Process]:
        processes = list[Process]()

        for file in self.work_dir.iterdir():
            if file.is_dir():
                info = self.__get_process(file)
                proc = Process.deserialize(info)
                processes.append(proc)

        return processes

    async def create_process(self, pr_id: int, name: str, created: str) -> Process:
        pr_dir = self.work_dir/f"pr_{pr_id}"
        pr_dir.mkdir()

        pr_structure_file = pr_dir/"structure.onlab"

        new_proc = Process(pr_id, name)
        new_proc.created = created
        pr_structure = Process.serialize(new_proc)

        with open(pr_structure_file, 'w', encoding='utf-8') as file:
            dump(pr_structure, file, indent=4)

        return new_proc

    def delete_process(self, pr_id: int):
        pr_dir = self.work_dir/f"pr_{pr_id}"
        for child in pr_dir.iterdir():
            if child.is_file():
                child.unlink()
            else:
                raise SystemError("Directory in process directory!")
        pr_dir.rmdir()

    def save_process(self, process: Process):
        pr_file = self.work_dir/f"pr_{process.id}"/"structure.onlab"
        pr_dict = Process.serialize(process)
        with open(pr_file, 'w', encoding='utf-8') as file:
            dump(pr_dict, file, indent=4)

        rdf_file = self.work_dir/f"pr_{process.id}"/"rdf.xml"
        process.rdf.to_xml(str(rdf_file))

    def process_to_png(self, process: Process):
        img_file = self.work_dir/f"pr_{process.id}"/"rdf"
        process.rdf.to_img(str(img_file))

    def load_xml(self, pr_id: int) -> str:
        pr_file = self.work_dir/f"pr_{pr_id}"/"rdf.xml"
        with open(pr_file, 'r', encoding='utf-8') as file:
            return file.read()

    def save_xml(self, pr_id: int, content: str):
        pr_file = self.work_dir/f"pr_{pr_id}"/"rdf.xml"
        with open(pr_file, 'w', encoding='utf-8') as file:
            file.write(content)

    def load_app_data(self):
        with open(ROOT/"data.json", 'r', encoding='utf-8') as file:
            return load(file)

    def save_app_data(self, data: dict):
        with open(ROOT/"data.json", 'w', encoding='utf-8') as file:
            dump(data, file, indent=4)

    def __get_process(self, process_dir: Path) -> dict:
        for file in process_dir.iterdir():
            if file.is_file() and file.suffix == self.suffix:
                return self.__read_onlab_file(file)

        return {}

    def __read_onlab_file(self, file: Path) -> dict:
        with open(file, 'r', encoding='utf-8') as onlab_file:
            process = load(onlab_file)

        return process
