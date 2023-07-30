import time
import requests
import selectorlib
import smtplib
import ssl
import os
import sqlite3

# SQL Query examples (just for myself)
"INSERT INTO events VALUES ('Tigers', 'Tiger City', '2088.10.14')"
"SELECT* FROM events WHERE date='2088.10.15'"
"DELETE FROM events WHERE band='Tigers'"

URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \
                  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 \
                  Safari/537.36'}

connection = sqlite3.connect("data.db")

def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "patrykkonior4@gmail.com"
    password = "HERE GOES YOUR GMAIL PASSWORD"

    receiver = "patrykkonior4@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)


def store(extracted_data):
    row = extracted_data.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()


def read(extracted_data):
    row = extracted_data.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",
                   (band, city, date))
    rows = cursor.fetchall()
    return rows


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row:
                store(extracted)
                send_email(message="""\
                Subject: New event!
                Hey, new event was found!""")
        time.sleep(2)
