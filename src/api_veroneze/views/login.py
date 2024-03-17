from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from api_veroneze.database import db
from api_veroneze.models import User
from api_veroneze.app_bcrypt import app_bcrypt


bp = Blueprint('login', __name__, template_folder='templates')


@bp.get('/login')
def get():
    username = request.args.get('user', None)
    password = request.args.get('password', None)

    if username is None or password is None:
        return {
            'error': {
                'status': 401,
                'message': 'Bad username or password'
            }
        }, 401 

    user = db.session.execute(db.select(User).filter_by(name=username)).scalar()

    if user is None or not app_bcrypt.check_password_hash(user.password, password):
        return {
            'error': {
                'status': 401,
                'message': 'Bad username or password'
            }
        }, 401
    
    access_token = create_access_token(identity=username)

    return {
        'ok': {
            'status': 200,
            'message': 'Token was generated!',
            'access_token': access_token
        }
    }, 200
    
