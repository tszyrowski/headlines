'''
Created on 16 Aug 2017

@author: T
'''
import feedparser
import datetime

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response

import json
from flask.templating import render_template
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
    publication = get_value_with_fallback("publication")
    articles = get_news(publication)
    # get weather
    city = get_value_with_fallback('city')
    weather = get_weather(city)
    # get currency
    currency_from = get_value_with_fallback('currency_from')
    currency_to = get_value_with_fallback('currency_to')
    rate, currencies = get_rate(currency_from, currency_to)    
    
    response =  make_response(render_template("home.html",
                           site=publication.upper(),
                           articles=articles,
                           weather=weather,
                           currency_from=currency_from,
                           currency_to=currency_to,
                           rate=rate,
                           currencies=sorted(currencies)))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response 
                           
    
    
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
    return (to_rate/frm_rate, parsed.keys())

def get_value_with_fallback(key):
    # function retrieving the cookies by key otherwise deafult value
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]
    

if __name__ == '__main__':
    app.run(port=5000, debug=True)