import pandas as pd


def writing_as_json_file(funk):
    """Декоратор, который записывает данные отчета в json-файл с названием по умолчанию"""
    def wrapper(*args, **kwargs):
        data = funk(*args, **kwargs)

        file_name = f"{funk.__name__}.json"

        if isinstance(data, pd.DataFrame):
            data.to_json(file_name, orient="records", indent=4, force_ascii=False)

        elif isinstance(data, pd.Series):
            data.to_json(file_name, orient="index", indent=4, force_ascii=False)

        return data

    return wrapper
