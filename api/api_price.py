import requests

from config import config_api


def get_usd_brs():
    price = 0
    url = "https://BrsApi.ir/Api/Market/Gold_Currency_Pro.php"
    # one-api token
    brs_key = config_api.brs_api_token

    parameters = {
        'key': brs_key,
        'section': 'currency'
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/106.0.0.0",
        "Accept": "application/json, text/plain, */*"
    }

    response = requests.get(url, params=parameters, headers=headers)

    if response.status_code == 200:
        print("Successful brs request!")
    else:
        print(f"Error brs: {response.status_code}")
        return 0
    link = response.json()['currency']['free']

    for pr in link:
        if pr['symbol'] == 'USD':
            print(pr)
            price = pr['price']
    return int(price / 10)


def get_gold_brs():
    price_18k = 0
    url = "https://BrsApi.ir/Api/Market/Gold_Currency_Pro.php"
    # one-api token
    brs_key = config_api.brs_api_token

    parameters = {
        'key': brs_key,
        'section': 'gold'
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/106.0.0.0",
        "Accept": "application/json, text/plain, */*"
    }

    response = requests.get(url, params=parameters, headers=headers)

    if response.status_code == 200:
        print("Successful brs request!")
    else:
        print(f"Error brs: {response.status_code}")
        return 0
    print(response.text)
    link = response.json()['gold']['type']

    for pr in link:
        if pr['symbol'] == 'IR_GOLD_18K':
            print(pr)
            price_18k = pr['price']
        elif pr['symbol'] == 'IR_GOLD_24K':
            print(pr)
            price_24k = pr['price']
    return str(int(price_18k / 10))