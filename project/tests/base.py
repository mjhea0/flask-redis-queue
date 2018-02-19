# project/server/tests/base.py


from flask_testing import TestCase

from project.server import create_app

app = create_app()


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('project.server.config.TestingConfig')
        return app

    def setUp(self):
        pass

    def tearDown(self):
        pass
