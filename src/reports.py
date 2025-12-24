import datetime
import logging
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.decorators import writing_as_json_file

logging.basicConfig(
    level=logging.DEBUG,
    filemode='a',
    filename='C:\\Users\\Boo_D\\PycharmProjects\\Project_1\\logs\\reports.log',
    format='%(asctime)s-%(filename)s-%(funcName)s-%(levelname)s: %(message)s',
    datefmt='%d-%m-%d %H:%M:%S',
    encoding='utf-8'
)

reports_logger = logging.getLogger('reports')


@writing_as_json_file
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)."""
    try:
        reports_logger.info('Начало формирования отчета')
        df_transactions = transactions.copy()
        df_transactions["Дата операции"] = pd.to_datetime(df_transactions["Дата операции"], dayfirst=True)

        if date is None:
            date = datetime.datetime.now()
        else:
            date = datetime.datetime.strptime(date, "%d.%m.%Y")

        start_date = date - relativedelta(months=3)
        filter_transactions = df_transactions[
            (df_transactions["Категория"] == category) &
            (df_transactions["Дата операции"] >= start_date) &
            (df_transactions["Дата операции"] <= date)]

        reports_logger.info('Отчет сформирован')
        return filter_transactions

    except Exception as e:
        reports_logger.error(f'Произошла ошибка: {e}', exc_info=True)


@writing_as_json_file
def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает средние траты в каждый из дней недели за последние три месяца (от переданной даты)."""
    try:
        reports_logger.info('Начало формирования отчета')
        df_transactions = transactions.copy()
        df_transactions["Дата операции"] = pd.to_datetime(df_transactions["Дата операции"], dayfirst=True)
        df_transactions["День недели"] = df_transactions["Дата операции"].dt.day_name()

        if date is None:
            date = datetime.datetime.now()
        else:
            date = datetime.datetime.strptime(date, "%d.%m.%Y")

        start_date = date - relativedelta(months=3)

        filter_transactions = df_transactions[
            (df_transactions["Дата операции"] >= start_date) &
            (df_transactions["Дата операции"] <= date)]

        weekday_grouped = filter_transactions.groupby("День недели")

        mean_transaction_amount_by_weekday = weekday_grouped["Сумма операции"].mean()

        reports_logger.info('Отчет сформирован')
        return mean_transaction_amount_by_weekday

    except Exception as e:
        reports_logger.error(f'Произошла ошибка: {e}', exc_info=True)


@writing_as_json_file
def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """Функция выводит средние траты в рабочий и в выходной день за последние три месяца (от переданной даты)."""
    try:
        reports_logger.info('Начало формирования отчета')
        df_transactions = transactions.copy()
        df_transactions["Дата операции"] = pd.to_datetime(df_transactions["Дата операции"], dayfirst=True)
        df_transactions["День недели"] = df_transactions["Дата операции"].dt.weekday
        df_transactions["Тип дня"] = df_transactions["День недели"].apply(lambda x: "Выходной" if x>=5 else "Рабочий")

        if date is None:
            date = datetime.datetime.now()
        else:
            date = datetime.datetime.strptime(date, "%d.%m.%Y")

        start_date = date - relativedelta(months=3)

        filter_df_transactions = df_transactions[
            (df_transactions["Дата операции"] >= start_date) &
            (df_transactions["Дата операции"] <= date)
            ]

        workday_grouped = filter_df_transactions.groupby("Тип дня")

        mean_transaction_amount_by_workday = workday_grouped["Сумма операции"].mean()

        reports_logger.info('Отчет сформирован')
        return mean_transaction_amount_by_workday

    except Exception as e:
        reports_logger.error(f'Произошла ошибка: {e}', exc_info=True)


if __name__ == "__main__":
    excel_data_transactions = pd.read_excel("C:\\Users\\Boo_D\\PycharmProjects\\Project_1\\data\\operations.xlsx")
    # print(excel_data_transactions.head())
    # print(spending_by_category(excel_data_transactions, "Фастфуд"))
    # print(spending_by_weekday(excel_data_transactions,"03.10.2021"))
    print(spending_by_workday(excel_data_transactions, "03.10.2021"))
