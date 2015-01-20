import datetime
import json
import logging
import pandas as pd
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
import requests
import time
from wsgiref.simple_server import make_server

@view_config(route_name='hello', renderer='json')
def hello_world(request):
    data = requests.get('https://nowkash.firebaseio.com/.json').json()['-Jg5JPZ6DavVthFpW-oD']
    logging.debug(data)
    return Response(json.dumps(data))

@view_config(route_name='hello.html')
def hello_html(request):
  data = requests.get(u'https://nowkash.firebaseio.com/.json').json()
  data = data['-Jg5JPZ6DavVthFpW-oD']

  ret = '''<!DOCTYPE html>
  <html>
  <body>
  <table>
  <tr><th>Time</th><th>Value</th></tr>'''
  for d in data:
    ret = ret + '<tr><td>{0}</td><td>{1}</td></tr>'.format(d['Index'], d['Value'])
  ret = ret + '</table>'
  ret = ret + '</body></html>'
  logging.debug(to_pandas(data))
  return Response(ret)

def to_pandas(data):
  for s in data:
    s['Index'] = datetime.datetime.fromtimestamp(time.mktime(time.strptime(s['Index'], '%Y-%m-%d')))
    s['Value'] = float(s['Value'])
  df = pd.Series([d['Value'] for d in data], [d['Index'] for d in data])
  logging.debug(df)
  return df

if __name__ == '__main__':
    logging.basicConfig(level=logging.FATAL)
    port = 8080

    config = Configurator()
    config.add_route('hello', '/hello')
    config.add_route('hello.html', '/hello.html')
    config.add_view(hello_world, route_name='hello')
    config.add_view(hello_html, route_name='hello.html')

    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', port, app)
    print 'Running on port {0}'.format(port)
    server.serve_forever()
