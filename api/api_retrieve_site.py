# coding= utf-8
from urllib.parse import urljoin

import cloudscraper
import requests
from bs4 import BeautifulSoup
from persiantools import digits


def get_tgju_price():
    server_name = "tgju"
    url = "https://www.tgju.org/profile/geram18"
    try:
        resp = requests.get(url.rstrip())
        # arrange file by html tags
        if resp.status_code == 404:
            print("server not responding")
            return "0"
        soup = BeautifulSoup(resp.text, 'html.parser').find("span", {"data-col": "info.last_trade.PDrCotVal"})
        if soup is None:
            print("page not downloaded beautiful or structure changed")
            return "0"
        version = soup.text
        new_version = ''.join((ch if ch in '0123456789' else '') for ch in version)
        if new_version is not None:
            rond = int(new_version[:-4])
            print("price on tgju site is: ", str(rond + 1))
            return str(rond + 1)
        else:
            return "0"
    except Exception as ex:
        print("an error occurred in checking " + server_name)
        print(ex)
        return "0"


def get_ice_news():
    server_name = "ice"
    url = "https://ice.ir/news/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/128.0.0.0 Safari/537.36"
        )
    }
    try:
        # resp = requests.get(url.rstrip(), headers=headers)
        scraper = cloudscraper.create_scraper(browser={
            'browser': 'chrome',
            'platform': 'windows',
            'mobile': False
        })

        resp = scraper.get(url, verify=False)
        resp.raise_for_status()
        # arrange file by html tags
        if resp.status_code == 404:
            print(f"server {server_name} not responding")
            return "0"
        soup = BeautifulSoup(resp.text, 'html.parser')
        if soup is None:
            print(f"page of {server_name} not downloaded beautiful")
            return "0"
        news = soup.text

        if news is not None:
            news_items = []
            print(f"news on {server_name} site is: ", news)
            for a in soup.select("div.news-list a"):  # این انتخابگر ممکنه تغییر کنه
                title = a.get_text(strip=True)
                href = a.get("href")
                if not href:
                    continue
                full_link = urljoin("base_url", href)
                news_items.append({
                    "title": title,
                    "link": full_link
                })
            return news_items
        else:
            return None
    except Exception as ex:
        print("an error occurred in checking " + server_name)
        print(ex)
        return None


def get_tala_price():
    url = "https://www.tala.ir/price/18k"
    server_name = "tala"
    try:
        resp = requests.get(url)
        if resp.status_code == 404:
            print("server not responding or structure changed")
            return "0"
        # arrange file by html tags
        soup = BeautifulSoup(resp.text, 'html.parser').find("h3", {"class": "bg-green-light"})
        # get version by text of before element
        version = soup.text
        version_en = digits.fa_to_en(version)
        # check version name if it has words and remove words
        new_version = ''.join((ch if ch in '0123456789' else '') for ch in version_en)
        rond = int(new_version[:-3])
        print("price on tala site is: ", str(rond + 1))
        return str(rond + 1)
    except Exception as ex:
        print("an error occurred in checking " + server_name)
        print(ex)
        return "0"
