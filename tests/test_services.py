from src.services import profitable_cashback_categories


def test_profitable_cashback_categories(df_transactions_excel):
    """Тест проверяет, что функция корректно проводит анализ выгодности категорий повышенного кэшбэка."""
    result = profitable_cashback_categories(df_transactions_excel, 2021, 11)
    assert result.loc['Супермаркеты'] == 570.0
    assert result.loc['Аптеки'] == 175.0
    assert result.loc['Дом и ремонт'] == 52.0


def test_profitable_cashback_categories_not_transactions(df_transactions_excel):
    """Тест, что при отсутствии транзакций в выбранном периоде вернется пустой Дата-фрейм"""
    result = profitable_cashback_categories(df_transactions_excel, 2025, 11)
    assert result.empty
