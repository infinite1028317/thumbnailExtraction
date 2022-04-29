from flask import Flask

from restapi import content_api


def create_app():
    app = Flask(__name__)
    app.register_blueprint(content_api, url_prefix='/api')

    return app
