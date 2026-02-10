import datetime
import json
import os
import yfinance as yf

import requests
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

def read_transactions_excel(path):
    """Функция для считывания финансовых операций из Excel-файла"""
    try:
        excel_data = pd.read_excel(path)
        return excel_data
    except FileNotFoundError:
        return []


def get_greeting():
    """Функция, которая возвращает приветствие в зависимости от времени суток"""
    date = datetime.datetime.now()
    if 6 <= date.hour < 12:
        return "Доброе утро!"
    elif 12 <= date.hour < 16:
        return "Добрый день!"
    elif 16 <= date.hour < 22:
        return "Добрый вечер!"
    else:
        return "Доброй ночи!"


def get_data_cards(transactions: pd.DataFrame) -> list[dict]:
    """Функция, которая возвращает данные по каждой карте (последние 4 цифры карты;
     общая сумма расходов; кешбэк (1 рубль на каждые 100 рублей)."""
    df_transactions = transactions.copy()

    df_transactions["Номер карты"] = df_transactions["Номер карты"].str.replace("*", "", regex=False)

    filter_transactions = df_transactions[
        (df_transactions["Сумма операции"] < 0) &
        (df_transactions["Статус"] == "OK")
        ]
    grouped_transactions = filter_transactions.groupby("Номер карты").agg({"Сумма операции": "sum"}).abs()

    grouped_transactions["Кешбэк"] = round((grouped_transactions["Сумма операции"] / 100), 2)

    list_cards = grouped_transactions.reset_index().to_dict(orient='records')

    return list_cards


def get_top_transactions(transactions: pd.DataFrame) -> list[dict]:
    """Функция, которая возвращает топ-5 транзакций по сумме платежа"""
    df_transactions = transactions.copy()

    filter_transactions = df_transactions[
        (df_transactions["Сумма операции"] < 0) &
        (df_transactions["Статус"] == "OK")
        ]

    sort_transactions = filter_transactions.sort_values(by="Сумма операции").head()

    top_transactions = sort_transactions.loc[:, ["Дата платежа", "Сумма операции", "Категория", "Описание"]]

    top_transactions["Сумма операции"] = top_transactions["Сумма операции"].abs()

    list_top_transactions = top_transactions.to_dict(orient='records')

    return list_top_transactions


def get_currency_rates():
    """Функция для получения курса валют"""
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'user_settings.json')
    with open(path, encoding='utf-8') as file:
        data = json.load(file)

        user_currencies = data.get("user_currencies", [])

        url = "https://api.apilayer.com/exchangerates_data/latest"

        api_key = os.getenv("API_KEY")
        headers = {"apikey": api_key}

        currency_rates = []

        for currency in user_currencies:
            payload = {
                "base": currency,
                "symbols": "RUB"
            }
            response = requests.get(url, headers=headers, params=payload)
            result = response.json()
            currency_rates.append({"currency" : result["base"], "rate" : result["rates"]["RUB"]})

        return currency_rates


def get_usd_rub():
    """Функция, которая получает актуальный курс доллара к рублю через API ЦБ РФ"""

    url = 'https://www.cbr-xml-daily.ru/daily_json.js'

    try:
        response = requests.get(url)

        response.raise_for_status()

        data = response.json()

        return data['Valute']['USD']['Value']

    except Exception as e:
        print(f"Ошибка при получении курса: {e}")
        return None


def get_stock_prices():
    """Функция для получения стоимости акций"""
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'user_settings.json')
    with open(path, encoding='utf-8') as file:
        data = json.load(file)

        tickers = data.get("user_stocks", [])

        usd_rate = get_usd_rub()

        result = []

        for ticker_name in tickers:
            stock = yf.Ticker(ticker_name)

            price_usd = stock.fast_info['last_price']

            price_rub = round(price_usd * usd_rate, 2)

            result.append({
                "stock": ticker_name,
                "price": price_rub
            })

    return result


if __name__ == "__main__":
    excel = read_transactions_excel("C:\\Users\\Boo_D\\PycharmProjects\\Project_1\\data\\operations.xlsx")
    # print(get_greeting())
    # print(get_data_cards(excel))
    # print(get_top_transactions(excel))
    # print(get_currency_rates())
    print(get_stock_prices())
    # print(get_usd_rub())
