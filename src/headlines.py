'''
Created on 16 Aug 2017

@author: T
'''
import feedparser
from flask import Flask

app = Flask(__name__)

BBC_FEED = 'http://feeds.bbci.co.uk/news/rss.xml'
BBC_FEED = 'http://rss.iol.io/iol/news'

@app.route('/')
def get_news():
    feed = feedparser.parse(BBC_FEED)
    first_article = feed['entries'][0]
    return """<html>
        <body>
            <h1> BBC Headlines </h1>
            <b>{0}</b> <br/>
            <i>{0}</i> <br/>
            <p>{2}</p> <br/>
        </body>
    </html>""".format(first_article.get("title"),
                      first_article.get("published"),
                      first_article.get("summary"))
            

if __name__ == '__main__':
    app.run(port=5000, debug=True)