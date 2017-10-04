# project/server/__init__.py


import os

from flask import Flask
from flask_bootstrap import Bootstrap


app = Flask(
    __name__,
    template_folder='../client/templates',
    static_folder='../client/static'
)


app_settings = os.getenv('APP_SETTINGS', 'project.server.config.DevelopmentConfig')
app.config.from_object(app_settings)

bootstrap = Bootstrap(app)


from project.server.main.views import main_blueprint
app.register_blueprint(main_blueprint)
