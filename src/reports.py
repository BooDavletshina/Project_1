import datetime
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)."""

    df_transactions = transactions.copy()
    df_transactions["Дата операции"] = pd.to_datetime(df_transactions["Дата операции"], dayfirst=True)

    if date is None:
        date = datetime.datetime.now()
    else:
        date = datetime.datetime.strptime(date, "%d.%m.%Y")

    start_date = date - relativedelta(months = 3)
    filter_transactions = df_transactions[
        (df_transactions["Категория"] == category) &
        (df_transactions["Дата операции"] >= start_date) &
        (df_transactions["Дата операции"] <= date)]

    return filter_transactions


def spending_by_weekday(transactions: pd.DataFrame,
                        date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает средние траты в каждый из дней недели за последние три месяца (от переданной даты)."""
    df_transactions = transactions.copy()
    df_transactions["Дата операции"] = pd.to_datetime(df_transactions["Дата операции"], dayfirst=True)
    df_transactions["День недели"] = df_transactions["Дата операции"].dt.day_name()

    if date is None:
        date = datetime.datetime.now()
    else:
        date = datetime.datetime.strptime(date, "%d.%m.%Y")

    start_date  = date - relativedelta(months = 3)

    filter_transactions = df_transactions[
        (df_transactions["Дата операции"] >= start_date) &
        (df_transactions["Дата операции"] <= date)]

    weekday_grouped = filter_transactions.groupby("День недели")

    mean_transaction_amount_by_weekday = weekday_grouped["Сумма операции"].mean()

    return mean_transaction_amount_by_weekday


if __name__ == "__main__":
    excel_data_transactions = pd.read_excel("C:\\Users\\Boo_D\\PycharmProjects\\Project_1\\data\\operations.xlsx")
    # print(excel_data_transactions.head())
    # print(spending_by_category(excel_data_transactions, "Фастфуд", "03.10.2021"))
    # print(spending_by_weekday(excel_data_transactions, "03.10.2021"))