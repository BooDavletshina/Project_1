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


@pytest.fixture
def sample_transactions_df():
    """Создает тестовый DataFrame с транзакциями"""
    data = {
        "Номер карты": ["*1234", "*1234", "*5678", "*1234", None],
        "Сумма операции": [-1000.0, -2000.0, -500.0, 500.0, -100.0],  # Отрицательные - расходы
        "Статус": ["OK", "OK", "OK", "OK", "FAILED"],
        "Дата платежа": ["01.01.2023", "02.01.2023", "03.01.2023", "04.01.2023", "05.01.2023"],
        "Категория": ["Супермаркеты", "Аптеки", "Транспорт", "Переводы", "Еда"],
        "Описание": ["Покупка 1", "Покупка 2", "Покупка 3", "Пополнение", "Ошибка"]
    }
    return pd.DataFrame(data)


@pytest.fixture
def empty_df():
    """Создает пустой DataFrame с нужными колонками"""
    return pd.DataFrame(columns=["Номер карты", "Сумма операции", "Статус", "Дата платежа", "Категория", "Описание"])


@pytest.fixture
def mock_user_settings():
    """Фикстура для имитации содержимого json-файла настроек"""
    return {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "TSLA"]
    }


@pytest.fixture
def mock_cbr_response():
    """Фикстура для ответа API ЦБ РФ"""
    return {
        "Valute": {
            "USD": {"Value": 75.50}
        }
    }
