from pathlib import Path
from json import load
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

    def __get_process(self, process_dir: Path) -> dict:
        for file in process_dir.iterdir():
            if file.is_file() and file.suffix == self.suffix:
                return self.__read_onlab_file(file)

        return {}

    def __read_onlab_file(self, file: Path) -> dict:
        with open(file, 'r', encoding='utf-8') as onlab_file:
            process = load(onlab_file)

        return process
