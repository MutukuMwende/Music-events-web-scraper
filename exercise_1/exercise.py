import time
import requests
import selectorlib
import os
from datetime import datetime


URL = "https://programmer100.pythonanywhere.com"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \
                  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 \
                  Safari/537.36'}


def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("ex_extract.yaml")
    value = extractor.extract(source)["temperature"]
    return value


def store(extracted_data):
    with open("data_ex.txt", "a") as file:
        now = datetime.now()
        date = now.strftime("%y-%m-%d-%H-%M-%S,")
        file.write(date + extracted_data + "\n")


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
        store(extracted)
        time.sleep(5)
