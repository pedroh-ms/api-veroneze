from flask import jsonify
from flask_jwt_extended import JWTManager

jwt = JWTManager()

@jwt.expired_token_loader
def app_expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'error' : {'status' : 401,
                               'message' : 'Token has expired!'}}), 401


@jwt.invalid_token_loader
def app_invalid_token_callback(error_string):
    return jsonify({'error' : {'status' : 422,
                               'message' : error_string + '!'}}), 422

@jwt.unauthorized_loader
def app_unauthorized_callback(error_string):
    return jsonify({'error' : {'status' : 401,
                               'message' : error_string + '!'}}), 401


