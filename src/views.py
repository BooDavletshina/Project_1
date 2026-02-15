import json
import os

from src.utils import get_greeting, read_transactions_excel, get_data_cards, get_top_transactions, get_currency_rates, \
    get_stock_prices


def generate_main_page_json():
    """Главная функция, которая генерирует JSON-ответа для страницы Главная"""
    # Приветствие в зависимости от времени суток
    greeting = get_greeting()

    # Преобразуем Excel-файл с данными о транзакциях в DF
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'operations.xlsx')
    df_transactions = read_transactions_excel(path)

    # Получаем информацию по картам
    cards = get_data_cards(df_transactions)

    # Получаем топ-5 транзакций по сумме платежа
    top_transactions = get_top_transactions(df_transactions)

    # Получаем курс валют
    currency_rates = get_currency_rates()

    # Получаем стоимость акций из S&P500
    stock_prices = get_stock_prices()

    # Формируем JSON-ответ для страницы Главная
    data = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }
    json_data = json.dumps(data, ensure_ascii=False)

    return json_data


if __name__ == "__main__":
    print(generate_main_page_json())
