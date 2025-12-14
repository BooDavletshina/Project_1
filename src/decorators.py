def writing_as_json_file(funk):
    def wrapper(*args, **kwargs):
        data = funk(*args, **kwargs)

        file_name = f"{funk.__name__}_report.json"

        data.to_json(file_name, orient="records", indent=4, force_ascii=False)

        return data

    return wrapper
