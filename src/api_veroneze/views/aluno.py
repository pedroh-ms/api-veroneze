from flask import Blueprint, request
from api_veroneze.database import db
from api_veroneze.models import *
from flask_jwt_extended import jwt_required
from sqlalchemy import exc
from typing import List


bp = Blueprint('aluno', __name__, template_folder='templates')


@bp.get('/aluno/page/<int:page_number>')
@bp.get('/aluno')
@jwt_required()
def index(page_number = None):
    if page_number is None:
        alunos: List[Aluno] = db.session.execute(db.select(Aluno)).scalars()
    else:
        per_page = request.args.get('per_page')
        alunos: List[Aluno] = db.paginate(db.select(Aluno), page=page_number, per_page=int(per_page) if per_page is not None else None, max_per_page=50)
        
    return { 
        'alunos': [ aluno.to_view() for aluno in alunos ] 
    }, 200

@bp.get('/aluno/<id>')
@jwt_required()
def get(id):
    aluno: Aluno = db.session.execute(db.select(Aluno).filter_by(id=id)).scalar()
    
    if aluno is None:
        return aluno_not_found(id)
    
    return aluno.to_view()

@bp.post('/aluno')
@jwt_required()
def post():
    try:
        aluno = Aluno.to_model(request.get_json())
    except KeyError:
        return {
            'error': {
                'status': 400,
                'message': 'The resource couldn\'t be inserted due to lack of valid parameters!'
            }
        }, 400
    
    db.session.add(aluno)

    try:
        db.session.commit()
    except exc.IntegrityError:
        return {
            'error': {
                'status': 400,
                'message': f'A resource Aluno of id { aluno.id } already exist in the database!'
            }
        }, 400
    
    return {
        'ok': {
            'status': 201,
            'message': f'Aluno inserted!'
        }
    }, 201

@bp.put('/aluno/<id>')
@jwt_required()
def put(id):
    aluno: Aluno = db.session.execute(db.select(Aluno).filter_by(id=id)).scalar()
    
    if aluno is None:
        return aluno_not_found(id)
    
    try:
        aluno.put(request.get_json())
    except KeyError:
        return {
            'error': {
                'status': 400,
                'message': f'The resource Aluno of id { aluno.id } couldn\'t be changed due to lack of valid parameters!'
            }
        }, 400
    
    db.session.commit()

    return {
        'ok': {
            'status': 200,
            'message': f'The resource Aluno of id { aluno.id } has its data changed!'
        }
    }, 200

@bp.patch('/aluno/<id>')
@jwt_required()
def patch(id):
    aluno: Aluno = db.session.execute(db.select(Aluno).filter_by(id=id)).scalar()

    if aluno is None:
        return aluno_not_found(id)
    
    aluno.patch(request.get_json())

    db.session.commit()

    return {
        'ok': {
            'status': 200,
            'message': f'The resouce Aluno of id { aluno.id } has its data changed!'
        }
    }, 200

@bp.delete('/aluno/<id>')
@jwt_required()
def delete(id):
    aluno: Aluno = db.session.execute(db.select(Aluno).filter_by(id=id)).scalar()

    if aluno is None:
        return aluno_not_found(id)
    
    db.session.delete(aluno)
    db.session.commit()

    return {
        'ok': {
            'status': '200',
            'message' : f'Aluno of id { aluno.id } deleted!'
        }
    }, 200

def aluno_not_found(id):
    return {
        'error': {
            'status':  404,
            'message': f'Aluno of id { id } not found!'
        }
    }, 404
