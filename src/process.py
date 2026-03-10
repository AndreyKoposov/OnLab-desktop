from rdf_model import RdfModel


class Process():
    def __init__(self, new_id: int, name: str) -> None:
        self.__id: int = new_id
        self.name: str = name
        self.created: str = ""
        self.option: int = 1
        self.messages: list = []

        self.__entities: list[str] = []
        self.__stages: list[str] = []
        self.__transitions: list[str] = []
        self.__params: dict = {}

        self.__rdf = RdfModel(self.__id)

    def validate_xml(self, content: str) -> bool:
        return self.__rdf.validate_xml(content)

    def get_id(self):
        return self.__id

    def get_rdf(self):
        return self.__rdf

    def get_entities(self):
        return self.__entities

    def set_entities(self, entities: list[str]):
        self.__entities = entities
        self.__rdf.add_entities(entities)

    def get_stages(self):
        return self.__stages

    def set_stages(self, stages: list[str]):
        self.__stages = stages
        self.__rdf.add_stages(stages)

    def get_transitions(self):
        return self.__transitions

    def set_transitions(self, transitions: list[str]):
        self.__transitions = transitions

        pairs = []
        for t in transitions:
            [stage_from, stage_to] = t.split("->")
            pairs.append((stage_from, stage_to))

        self.__rdf.add_transitions(pairs)

    def get_params(self):
        return self.__params

    def set_params(self, params: dict):
        self.__params = params

        parameters = list[tuple[str, str, tuple[str, str], dict[str, str]]]()
        for item in params.items():
            stage = item[0]
            for param_type in item[1].keys():
                for param in item[1][param_type]:
                    name = param["name"]
                    unit = param["unit"]
                    new_param = (name, unit)
                    attrs = dict[str, str]()

                    if param_type == "main":
                        attrs["output_value"] = param["output_value"]
                    elif param_type in ("control" ,"input"):
                        attrs["input_value"] = param["input_value"]
                    else:
                        attrs["expected_value"] = param["expected_value"]
                        attrs["result"] = param["result"]
                        attrs["condition"] = param["condition"]

                    parameters.append((stage, param_type, new_param, attrs))


        self.__rdf.add_params(parameters)

    def get_stage_params_count(self, stage_name: str) -> int:
        params = self.__params[stage_name]
        count = 0
        for param_type in params.keys():
            for _ in params[param_type]:
                count += 1
        return count

    def count_elements(self) -> int:
        params_count = 0
        for stage in self.__stages:
            params_count += self.get_stage_params_count(stage)

        return len(self.__entities) + len(self.__stages) + params_count

    @staticmethod
    def serialize(proc) -> dict:
        res = proc.__dict__.copy()
        res.pop("_Process__rdf", None)

        return res

    @staticmethod
    def deserialize(json_data: dict):
        proc = Process(json_data["_Process__id"], json_data["name"])
        proc.created = json_data["created"]
        proc.option = json_data["option"]
        proc.messages = json_data["messages"]

        proc.entities = json_data["_Process__entities"]
        proc.stages = json_data["_Process__stages"]
        proc.transitions = json_data["_Process__transitions"]
        proc.params = json_data["_Process__params"]

        return proc

    id = property(get_id)
    rdf = property(get_rdf)
    entities = property(get_entities, set_entities)
    stages = property(get_stages, set_stages)
    transitions = property(get_transitions, set_transitions)
    params = property(get_params, set_params)
