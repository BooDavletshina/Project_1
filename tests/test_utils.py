import json
from datetime import datetime
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
import pytest

from src.utils import (get_currency_rates, get_data_cards, get_greeting, get_stock_prices, get_top_transactions,
                       get_usd_rub, read_transactions_excel)


@patch('pandas.read_excel')
@patch('src.utils.utils_logger')
def test_read_transactions_excel_success(mock_logger, mock_read_excel, mock_df):
    """Тест успешного чтения Excel файла"""
    mock_read_excel.return_value = mock_df

    result = read_transactions_excel('fake_path.xlsx')

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    mock_read_excel.assert_called_once_with('fake_path.xlsx')
    mock_logger.info.assert_called_with('Данные из Excel-файла успешно преобразованы в дата-фрейм')


@patch('pandas.read_excel')
@patch('src.utils.utils_logger')
def test_read_transactions_excel_file_not_found(mock_logger, mock_read_excel):
    """Тест обработки ошибки отсутствия файла"""
    mock_read_excel.side_effect = FileNotFoundError("File not found")

    result = read_transactions_excel('non_existent.xlsx')

    assert result == []
    mock_logger.error.assert_called()


@pytest.mark.parametrize("hour, expected_greeting", [
    (7, "Доброе утро!"),
    (11, "Доброе утро!"),
    (13, "Добрый день!"),
    (15, "Добрый день!"),
    (19, "Добрый вечер!"),
    (21, "Добрый вечер!"),
    (23, "Доброй ночи!"),
    (3, "Доброй ночи!"),
])
def test_get_greeting_times(hour, expected_greeting):
    """Параметризованный тест приветствий в зависимости от часа"""

    # Создаем фиксированную дату с подменой часа
    fixed_date = datetime(2023, 10, 10, hour, 0, 0)

    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now.return_value = fixed_date

        assert get_greeting() == expected_greeting


@patch('src.utils.utils_logger')
def test_get_greeting_exception(mock_logger):
    """Тест обработки исключения внутри get_greeting"""
    with patch('datetime.datetime') as mock_datetime:
        # Имитируем ошибку при вызове .now()
        mock_datetime.now.side_effect = Exception("System error")

        result = get_greeting()

        assert result is None  # Так как в функции нет return в блоке except
        mock_logger.error.assert_called()


@patch('src.utils.utils_logger')
def test_get_data_cards_success(mock_logger, sample_transactions_df):
    """Тест корректного расчета суммы и кешбэка по картам"""
    result = get_data_cards(sample_transactions_df)

    # Проверка карты *1234: расходы (-1000) + (-2000) = 3000 (abs)
    # Положительная операция 500 и FAILED операция не должны учитываться
    card_1234 = next(item for item in result if item["Номер карты"] == "1234")
    assert card_1234["Сумма операции"] == 3000.0
    assert card_1234["Кешбэк"] == 30.0

    # Проверка карты *5678
    card_5678 = next(item for item in result if item["Номер карты"] == "5678")
    assert card_5678["Сумма операции"] == 500.0
    assert card_5678["Кешбэк"] == 5.0

    assert mock_logger.info.called


@pytest.mark.parametrize("input_df, expected_length", [
    (pd.DataFrame(columns=["Номер карты", "Сумма операции", "Статус"]), 0),
])
@patch('src.utils.utils_logger')
def test_get_data_cards_empty(mock_logger, input_df, expected_length):
    """Тест проверяет, что на пустой DataFrame функция возвращает пустой список"""
    result = get_data_cards(input_df)

    assert result == []
    assert len(result) == expected_length


def test_get_top_transactions_sorting(sample_transactions_df):
    """Тест выбора топ-5 самых дорогих покупок (самые большие отрицательные числа)"""
    # Добавим еще данных, чтобы было больше 5
    extra_data = pd.DataFrame({
        "Номер карты": ["*1111"] * 5,
        "Сумма операции": [-5000.0, -4000.0, -100.0, -200.0, -300.0],
        "Статус": ["OK"] * 5,
        "Дата платежа": ["01.01.2023"] * 5,
        "Категория": ["Тест"] * 5,
        "Описание": ["Топ"] * 5
    })
    full_df = pd.concat([sample_transactions_df, extra_data])

    result = get_top_transactions(full_df)

    assert len(result) <= 5
    # Проверяем, что первая в списке — самая крупная трата (5000)
    assert result[0]["Сумма операции"] == 5000.0
    # Проверяем наличие необходимых ключей
    assert all(k in result[0] for k in ["Дата платежа", "Сумма операции", "Категория", "Описание"])


@patch('src.utils.utils_logger')
def test_get_top_transactions_exception(mock_logger):
    """Тест обработки исключения при некорректном типе данных"""
    # Передаем None вместо DataFrame для вызова Exception
    result = get_top_transactions(None)

    assert result is None
    mock_logger.error.assert_called()


@pytest.mark.parametrize("status_filter, expected_count", [
    ("OK", 3),  # В sample_transactions_df 3 расхода со статусом OK
    ("FAILED", 0)  # Функция жестко фильтрует по "OK", другие не пройдут
])
def test_get_top_transactions_filtering(sample_transactions_df, status_filter, expected_count):
    """Параметризованный тест фильтрации по статусу"""
    # Изменим статус для теста фильтрации
    df = sample_transactions_df.copy()
    if status_filter == "FAILED":
        df["Статус"] = "FAILED"

    result = get_top_transactions(df)
    assert len(result) == (expected_count if status_filter == "OK" else 0)


@patch('src.utils.requests.get')
@patch('builtins.open', new_callable=mock_open)
@patch('src.utils.os.getenv')
def test_get_currency_rates_success(mock_env, mock_file, mock_get, mock_user_settings):
    """Тест успешного получения курсов валют через API"""
    # Настройка моков
    mock_env.return_value = "fake_api_key"
    mock_file.return_value.read.return_value = json.dumps(mock_user_settings)

    # Имитируем ответ от api.apilayer.com
    mock_response = MagicMock()
    mock_response.json.return_value = {"base": "USD", "rates": {"RUB": 80.0}}
    mock_get.return_value = mock_response

    result = get_currency_rates()

    assert len(result) == 2
    assert result[0] == {"currency": "USD", "rate": 80.0}
    assert mock_get.call_count == 2


@pytest.mark.parametrize("mock_data, expected_rate", [
    ({"Valute": {"USD": {"Value": 75.0}}}, 75.0),
    ({"Valute": {"USD": {"Value": 100.5}}}, 100.5),
])
@patch('src.utils.requests.get')
def test_get_usd_rub_success(mock_get, mock_data, expected_rate):
    """Параметризованный тест получения курса USD"""
    mock_response = MagicMock()
    mock_response.json.return_value = mock_data
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    assert get_usd_rub() == expected_rate


@patch('src.utils.requests.get')
def test_get_usd_rub_exception(mock_get):
    """Тест обработки ошибки в get_usd_rub"""
    mock_get.side_effect = Exception("Connection error")

    result = get_usd_rub()
    assert result is None


@patch('src.utils.yf.Ticker')
@patch('src.utils.get_usd_rub')
@patch('builtins.open', new_callable=mock_open)
def test_get_stock_prices_success(mock_file, mock_usd, mock_yf, mock_user_settings):
    """Тест успешного получения цен акций с конвертацией в рубли"""
    # Настройка
    mock_file.return_value.read.return_value = json.dumps(mock_user_settings)
    mock_usd.return_value = 100.0  # Курс для простоты счета

    # Настройка мока для yfinance
    mock_ticker = MagicMock()
    mock_ticker.fast_info = {'last_price': 150.0}
    mock_yf.return_value = mock_ticker

    result = get_stock_prices()

    assert len(result) == 2
    # 150.0 (цена) * 100.0 (курс) = 15000.0
    assert result[0] == {"stock": "AAPL", "price": 15000.0}
    assert result[1] == {"stock": "TSLA", "price": 15000.0}


@patch('src.utils.utils_logger')
@patch('builtins.open', side_effect=FileNotFoundError)
def test_get_stock_prices_file_error(mock_open_file, mock_logger):
    """Тест ошибки при отсутствии файла настроек"""
    result = get_stock_prices()

    assert result is None
    mock_logger.error.assert_called()
