# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SRC_ROOT = os.path.dirname(os.path.abspath(__file__))   # application_top
    APP_ROOT = os.path.join(SRC_ROOT, 'app')
    APP_UPLOADS = os.path.join(APP_ROOT, 'uploads')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    BOOTSTRAP_SERVE_LOCAL = True
    LANGUAGES = {
        'en': 'English',
        'es': 'Español'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 's3cr3t'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 's3cr3t'
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 's3cr3t'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-prod.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

