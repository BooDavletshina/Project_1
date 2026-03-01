import pandas as pd
import pytest


@pytest.fixture
def df_transactions():
    df = pd.DataFrame({
        'Дата операции': ['01.01.2021', '02.01.2021', '03.01.2021', '04.01.2021', '05.01.2021', '06.01.2021'],
        'Категория': ['Фастфуд', 'Аптека', 'Фастфуд', 'Аптека', 'Супермаркеты', 'Супермаркеты'],
        'Сумма операции': [100, 200, 300, 400, 500, 600]
    })
    return df


@pytest.fixture
def df_transactions_excel():
    excel_data_transactions = pd.read_excel("C:\\Users\\Boo_D\\PycharmProjects\\Project_1\\data\\operations.xlsx")
    return excel_data_transactions

@pytest.fixture
def mock_df():
    return pd.DataFrame({'id': [1, 2], 'amount': [100, 200]})