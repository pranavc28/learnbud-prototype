"""Learning app package init."""
import flask
import os
from flask_login import LoginManager

from learning.user import User

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)  # pylint: disable=invalid-name
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# Read settings from config module (learning/config.py)
# app.config.from_object('learning.config')

# Overlay settings read from a Python file whose path is set in the environment
# variable LEARNING_SETTINGS. Setting this environment variable is optional.
# Docs: http://flask.pocoo.org/docs/latest/config/
#
# EXAMPLE:
# $ export LEARNING_SETTINGS=secret_key_config.py
app.config.from_envvar('LEARNING_SETTINGS', silent=True)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = ""

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Tell our app about views and model.  This is dangerously close to a
# circular import, which is naughty, but Flask was designed that way.
# (Reference http://flask.pocoo.org/docs/patterns/packages/)  We're
# going to tell pylint and pycodestyle to ignore this coding style violation.
import learning.views  # noqa: E402  pylint: disable=wrong-import-position
#import learning.model  # noqa: E402  pylint: disable=wrong-import-position
