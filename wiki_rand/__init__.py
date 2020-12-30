"""Wiki App package initializer"""
import flask

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)

# Read settings from config module (wiki_rand/config.py)
app.config.from_object('wiki_rand.config')

# Overlay settings read from file specified by environment variable.  This is
# useful for using different on development and production machines.
# Reference: http://flask.pocoo.org/docs/config
app.config.from_envvar('WIKI_RAND_SETTINGS', silent=True)

# Tell our app about views and model.  This is close to a
# circular import, but flask was designed that way.
# (Reference http://flask.pocoo.org/docs/patterns/packages/)  We're
# going to tell pylint and pycodestyle to ignore this coding style violation.
import wiki_rand.views
