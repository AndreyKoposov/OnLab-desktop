def p_entities(desc: str):
    """Промт для GigaChat"""
    return '''
## ЗАДАЧА
Выдели основные сущности процесса из текста

## ФОРМАТ ОТВЕТА
Верни только строго валидный JSON без пояснений по следующему шаблону
{
    "entities": [
        "entities_name_1",
        "entities_name_2",
    ]
}

## ТЕКСТ
''' + desc + '''
'''

def p_stages(desc: str):
    """Промт для GigaChat"""
    return f"Выдели основные этапы процесса из текста: {desc}"

def p_transitions(desc: str, stages: list):
    """Промт для GigaChat"""
    return f"""Выдели основные ПЕРЕХОДЫ между этапами процесса 
            (ОБЯЗАТЕЛЬНО в формате этап1->этап2) из текста: 
            {desc}. Вот список основных этапов: {stages}"""