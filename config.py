##
# This file configures the microservice. 
# 
# This microservice uses dotenv (.env) files to get environmental variables.
# This is done to configure sensible parameters, like database connections, 
# application secret keys and the like. 
#
# In case the dotenv file does not exists, a warning is generated. 
#
##

import os 
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
env = os.path.join(basedir, '.env')
if os.path.exists(env):
    load_dotenv(env)
else:
    print('Warning: .env file not found')


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL_PROD')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL_DEV')


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL_TEST')


class ProdConfig(Config):
    pass

