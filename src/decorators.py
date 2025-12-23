import logging

import pandas as pd

logging.basicConfig(
    level=logging.DEBUG,
    filemode='a',
    filename='C:\\Users\\Boo_D\\PycharmProjects\\Project_1\\logs\\reports.log',
    format='%(asctime)s-%(filename)s-%(funcName)s-%(levelname)s: %(message)s',
    datefmt='%d-%m-%d %H:%M:%S',
    encoding='utf-8'
)

decorators_logger = logging.getLogger("services")


def writing_as_json_file(funk):
    """Декоратор, который записывает данные отчета в json-файл с названием по умолчанию"""

    def wrapper(*args, **kwargs):
        decorators_logger.info("Получение данных декорируемой функции")
        data = funk(*args, **kwargs)

        decorators_logger.info("Формирование наименования файла")
        file_name = f"{funk.__name__}.json"

        decorators_logger.info("Проверка типа данных")
        if isinstance(data, pd.DataFrame):
            data.to_json(file_name, orient="records", indent=4, force_ascii=False)
            decorators_logger.info("Данные успешно записаны в json-файл")

        elif isinstance(data, pd.Series):
            data.to_json(file_name, orient="index", indent=4, force_ascii=False)
            decorators_logger.info("Данные успешно записаны в json-файл")

        return data

    return wrapper
