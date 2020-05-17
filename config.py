from pathlib import Path

DEBUG = False
TESTING = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
SECRET_KEY = 'acU7/<}Jr\(!m,JX'
SESSION_COOKIE_HTTPONLY = False
SESSION_TYPE = 'redis'
QUERY_MAX_RESULT_COUNT = 1000
STRIPE_URL = 'https://api.stripe.com'
STRIPE_KEY = 'sk_test_KGm6pfEhnrCPDV235bUMmUWV'
SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 465
SMTP_USERNAME = 'poussy.magnette@gmail.com'
SMTP_PASSWORD = 'fwudamcgudlkenjz'
BASE_URL = 'http://localhost:5000'
GOOGLE_CLIENT_ID = '588518739043-oe363kajcna7evu7m96f6rdikkhqmoee.apps.googleusercontent.com'
GOOGLE_APPLICATION_CREDENTIALS = str(Path.home() / 'dip-ops-6a5560cff052.json')
DARTS_URL = 'http://localhost:8080'
DARTS_USERNAME = 'darts'
DARTS_PASSWORD = 'no1ere4ever'
