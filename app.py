import pytz
import datetime
from pytz import timezone
import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask import render_template

app = Flask(__name__)

base_url = "https://programm.ard.de/programm/sender?sender=28106&datum="

def get_when(search_term):
    tz = pytz.timezone('Europe/Berlin')
    today = str(datetime.datetime.now(tz).strftime("%d.%m.%Y"))
    url = base_url + today
    r = requests.get(url)
    soup = soup = BeautifulSoup(r.text, "html.parser")
    spans = soup.findAll("span")
    titles = []
    dates = []
    for span in spans:
        try:
            classes = span["class"]
            if "title" in classes:
                s = str(span.contents[0]).strip()
                if s:
                    titles.append(s)
            if "date" in classes:
                s = str(span.contents[0]).strip()
                if s:
                    dates.append(s)
        except KeyError:
            """Ignore the tag that doesn't have a class atribute"""
            pass
    program = dict(zip(titles, dates))
    return {
        "when": program[search_term],
        "searchTerm": search_term,
        "url": url
    }

@app.route("/json")
def json():
    return get_when("Tagesthemen")

@app.route("/plain")
def plain_text():
    return get_when("Tagesthemen")["when"]

@app.route("/")
def index():
    answer = "Die Tagesthemen kommen heute um " + get_when("Tagesthemen")["when"] + " in der ARD."
    response = render_template("index.html", when=answer, url=get_when("Tagesthemen")["url"])
    response.headers['Cache-Control'] = 'max-age=60'
    return 
