import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://3000:3000@localhost/3000'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    WTF_CSRF_ENABLED = True

class DevelopmentConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = True

class ProductionConfig(Config):
    WTF_CSRF_ENABLED = True
