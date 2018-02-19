# project/server/tests/test__config.py


import unittest

from flask import current_app
from flask_testing import TestCase

from project.server import create_app

app = create_app()


class TestDevelopmentConfig(TestCase):

    def create_app(self):
        app.config.from_object('project.server.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertFalse(current_app.config['TESTING'])
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertTrue(app.config['WTF_CSRF_ENABLED'] is False)
        self.assertFalse(current_app is None)


class TestTestingConfig(TestCase):

    def create_app(self):
        app.config.from_object('project.server.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertTrue(app.config['WTF_CSRF_ENABLED'] is False)


if __name__ == '__main__':
    unittest.main()
