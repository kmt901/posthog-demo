import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hogflix.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    WTF_CSRF_ENABLED = True
    PH_PROJECT_KEY = os.environ.get('PH_PROJECT_KEY', '')
    PH_HOST = os.environ.get('PH_HOST', 'https://us.i.posthog.com')

class DevelopmentConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = True

class ProductionConfig(Config):
    WTF_CSRF_ENABLED = True
