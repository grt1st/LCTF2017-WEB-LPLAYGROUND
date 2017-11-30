from flask import Flask
from flask import request, render_template

from request_url import *

import http
import urllib
import urllib.error
import urllib.request

import logging

app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_world():
    url = request.args.get('url')

    try:
        if not url.startswith('http://') and not url.startswith('https://'):
            url = "http://%s" % url
        #print(url)
        if not check_box(url):
            return render_template('result.html', info="我觉得不行")
    except Exception as e:
        return render_template('result.html', info=e)

    try:
        info = urllib.request.urlopen(url, timeout=2).info()
        return render_template('result.html', info="我觉得可以")
    except urllib.error.URLError as e:
        info = e
    except http.client.BadStatusLine as e:
        info = "我觉得还ok"
    except Exception as e:
        info =  e

    return render_template('result.html', info=info)

    #return render_template('result.html', url=url, status_code=r.status_code, title=title, content=content)

@app.errorhandler(404)
def page_not_found(error):
    app.logger.info('')
    return "阿X真的很严格"

if __name__ == '__main__':
    
    app.run()