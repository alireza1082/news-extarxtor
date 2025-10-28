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


def get_tgju_news():
    server_name = "tgju"

    url = "https://www.tgju.org/news"
    base_url = "https://www.tgju.org"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/128.0.0.0 Safari/537.36"
        )
    }
    try:
        resp = requests.get(url.rstrip(), headers=headers)

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
            print(f"news on {server_name} site is: ")
            news_items = []
            for item in soup.find_all("div", {"class": "news-article-block"}):
                title_tag = item.select_one("h3.news-article-title a")
                title = title_tag.get_text(strip=True) if title_tag else None
                link = urljoin(base_url, title_tag["href"]) if title_tag else None

                category_tags = item.select("a.news-article-tag")
                category = category_tags[0].get_text(strip=True) if category_tags else None
                tags = [t.get_text(strip=True) for t in category_tags[1:]] if len(category_tags) > 1 else []

                desc_tag = item.select_one("span.news-article-description")
                description = desc_tag.get_text(strip=True) if desc_tag else None

                img_tag = item.select_one("figure a img")
                image_url = img_tag["src"] if img_tag else None

                time_tag = item.select_one("time.news-article-text-sub")
                publish_datetime = time_tag.get("datetime") if time_tag else None  # زمان میلادی
                publish_text = time_tag.get_text(strip=True) if time_tag else None  # زمان شمسی متنی

                news_items.append({
                    "title": title,
                    "link": link,
                    "category": category,
                    "tags": tags,
                    "summary": description,
                    "image": image_url,
                    "publish_datetime": publish_datetime,
                    "publish_text": publish_text
                })
            print(len(news_items))
            return news_items
        else:
            return None
    except Exception as ex:
        print("an error occurred in checking " + server_name)
        print(ex)
        return None


def fetch_eghtesadonline_section(sec_id=266):
    base_url = "https://www.eghtesadonline.com"
    # url = f"{base_url}/fa/archive/section?sec_id={sec_id}"
    url = f"{base_url}/fa/services/13"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/128.0.0.0 Safari/537.36"
        )
    }

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    news_items = []
    for article in soup.select("section.ListNewsSection article.newsList"):
        title_tag = article.select_one("h3.title a")
        title = title_tag.get_text(strip=True) if title_tag else None
        link = urljoin(base_url, title_tag["href"]) if title_tag and title_tag.get("href") else None

        summary_tag = article.select_one("p.summery")
        summary = summary_tag.get_text(strip=True) if summary_tag else None

        img_tag = article.select_one("a.picLink img")
        image = urljoin(base_url, img_tag["src"]) if img_tag and img_tag.get("src") else None

        date_tag = article.select_one("span.date")
        date = date_tag.get_text(strip=True) if date_tag else None
        # must use requests_html instead requests

        news_items.append({
            "title": title,
            "link": link,
            "summary": summary,
            "image": image
        })

    return news_items


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
