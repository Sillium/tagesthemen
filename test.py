import pytz
import datetime
from pytz import timezone
import requests
from bs4 import BeautifulSoup

base_url = "https://www.fernsehserien.de/heute-journal/sendetermine/zdf"

def get_when(search_term):
    tz = pytz.timezone('Europe/Berlin')
    #today = str(datetime.datetime.now(tz).strftime("%d.%m.%Y"))
    url = base_url
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    
    firstrow = soup.find("a", attrs={"role": "rowgroup"})

    div = firstrow.find("div", attrs={"role": "row"})

    span = div.findAll("span", attrs={"role": "cell"})[1]

    a = span.get_text().strip().split(" ")
    b = (a[1]).rsplit(".", 1)
    c = (b[1]).split("–", 1)

    return {
        "weekday": a[0],
        "date": b[0],
        "start": c[0],
        "end": c[1],
        "url": url
    }

print(get_when("Tagesthemen"))