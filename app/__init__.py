from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

# Configuration
DEBUG = True,
SECRET_KEY = 'ssshhh it\'s a secret'
WTF_CSRF_SECRET_KEY = 'a random string'


# create app
app = Flask(__name__)
app.config.from_object(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# import statement at end to avoid circular reference; views module imports app
from app import views
