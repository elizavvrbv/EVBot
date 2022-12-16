from requests import get


def get_main_currencies():
    j = get(
        "https://www.cbr-xml-daily.ru/daily_json.js"
    )
    data = j.json()
    usd_name = data["Valute"]["USD"]["Name"]
    usd_value = round(data["Valute"]["USD"]["Value"] / int(data["Valute"]["USD"]["Nominal"]), 2)
    usd = f"Курс {usd_name} - {usd_value}"
    eur_name = data["Valute"]["EUR"]["Name"]
    eur_value = round(data["Valute"]["EUR"]["Value"] / int(data["Valute"]["EUR"]["Nominal"]), 2)
    eur = f"Курс {eur_name} - {eur_value}"
    cny_name = data["Valute"]["CNY"]["Name"]
    cny_value = round(data["Valute"]["CNY"]["Value"] / int(data["Valute"]["CNY"]["Nominal"]), 2)
    cny = f"Курс {cny_name} - {cny_value}"
    try_name = data["Valute"]["TRY"]["Name"]
    try_value = round(data["Valute"]["TRY"]["Value"] / int(data["Valute"]["TRY"]["Nominal"]), 2)
    try_ = f"Курс {try_name} - {try_value}"
    byn_name = data["Valute"]["BYN"]["Name"]
    byn_value = round(data["Valute"]["BYN"]["Value"] / int(data["Valute"]["BYN"]["Nominal"]), 2)
    byn = f"Курс {byn_name} - {byn_value}"
    return f"{usd} \n{eur} \n{cny} \n{try_} \n{byn}"
