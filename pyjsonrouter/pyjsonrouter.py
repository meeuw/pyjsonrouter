import json
import re
import urlparse
import utils
import types
import sys

def getfunc(call):
    s = call.split('.')
    mod = __import__(s.pop(0))
    while len(s) > 1:
        mod = getattr(mod, s.pop(0))
    return getattr(mod, s[-1])


def merge(dst, src):
    for key, value in src.iteritems():
        if type(value) == types.DictType:
           if key in dst:
               merge(dst[key], src[key])
           else:
               dst[key] = src[key]
        elif type(value) == types.UnicodeType:
            dst[key] = src[key]
        elif type(value) == types.ListType:
            if not key in dst:
                dst[key] = []
            dst[key] += src[key]
        else:
           print type(value)
           sys.exit()

def application(environ, start_response):
    with open('router.json') as f:
        router = json.loads(f.read())
    if not environ['REQUEST_METHOD'] in router:
        start_response('404 Not Found', [('Content-Type', 'text/txt')])
        return 'Not Found'
    for route in router[environ['REQUEST_METHOD']]:
        m = re.match(route['regex'], environ['PATH_INFO'])
        if m:
            # initialize route
            if not 'response' in route:
                route['response'] = {}
            if not 'code' in route['response']:
                route['response']['code'] = '200 OK'
            if not 'headers' in route['response']:
                route['response']['headers'] = [
                    ('Content-Type', 'text/html')
                ]
            if 'include' in route:
                for include in route['include']:
                    with open(include) as f:
                        merge(route, json.loads(f.read()))
            route['call_args'] = {}
            # apply post data
            body = ''
            try:
                length= int(environ.get('CONTENT_LENGTH', '0'))
            except ValueError:
                length= 0
            if length != 0:
                body = environ['wsgi.input'].read(length)
            for key, value in urlparse.parse_qs(body).iteritems():
                route['call_args'][key] = value[0]
            # apply regexp matches from URL
            for key, value in m.groupdict().iteritems():
                route['call_args'][key] = value
            # apply args
            if 'args' in route:
                for key, value in route['args'].iteritems():
                    route['call_args'][key] = value
            # apply middleware
            if 'middleware' in route:
                for middleware in route['middleware']:
                    func = getfunc(middleware)
                    func(route, environ)
            func = getfunc(route['call'])
            if 'data' in route['response']:
                ret = route['response']['data']
            else:
                ret = func(**route['call_args'])

            if 'serialize' in route:
                func = getfunc(route['serialize'])
                ret = func(ret)
            start_response(
                route['response']['code'],
                route['response']['headers']
            )
            return ret
    start_response('404 Not Found', [('Content-Type', 'text/txt')])
    return 'Not Found'
