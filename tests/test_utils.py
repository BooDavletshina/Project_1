import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from datetime import datetime

from src.utils import read_transactions_excel, get_greeting


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