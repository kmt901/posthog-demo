import os
from dotenv import load_dotenv

# Load the environment variables from the .env file if exists
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hogflix.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    WTF_CSRF_ENABLED = True
    PH_PROJECT_KEY = os.getenv('PH_PROJECT_KEY', '')
    PH_HOST = os.getenv('PH_HOST', 'https://us.i.posthog.com')

class DevelopmentConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = True

class ProductionConfig(Config):
    WTF_CSRF_ENABLED = True
