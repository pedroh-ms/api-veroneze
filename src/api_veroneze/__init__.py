import os

from datetime import timedelta

from flask import Flask
from flasgger import Swagger
from .doc import doc


def make_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SWAGGER={'uiversion' : 3,
                 'openapi' : '3.0.0'},
        JWT_SECRET_KEY='super-secret',
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=15),
        JWT_ERROR_MESSAGE_KEY='message'
    )

    app.config['DATABASE'] = os.getenv('DATABASE')
    
    if app.config['DATABASE'] == 'postgresql':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:123admin@db/ProjetoVeroneze'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

    print(app.config['SQLALCHEMY_DATABASE_URI'])

    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    
    swagger = Swagger(app, template=doc)

    
    from .auth import jwt
    jwt.init_app(app)
    
    from .database import db
    db.init_app(app)

    from .app_bcrypt import app_bcrypt
    app_bcrypt.init_app(app)

    from .start_database import start_database
    start_database(app, db)

    # home
    @app.route('/')
    def home():
        return {
            'ok' : {
                'status' : 200,
                'message' : 'Test server for the Veroneze\'s project'
            }
        } 
    
    from .views import (
        aluno,
        curso,
        login
    )

    app.register_blueprint(aluno.bp)
    app.register_blueprint(curso.bp)
    app.register_blueprint(login.bp)

    
    return app
