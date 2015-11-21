import json
import base64
def auth(route, environ):
    auth = False
    if 'HTTP_AUTHORIZATION' in environ:
        if environ['HTTP_AUTHORIZATION'][:6] == 'Basic ':
            s = base64.b64decode(environ['HTTP_AUTHORIZATION'][6:]).split(':')
            if s[0] in route['auth'] and route['auth'][s[0]]['password'] == ":".join(s[1:]):
               auth = True
    if auth:
        if 'args' in route['auth'][s[0]]:
            for key, value in route['auth'][s[0]]['args'].iteritems():
                route['call_args'][key] = value
    else:
        route['response']['data'] = '401 Not Authorized'
        route['response']['code'] = '401 Not Authorized'
        route['response']['headers'].append(('WWW-Authenticate', 'Basic realm="pyjsonrouter"'))

def static_file(file):
    with open(file) as f:
        return f.read()
