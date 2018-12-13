from base64 import b64decode
import json
import os
from urllib.parse import parse_qsl, urlparse

import sqlite3
from flask import Flask, request, Response, abort

BEACON = b64decode('R0lGODlhAQABAIAAANvf7wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')

APP_DIR = os.path.dirname(__file__)
DATABASE_NAME = os.path.join(APP_DIR, 'analytics.db')

EXTERNAL_SCRIPT = """(function(){
    var d=document,i=new Image,e=encodeURIComponent;
    i.src='%s/getgif?url='+e(d.location.href)+'&ref='+e(d.referrer)+'&t='+e(d.title);
    })()""".replace('\n', '')
DOMAIN = 'http://127.0.0.1:5000'


app = Flask(__name__)
app.config.from_object(__name__)

class Database:

    def __init__(self):
        self.db = DATABASE_NAME

    def __enter__(self):
        self.connection = sqlite3.connect(self.db)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_value, trace):
        if not exc_type:
            self.connection.commit()
        self.cursor.close()
        self.connection.close()
"""
class PageVisit(Model):



class JSONField(TextField):
    def python_value(self, value):
        if value is not None:
            return json.loads(value)

    def db_value(self, value):
        if value is not None:
            return json.dumps(value)
"""

@app.route('/servjs', methods=['GET'])
def send_js():
    return Response(app.config['EXTERNAL_SCRIPT'] % (app.config['DOMAIN']),
        mimetype='text/javascript')

@app.route('/getgif')
def gift():
    if not request.args.get('url'):
        abort(404)

    parsed = urlparse(request.args['url'])
    params = dict(parse_qsl(parsed.query))
    print('Request!')
    print('Netloc: ', parsed.netloc)
    print('Path: ', parsed.path)
    print('Args "t" :', request.args.get('t') or '')
    print('Headers: ', request.headers.get('X-Forwarded-For', request.remote_addr))
    print('Ref: ', request.args.get('ref') or '')
    print(dict(request.headers), params)

    response = Response(app.config['BEACON'], mimetype='image/gif')
    response.headers['Cache-Control'] = 'private, no-cache'
    return response

@app.errorhandler(404)
def not_found(error):
    return Response('Endpoint not found.')


if __name__=='__main__':
    app.run(debug=True)