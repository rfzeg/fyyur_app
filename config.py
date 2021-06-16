import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to a local postgresql database
SQLALCHEMY_DATABASE_URI = 'postgres://roberto@localhost:5432/fyyur_app_db'

# Silence warning 'FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead...'
SQLALCHEMY_TRACK_MODIFICATIONS = False