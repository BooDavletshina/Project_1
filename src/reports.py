import datetime

from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)."""

    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])

    if date is None:
        date = datetime.datetime.now()
    else:
        date = datetime.datetime.strptime(date, "%d.%m.%Y")

    start_date = date - relativedelta(month=3)
    filter_transactions = transactions[
        (transactions["Категория"] == category) &
        (transactions["Дата операции"] >= start_date) &
        (transactions["Дата операции"] <= date)]

    return filter_transactions
