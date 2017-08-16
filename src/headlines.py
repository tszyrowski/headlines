'''
Created on 16 Aug 2017

@author: T
'''
import feedparser
from flask import Flask

app = Flask(__name__)

RSS_FEED = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'iol': 'http://rss.iol.io/iol/news',
            'cnn': 'http://rss.cnn.com/rss/edition.rss',
            'fox': 'http://feeds.foxnews.com/foxnews/latest'}

@app.route('/')
@app.route('/bbc')
def bbc():
    return get_news('bbc')

@app.route('/cnn')
def cnn():
    return get_news('cnn')

def get_news(publication):
    feed = feedparser.parse(RSS_FEED[publication])
    first_article = feed['entries'][0]
    return """<html>
        <body>
            <h1> {3} Headlines </h1>
            <b>{0}</b> <br/>
            <i>{0}</i> <br/>
            <p>{2}</p> <br/>
        </body>
    </html>""".format(first_article.get("title"),
                      first_article.get("published"),
                      first_article.get("summary"),
                      publication.upper())
            

if __name__ == '__main__':
    app.run(port=5000, debug=True)