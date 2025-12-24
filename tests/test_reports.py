import pandas as pd
from pandas.testing import assert_frame_equal

from src.reports import spending_by_weekday, spending_by_category, spending_by_workday


def test_spending_by_category(df_transactions):
    expected_result = spending_by_category(df_transactions, 'Фастфуд', '06.01.2021').reset_index(drop=True)

    actual_result = pd.DataFrame({
        'Дата операции': ['01.01.2021', '03.01.2021'],
        'Категория': ['Фастфуд', 'Фастфуд'],
        'Сумма операции': [100, 300]
    }).reset_index(drop=True)

    actual_result['Дата операции'] = pd.to_datetime(actual_result['Дата операции'], dayfirst=True)

    assert_frame_equal(expected_result, actual_result)


def test_spending_by_category_not_date(df_transactions):
    result = spending_by_category(df_transactions, 'Фастфуд')

    assert result.empty


def test_spending_by_weekday(df_transactions_excel):
    result = spending_by_weekday(df_transactions_excel, "03.10.2021")

    assert result.loc["Monday"] == -466.9661818181818


def test_spending_by_weekday_not_date(df_transactions_excel):
    result = spending_by_weekday(df_transactions_excel)

    assert result.empty


def test_spending_by_workday(df_transactions_excel):
    result = spending_by_workday(df_transactions_excel, "03.10.2021")

    assert result.loc["Выходной"] == -270.8437234042553
    assert result.loc["Рабочий"] == -1266.7234905660375


def test_spending_by_workday_not_date(df_transactions_excel):
    result = spending_by_workday(df_transactions_excel)

    assert result.empty
