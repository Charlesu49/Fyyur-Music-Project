import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL

# modify with your personal db details
username = ''
password = ''
dbname = ''


# do not change the below
SQLALCHEMY_DATABASE_URI = f'postgresql://{username}:{password}@127.0.0.1:5432/{dbname}'
