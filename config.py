import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ph:r45se@localhost/ph_demo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    WTF_CSRF_ENABLED = True

class DevelopmentConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = True

class ProductionConfig(Config):
    WTF_CSRF_ENABLED = True
