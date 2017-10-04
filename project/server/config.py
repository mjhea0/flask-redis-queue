# project/server/config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration."""
    DEBUG = False
    WTF_CSRF_ENABLED = True
    REDIS_URL = 'redis://redis:6379/0'
    QUEUES = ['default']

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    WTF_CSRF_ENABLED = False


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
