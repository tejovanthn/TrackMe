from flask.ext.script import Manager
from flask import url_for
from app import app

manager = Manager(usage='Utilities and helpers')

@manager.command
def list_routes():
    '''Lists all the routes that the app uses.'''

    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = '[{0}]'.format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote('{:50s} {:20s} {}'.format(rule.endpoint,
                              methods, url))
        output.append(line)

    for line in sorted(output):
        print line


