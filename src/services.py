import logging

import pandas as pd

from src.decorators import writing_as_json_file

logging.basicConfig(
    level=logging.DEBUG,
    filemode='a',
    filename='C:\\Users\\Boo_D\\PycharmProjects\\Project_1\\logs\\services.log',
    format='%(asctime)s-%(filename)s-%(funcName)s-%(levelname)s: %(message)s',
    datefmt='%d-%m-%d %H:%M:%S',
    encoding='utf-8'
)

services_logger = logging.getLogger("services")


@writing_as_json_file
def profitable_cashback_categories(data: pd.DataFrame, year: int, month: int) -> pd.DataFrame:
    """Функция для анализа выгодности категорий повышенного кешбэка."""
    try:
        services_logger.info("Начало формирования аналитических данных")
        df_data = data.copy()

        df_data["Дата операции"] = pd.to_datetime(df_data["Дата операции"], dayfirst=True)

        df_data_filter = df_data[
            (df_data["Дата операции"].dt.year == year) &
            (df_data["Дата операции"].dt.month == month)
            ]

        df_data_grouped = df_data_filter.groupby("Категория")["Кэшбэк"].sum()

        df_data_sort = df_data_grouped.sort_values(ascending=False)

        services_logger.info("Отчет сформирован")
        return df_data_sort

    except Exception as e:
        services_logger.error(f'Произошла ошибка: {e}', exc_info=True)


if __name__ == "__main__":
    excel_data_transactions = pd.read_excel("C:\\Users\\Boo_D\\PycharmProjects\\Project_1\\data\\operations.xlsx")
    print(profitable_cashback_categories(excel_data_transactions, 2021, 11))
