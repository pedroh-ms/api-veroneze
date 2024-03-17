from flask import Blueprint, request
from api_veroneze.database import *
from api_veroneze.models import *
from flask_jwt_extended import jwt_required
from sqlalchemy import exc
from typing import List


bp = Blueprint('curso', __name__, template_folder='templates')


@bp.get('/curso')
@jwt_required()
def index():
    cursos: List[Curso] = db.session.execute(db.select(Curso)).scalars()
    return {
        'cursos': [ curso.to_view() for curso in cursos]
    }, 200

@bp.get('/curso/<id>')
@jwt_required()
def get(id):
    curso: Curso = db.session.execute(db.select(Curso).filter_by(id=id)).scalar()

    if curso is None:
        return curso_not_found(id)
    
    return curso.to_view()

@bp.post('/curso')
@jwt_required()
def post():
    try:
        curso = Curso.to_model(request.get_json())
    except KeyError:
        return {
            'error': {
                'status': 400,
                'message': 'The resource couldn\'t be inserted due to lack of valid parameters!'
            }
        }, 400
    
    db.session.add(curso)

    try:
        db.session.commit()
    except exc.IntegrityError:
        return {
            'error': {
                'status': 400,
                'message': f'A resource Curso of id { curso.id } already exist in the database!'
            }
        }, 400
    
    return {
        'ok': {
            'status': 201,
            'message': f'Curso inserted!'
        }
    }, 201

@bp.put('/curso/<id>')
@jwt_required()
def put(id):
    curso: Curso = db.session.execute(db.select(Curso).filter_by(id=id)).scalar()

    if curso is None:
        return curso_not_found(id)
    
    try:
        curso.put(request.get_json())
    except KeyError:
        return {
            'error': {
                'status': 400,
                'message': f'The resource Curso of id { curso.id } couldn\'t be changed due to lack of valid parameters!'
            }
        }, 400
    
    db.session.commit()

    return {
        'ok': {
            'status': 200,
            'message': f'The resource Curso of id { curso.id } has its data changed!'
        }
    }, 200

@bp.patch('/curso/<id>')
@jwt_required()
def patch(id):
    curso: Curso = db.session.execute(db.select(Curso).filter_by(id=id)).scalar()

    if curso is None:
        return curso_not_found(id)
    
    curso.patch(request.get_json())

    db.session.commit()

    return {
        'ok': {
            'status': 200,
            'message': f'The resource Curso of id { curso.id } has its data changed!'
        }
    }, 200

@bp.delete('/curso/<id>')
@jwt_required()
def delete(id):
    curso: Curso = db.session.execute(db.select(Curso).filter_by(id=id)).scalar()

    if curso is None:
        return curso_not_found(id)
    
    db.session.delete(curso)
    db.session.commit()

    return {
        'ok': {
            'status': 200,
            'message': f'Curso of id { curso.id } deleted!'
        }
    }, 200

def curso_not_found(id):
    return {
        'error': {
            'status': 404,
            'message': f'Curso of id { id } not found'
        }
    }, 404