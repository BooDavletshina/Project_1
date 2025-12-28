from unittest.mock import patch

import pandas as pd

from src.decorators import writing_as_json_file


def mock_function_df():
    return pd.DataFrame({"test": [1, 2, 3]})


def mock_function_series():
    return pd.Series([1, 2, 3], name="test")


def test_writing_as_json_file_dataframe():
    """Тест сохранения DataFrame."""
    with patch("pandas.core.generic.NDFrame.to_json") as mock_to_json:
        decorated = writing_as_json_file(mock_function_df)
        result = decorated()
        assert isinstance(result, pd.DataFrame)
        mock_to_json.assert_called_once()


def test_writing_as_json_file_series():
    """Тест сохранения Series."""
    with patch("pandas.core.generic.NDFrame.to_json") as mock_to_json:
        decorated = writing_as_json_file(mock_function_series)
        result = decorated()

        assert isinstance(result, pd.Series)
        mock_to_json.assert_called_once()


def test_writing_as_json_file_return_value():
    """Проверка, что декоратор не портит возвращаемое значение."""
    with patch("pandas.core.generic.NDFrame.to_json"):
        decorated = writing_as_json_file(mock_function_df)
        result = decorated()

        expected_df = pd.DataFrame({"test": [1, 2, 3]})
        pd.testing.assert_frame_equal(result, expected_df)
