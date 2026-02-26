import os

import pandas as pd

from src.reports import spending_by_category, spending_by_weekday, spending_by_workday
from src.services import profitable_cashback_categories
from src.utils import get_usd_rub, get_stock_prices, get_currency_rates, get_top_transactions, get_data_cards, \
    get_greeting
from src.views import generate_main_page_json

base_dir = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(base_dir, "data", "operations.xlsx")

df = pd.read_excel(file_path)

# Вызов функций формирующих отчеты
print(spending_by_category(df, "Фастфуд","03.10.2021"))  # траты по заданной категории
print(spending_by_weekday(df, "03.10.2021"))  # средние траты в каждый из дней недели
print(spending_by_workday(df, "03.10.2021"))  # траты в рабочий и в выходной день

# Вызов функции для анализа выгодности категорий повышенного кешбэка.
print(profitable_cashback_categories(df, 2021, 11))

# Вызов вспомогательных функций, необходимых для работы функции страницы «Главная»
print(get_greeting())
print(get_data_cards(df))
print(get_top_transactions(df))
print(get_currency_rates())
print(get_stock_prices())
print(get_usd_rub())

# Вызов функции, которая генерирует JSON-ответа для страницы Главная
print(generate_main_page_json())
