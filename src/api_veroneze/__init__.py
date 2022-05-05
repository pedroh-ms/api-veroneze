import os

from flask import Flask
from flasgger import Swagger
from .doc import doc

def make_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SWAGGER={'uiversion' : 3,
                 'openapi' : '3.0.0'}
    )

    swagger = Swagger(app, template=doc)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .database import db
    db.init_app(app)

    # home
    @app.route('/')
    @app.route('/home')
    def home():
        
        return {'ok' : {'status' : 200,
                         'message' : 'Test server for the Veroneze\'s project'}} 

    from . import routes
    app.register_blueprint(routes.bp)

    return app
