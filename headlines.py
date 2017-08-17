'''
Created on 16 Aug 2017

@author: T
'''
import feedparser
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

RSS_FEED = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'iol': 'http://rss.iol.io/iol/news',
            'cnn': 'http://rss.cnn.com/rss/edition.rss',
            'fox': 'http://feeds.foxnews.com/foxnews/latest'}

@app.route('/')
def get_news(publication='bbc'):
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEED:
        publication = "bbc"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEED[publication])
    return render_template("home.html",
                           site=publication.upper(),
                           articles=feed['entries'])

if __name__ == '__main__':
    app.run(port=5000, debug=True)