from pathlib import Path
from json import load, dump
from config import ROOT


class FileManager():
    work_dir = ROOT/"processes"
    suffix = ".onlab"

    def get_processes(self) -> list:
        processes_info = []

        for file in self.work_dir.iterdir():
            if file.is_dir():
                info = self.__get_process(file)
                processes_info.append(info)

        return processes_info

    def create_process(self, pr_id: int, name: str, created: str) -> dict:
        pr_dir = self.work_dir/f"pr_{pr_id}"
        pr_dir.mkdir()

        pr_structure_file = pr_dir/"structure.onlab"

        pr_structure = {
            "id": pr_id,
            "name": name,
            "created": created,

            "entities": [],
            "stages": [],
            "transitions": [],
            "params": [],
            "messages": []
        }

        with open(pr_structure_file, 'w', encoding='utf-8') as file:
            dump(pr_structure, file, indent=4)

        return pr_structure

    def save_process(self, process):
        pr_file = self.work_dir/f"pr_{process['id']}"/"structure.onlab"

        with open(pr_file, 'w', encoding='utf-8') as file:
            dump(process, file, indent=4)

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
