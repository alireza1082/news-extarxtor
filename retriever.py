from werkzeug.exceptions import abort

import api.api_price as api
import database.redisCache as dB


def get_gold_price():
    redis = dB.connect()
    dB.increase_counter(redis, "gold")

    if dB.is_update_required(redis):
        print("DB update required!")
        price = get_gold_price_from_api()
        if price is not None:
            print("returned price: " + str(price))
            dB.update_last_price(redis, price)
            return price
        if (price is None) and dB.is_update_valid(redis):
            print("Api not responding and price is valid!!")
            return dB.get_last_price(redis)
        else:
            abort(404, description="Resource not found")
    else:
        print("update not required")
        return dB.get_last_price(redis)


def get_usd_price():
    redis = dB.connect()
    dB.increase_counter(redis, "usd")

    if dB.is_update_required_usd(redis):
        print("DB update required for usd!")
        price = api.get_usd_brs()
        if price is not None:
            print("returned price: " + str(price))
            dB.update_last_price_usd(redis, str(price))
            return price
        if price is None:
            print("Api brs not responding!!")
            return dB.get_last_price_usd(redis)
        else:
            abort(404, description="Resource not found")
    else:
        print("update not required")
        return dB.get_last_price_usd(redis)


def get_counter():
    redis = dB.connect()
    return dB.get_counter(redis)
