'''
Created on 16 Aug 2017

@author: T
'''
import feedparser
from flask import Flask
from flask import render_template
from flask import request

import json
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
import urllib

app = Flask(__name__)

RSS_FEED = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'iol': 'http://rss.iol.io/iol/news',
            'cnn': 'http://rss.cnn.com/rss/edition.rss',
            'fox': 'http://feeds.foxnews.com/foxnews/latest'}
DEFAULTS = {'publication':'bbc',
            'city':'Plymouth,UK',
            'currency_from':'GBP',
            'currency_to':'USD'}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=b41a0fe07ab09297d1e681977197888a"
CURRENCY_URL="https://openexchangerates.org//api/latest.json?app_id=65b6487c1d6046cca1e3d446bed6e4e5"

@app.route('/')
def home():
    # news
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    # get weather
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    # get currency
    currency_from = request.args.get('currency_from')
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.args.get('currency_to')
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate = get_rate(currency_from, currency_to)    
    return render_template("home.html",
                           site=publication.upper(),
                           articles=articles,
                           weather=weather,
                           currency_from=currency_from,
                           currency_to=currency_to,
                           rate=rate)
                           
    
    
def get_news(query):
    if not query or query.lower() not in RSS_FEED:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEED[publication])
    return feed['entries']
    
def get_weather(query):
    query = urllib.parse.quote(query)
    url = WEATHER_URL.format(query)
    data = urlopen(url).read()
    parsed = json.loads(data.decode('utf-8'))
    weather = None
    if parsed.get("weather"):
        weather = {"description":
                   parsed["weather"][0]["description"],
                   "temperature":parsed["main"]["temp"],
                   "city":parsed["name"],
                   "country":parsed['sys']['country']}
    return weather

def get_rate(frm, to):
    all_currency=urlopen(CURRENCY_URL).read()
    all_currency = all_currency.decode('utf-8')
#    print((all_currency))
    parsed = json.loads(all_currency).get('rates') #
    frm_rate=parsed.get(frm.upper())
    to_rate=parsed.get(to.upper())
    return to_rate/frm_rate

if __name__ == '__main__':
    app.run(port=5000, debug=True)