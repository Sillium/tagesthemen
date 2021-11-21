import pytz
import datetime
from pytz import timezone
import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/tagesthemen")
def index():
    tz = pytz.timezone('Europe/Berlin')
    today = str(datetime.datetime.now(tz).strftime("%d.%m.%Y"))
    url = "https://programm.ard.de/programm/sender?sender=28106&datum=" + today
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
    when = "Die Tagesthemen kommen heute um " + program["Tagesthemen"] + " in der ARD."
    return render_template("index.html", when=when, url=url)
