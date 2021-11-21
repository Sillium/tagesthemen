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

@app.route("/tagesthemen/json")
def json():
    result_dict = get_when["Tagesthemen"]
    return result_dict

@app.route("/tagesthemen/plain")
def plain_text():
    result_dict = get_when["Tagesthemen"]
    return result_dict["when"]

@app.route("/tagesthemen")
def index():
    result_dict = get_when["Tagesthemen"]
    answer = "Die Tagesthemen kommen heute um " + result_dict["when"] + " in der ARD."
    return render_template("index.html", when=answer, url=url)
