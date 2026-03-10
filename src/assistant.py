from enum import Enum
from datetime import datetime
from prompts import p_entities, p_stages, p_transitions, p_params
from api_manager import ApiManager
from process import Process


class State(str, Enum):
    DEFAULT = "default"
    WAIT_TEXT = "wait_text"
    CONFIRM = "confirm"

class Assistant():
    def __init__(self) -> None:
        self.state: State = State.DEFAULT
        self.proc: Process
        self.api = ApiManager()

        self.temp_entities = []
        self.temp_stages = []
        self.temp_transitions = []
        self.temp_params = {}

    def answer(self, user_input: str, proc: Process):
        self.proc = proc
        match self.state:
            case State.DEFAULT:
                self.__do_command(user_input)
            case State.WAIT_TEXT:
                self.__check_text(user_input)
            case State.CONFIRM:
                self.__check_confirm(user_input)

    def __check_text(self, user_input: str):
        if len(user_input) < 30:
            return self.__answer("Описание слишком короткое, ничего не понятно. \
                                 Пожалуйста, опишите процесс подробнее")

        if len(user_input) > 1500:
            return self.__answer("Описание слишком длинное. \
                                 Пожалуйста, опишите процесс компактнее")

        return self.__start_analyze(user_input)

    def __do_command(self, user_input: str):
        match user_input:
            case "/help":
                self.__help()
            case "/analyze":
                self.__analyze()
            case "/ontology":
                self.__ontology()
            case "/clear":
                self.__clear()
            case _:
                self.__unknown()

    def __check_confirm(self, user_input: str):
        user_input = user_input.lower().strip()

        if user_input == "да":
            self.proc.entities = self.temp_entities
            self.proc.stages = self.temp_stages
            self.proc.transitions = self.temp_transitions
            self.proc.params = self.temp_params
            self.state = State.DEFAULT
            self.__answer("Структура создана")
        elif user_input == "нет":
            self.state = State.DEFAULT
            self.__answer("Анализ отменен")
        else:
            self.__answer("Введите (да/нет)")

    def __help(self):
        answer = "Список команд:\n"\
                 "\t/help - список команд\n"\
                 "\t/analyze - анализ описания процесса\n"\
                 "\t/ontology - отчет об онтологии процесса\n"\
                 "\t/clear - очистка чата\n"\

        self.__answer(answer)

    def __analyze(self):
        answer = "Пожалуйста, введите текстовое описание процесса и я попробую разобраться. \
        \n!!! Анализ может занять до 30 секунд !!!"
        self.__answer(answer)
        self.state = State.WAIT_TEXT

    def __ontology(self):
        pass

    def __clear(self):
        self.proc.messages = []
        answer = "Чат очищен!"
        self.__answer(answer)

    def __unknown(self):
        answer = "Я не совсем понял"
        self.__answer(answer)

    def __answer(self, text: str):
        now = datetime.now()
        time = now.strftime('%Y-%m-%d')
        msg = {
            "text": text,
            "sender": "assistant",
            "time": time
        }
        self.proc.messages.append(msg)

    def __start_analyze(self, desc: str):
        # Запрос у gigachat сущностей, этапов и переходов из текста
        # Сущности
        query = p_entities(desc)
        self.temp_entities = self.api.request(query, 'entities')
        # Этапы
        query = p_stages(desc)
        self.temp_stages = self.api.request(query, 'stages')

        # Upper case first char
        self.temp_entities = list(map(str.capitalize, self.temp_entities))
        self.temp_stages = list(map(str.capitalize, self.temp_stages))

        # Переходы между этапами
        query = p_transitions(desc, self.temp_stages)
        self.temp_transitions = self.api.request(query, 'transitions')


        # Вывод результата
        self.__answer("Основные сущности процесса:\n- " + "\n- ".join(self.temp_entities))
        self.__answer("Основные этапы процесса:\n- " + "\n- ".join(self.temp_stages))
        self.__answer("Переходы между этапами:\n- " + "\n- ".join(self.temp_transitions))

        # Вывод результата
        query = p_params(desc, self.temp_stages)
        self.temp_params = self.api.request(query, 'params')
        self.__answer(self.__params_to_str(self.temp_params))

        self.__answer("Создать на основании анализа структуру процесса? (да/нет)")
        self.state = State.CONFIRM

    def __params_to_str(self, stages_params: dict):
        """Преобразует JSON в текст для пользователя"""
        reply = ""

        for item in stages_params.items():
            reply += f"\n\nЭтап - {item[0]}"

            reply += "\nВыходные параметры:"
            for param in item[1]["main"]:
                name = param["name"]
                unit = param["unit"]
                value = param["output_value"]
                descr = param["description"]
                reply += f"\n\t- {name} | {unit} ({value}) | {descr}"

            reply += "\nУправляющие параметры:"
            for param in item[1]["control"]:
                name = param["name"]
                unit = param["unit"]
                value = param["input_value"]
                descr = param["description"]
                reply += f"\n\t- {name} | {unit} ({value}) | {descr}"

            reply += "\nВходные параметры:"
            for param in item[1]["input"]:
                name = param["name"]
                unit = param["unit"]
                value = param["input_value"]
                descr = param["description"]
                reply += f"\n\t- {name} | {unit} ({value}) | {descr}"

            reply += "\nОбеспечивающие параметры:"
            for param in item[1]["resource"]:
                name = param["name"]
                unit = param["unit"]
                value = param["expected_value"]
                result = param["result"]
                condition = param["condition"]
                descr = param["description"]
                reply += f"\n\t- {name} | {unit} ({condition} {value} => {result}) | {descr}"

        return reply
