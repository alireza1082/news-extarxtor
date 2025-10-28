import api.api_retrieve_site as retrieve_site
import api.api_price as api_price

def test_ice():
    print(retrieve_site.get_tgju_news())

def test_egh():
    print(retrieve_site.fetch_eghtesadonline_section())

def test_gold_price():
    print(api_price.get_gold_brs())


if __name__ == "__main__":
    test_egh()
