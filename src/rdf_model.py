"""io, rdflib, transliterate, graphviz, parameter"""
from io import StringIO
from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import RDF, OWL, RDFS, XSD
from rdflib.tools.rdf2dot import rdf2dot
from transliterate import translit
from transliterate.contrib.languages import ru
import graphviz
from uuid import UUID


class RdfModel():
    """Класс для работы с rdf моделью"""
    def __init__(self) -> None:
        self.g = Graph()
        self.ns = Namespace("http://1/")

        # Понятие сущности
        entity = self.ns.entity
        self.g.add((entity, RDF.type, OWL.Class))

        # Понятие этапа
        stage = self.ns.stage
        self.g.add((stage, RDF.type, OWL.Class))

        # Понятие параметра
        parameter = self.ns.parameter
        self.g.add((parameter, RDF.type, OWL.Class))

        # Понятие "этап следует этапу"
        follows = self.ns.follows
        self.g.add((follows, RDF.type, RDF.Property))
        self.g.add((follows, RDFS.domain, stage))
        self.g.add((follows, RDFS.range, stage))

        # Понятие "имеет входной параметр"
        has_input = self.ns.hasInput
        self.g.add((has_input, RDF.type, RDF.Property))
        self.g.add((has_input, RDFS.domain, stage))
        self.g.add((has_input, RDFS.range, parameter))

        # Понятие "имеет управляющий параметр"
        has_control = self.ns.hasControl
        self.g.add((has_control, RDF.type, RDF.Property))
        self.g.add((has_control, RDFS.domain, stage))
        self.g.add((has_control, RDFS.range, parameter))

        # Понятие "имеет ресурс"
        has_resource = self.ns.hasResource
        self.g.add((has_resource, RDF.type, RDF.Property))
        self.g.add((has_resource, RDFS.domain, stage))
        self.g.add((has_resource, RDFS.range, parameter))

        # Понятие "имеет выходной параметр"
        has_main = self.ns.hasMain
        self.g.add((has_main, RDF.type, RDF.Property))
        self.g.add((has_main, RDFS.domain, stage))
        self.g.add((has_main, RDFS.range, parameter))

    def add_entities(self, entities: list[str]):
        """Добавляет сущности в модель"""
        for e in entities:
            e = self.transliterate_russian(e)
            uri = URIRef(self.ns + e)
            self.g.add((uri, RDF.type, self.ns.entity))

    def add_stages(self, stages: list[str]):
        """Добавляет этапы в модель"""
        for s in stages:
            s = self.transliterate_russian(s)
            uri = URIRef(self.ns + s)
            self.g.add((uri, RDF.type, self.ns.stage))

    def add_transitions(self, transitions: list[tuple[str, str]]):
        """Добавляет переходы между этапами в модель"""
        for stage_from, stage_to in transitions:
            stage_from = self.transliterate_russian(stage_from)
            stage_to = self.transliterate_russian(stage_to)

            self.g.add((self.ns[stage_to], self.ns.follows, self.ns[stage_from]))

    def add_params(self, parameters: list[tuple[str, str, tuple[str, str], dict[str, str]]]):
        """Добавляет параметры в модель, формат (stage, type, paramter, unit)"""
        for stage_name, p_type, param, _ in parameters:
            stage_name = self.transliterate_russian(stage_name)
            param_name = self.transliterate_russian(param[0])
            param_unit = self.transliterate_russian(param[1])

            param_uri = URIRef(self.ns + param_name)
            stage_uri =  URIRef(self.ns + stage_name)

            param_range = XSD.string if param_unit == "-" else XSD.double
            relation_type = None
            if p_type == "input":
                relation_type = self.ns.hasInput
            elif p_type == "control":
                relation_type = self.ns.hasControl
            elif p_type == "resource":
                relation_type = self.ns.hasResource
            else:
                relation_type = self.ns.hasMain

            self.g.add((param_uri, RDF.type, self.ns.parameter))
            self.g.add((param_uri, RDFS.range, param_range))
            self.g.add((stage_uri, relation_type, param_uri))

    def format_text(self, text: str) :
        """Убирает недопустимые символы из транслитерации"""
        return text.lower().replace(" ", "_").replace("'", "").replace("/", "_")

    def transliterate_russian(self, text):
        """Транслитерирует русский текст в латиницу"""
        print(ru.__file__)
        return self.format_text(translit(text, "ru", reversed=True))

    def to_xml(self):
        """Сериализует граф в xml формат"""
        # dest = file_name
        return self.g.serialize(format="xml")

    def to_img(self, file_name: str):
        """Сериализует граф в png картинку"""
        dot_data = StringIO()
        rdf2dot(self.g, dot_data)
        dot_content = dot_data.getvalue()
        dot_graph = graphviz.Source(dot_content)

        try:
            dot_graph.render(file_name, format="png", cleanup=True)
        except ValueError as error:
            print(f"{error}")

    def validate_xml(self, content: str) -> bool:
        g_temp = Graph()
        try:
            g_temp.parse(data=content, format="xml")
            if len(g_temp) == 0:
                return False
            return True
        except Exception:
            return False
