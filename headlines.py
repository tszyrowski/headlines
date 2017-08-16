'''
Created on 16 Aug 2017

@author: T
'''
import feedparser
from flask import Flask
from flask import render_template

app = Flask(__name__)

RSS_FEED = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'iol': 'http://rss.iol.io/iol/news',
            'cnn': 'http://rss.cnn.com/rss/edition.rss',
            'fox': 'http://feeds.foxnews.com/foxnews/latest'}

@app.route('/')
@app.route('/<publication>')    # path added in <> for URL
def get_news(publication='bbc'):
    feed = feedparser.parse(RSS_FEED[publication])
    first_article = feed['entries'][0]
    return render_template("home.html",
                           site=publication.upper(),
                           article=first_article)

if __name__ == '__main__':
    app.run(port=5000, debug=True)