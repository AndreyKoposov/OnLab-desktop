from enum import Enum
from datetime import datetime
from prompts import p_entities, p_stages, p_transitions
from api_manager import ApiManager


class State(str, Enum):
    DEFAULT = "default"
    WAIT_TEXT = "wait_text"

class Assistant():
    def __init__(self) -> None:
        self.state: State = State.DEFAULT
        self.proc: dict = {}
        self.api = ApiManager()

    def answer(self, user_input: str, proc: dict):
        self.proc = proc
        match self.state:
            case State.DEFAULT:
                self.__do_command(user_input)
            case State.WAIT_TEXT:
                self.__check_text(user_input)

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

    def __help(self):
        answer = "Список команд:\n"\
                 "\t/help - список команд\n"\
                 "\t/analyze - анализ описания процесса\n"\
                 "\t/ontology - отчет об онтологии процесса\n"\
                 "\t/clear - очистка чата\n"\

        self.__answer(answer)

    def __analyze(self):
        answer = "Пожалуйста, введите текстовое описание процесса и я попробую разобраться!"
        self.__answer(answer)
        self.state = State.WAIT_TEXT

    def __ontology(self):
        pass

    def __clear(self):
        self.proc["messages"] = []
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
        self.proc["messages"].append(msg)

    def __start_analyze(self, desc: str):
        # Запрос у gigachat сущностей, этапов и переходов из текста
        # Сущности
        query = p_entities(desc)
        entities = self.api.get_entities(query)

        # Этапы
        #query = p_stages(desc)
        #res = ai.invoke(query)
        #stages = res['stages']

        ## Переходы между этапами
        #query = p_transitions(desc, stages)
        #res = ai.invoke(query)
        #transitions = res['transitions']

        # Вывод результата
        #self.__answer("Основные сущности процесса:\n- " + "\n- ".join(entities))
        #self.__answer("Основные этапы процесса:\n- " + "\n- ".join(stages))
        #self.__answer("Переходы между этапами:\n- " + "\n- ".join(transitions))
