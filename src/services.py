import pandas as pd

from src.decorators import writing_as_json_file


@writing_as_json_file
def profitable_cashback_categories(data: pd.DataFrame, year: int, month: int) -> pd.DataFrame:
    """Функция для анализа выгодности категорий повышенного кэшбэка."""
    df_data = data.copy()

    df_data["Дата операции"] = pd.to_datetime(df_data["Дата операции"], dayfirst=True)

    df_data_filter = df_data[
        (df_data["Дата операции"].dt.year == year) &
        (df_data["Дата операции"].dt.month == month)
                             ]

    df_data_grouped = df_data_filter.groupby('Категория')['Кэшбэк'].sum()

    df_data_sort = df_data_grouped.sort_values(ascending=False)

    return df_data_sort


if __name__ == "__main__":
    excel_data_transactions = pd.read_excel("C:\\Users\\Boo_D\\PycharmProjects\\Project_1\\data\\operations.xlsx")
    print(profitable_cashback_categories(excel_data_transactions, 2021, 11))
