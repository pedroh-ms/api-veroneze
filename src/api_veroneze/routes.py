from flask import current_app, Blueprint, render_template, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from .database import *
import os
import json


bp = Blueprint('testedb', __name__, template_folder='templates')


def resourceUpdate(resource, resourceupdate, columns, resourcename):
    
    resourceupdated = False

    resourceid = resource.id
    
    for k, v in resourceupdate.items():

        try:
            
            if type(v) == dict:
                for r in v:
                    setattr(resource, columns[k][r], resourceupdate[k][r])
            elif type(v) == list:
                setattr(resource, columns[k], ','.join(resourceupdate[k]))
            else:
                setattr(resource, columns[k], resourceupdate[k])

            resourceupdated = True

        except KeyError:
            pass

    if resourceupdated == False:
        
        return {'error' : {'status' : 400,
                           'message' : 'The resouce' + resourcename + ' of id ' + str(resourceid) + ' couldn\'t be changed due to lack of valid parameters!'}}, 400
    
    db.session.commit()

    return {'ok' : {'status' : 200,
                    'message' : 'The resouce ' + resourcename + ' of id ' + str(resourceid) + ' has its data changed!'}}, 200


@bp.route('/login')
def login():
    
    username = request.args.get('user', None)
    password = request.args.get('password', None)
    if username != 'admin' or password != 'admin':
        return {'error' : {'status' : 401,
                           'message' : 'Bad username or password'}}, 401

    access_token = create_access_token(identity=username)
    return jsonify({'ok' : {'status' : 200,
                            'message' : 'Token was generated!',
                            'access_token' : access_token}}), 200


# seleciona todo o banco de dados e devolve o json do mesmo
@bp.route('/database')
@jwt_required()
def getDataBase():

    return {'alunos' : [{'id' : i.id,
                         'nome_completo' : i.nome_completo,
                         'email' : i.email,
                         'endereço' : {'rua' : i.endereco_rua,
                                       'numero' : i.endereco_numero,
                                       'cidade' : i.endereco_cidade},
                         'curso' : i.curso,
                         'disciplinas' : i.disciplinas.split(',')} for i in Aluno.query.all()],
            'cursos' : [{'id' : i.id,
                         'nome' : i.nome} for i in Curso.query.all()]}, 200


@bp.route('/aluno/<id>', methods=['GET', 'DELETE', 'PUT'])
@jwt_required()
def alunoGetDeleteUpdate(id):

    aluno = Aluno.query.filter_by(id=id).first()
    if aluno == None:
        return {'error' : {'status' : 404,
                           'message' : f'Aluno of id {id} not found!'}}, 404

    if request.method == 'GET':

        return {'id' : aluno.id,
                'nome_completo' : aluno.nome_completo,
                'email' : aluno.email,
                'endereço' : {'rua' : aluno.endereco_rua,
                              'numero' : aluno.endereco_numero,
                              'cidade' : aluno.endereco_cidade},
                'curso' : aluno.curso,
                'disciplinas' : aluno.disciplinas.split(',')}, 200

    elif request.method == 'DELETE':
        
        db.session.delete(aluno)
        db.session.commit()
        
        return {'ok' : {'status' : '200',
                        'message' : f'Aluno of id {aluno.id} deleted!'}}, 200

    elif request.method == 'PUT':

        columns = {'nome_completo' : 'nome_completo',
                   'email' : 'email',
                   'endereço' : {'rua' : 'endereco_rua',
                                 'numero' : 'endereco_numero',
                                 'cidade' : 'endereco_cidade'},
                   'curso' : 'curso',
                   'disciplinas' : 'disciplinas'}

        return resourceUpdate(aluno, request.get_json(), columns, 'Aluno')


# retorna os alunos por página
@bp.route('/aluno/page/<int:page_number>')
@jwt_required()
def alunoGetPage(page_number):

    alunos = Aluno.query.paginate(page_number, 10, False).items

    if alunos==[]:

        return {'error' : {'status' : 404,
                           'message' : 'Page not found!'}}

    return jsonify({'alunos' : [{'id' : i.id,
                                 'nome_completo' : i.nome_completo,
                                 'email' : i.email,
                                 'endereço' : {'rua' : i.endereco_rua,
                                               'numero' : i.endereco_numero,
                                               'cidade' : i.endereco_cidade},
                                 'curso' : i.curso,
                                 'disciplinas' : i.disciplinas.split(',')} for i in alunos]}), 200


# insere uma linha na tabela aluno
@bp.route('/aluno', methods = ['POST'])
@jwt_required()
def alunoInsert():

    if request.method == 'POST':

        aluno = request.get_json()

        try:

            db.session.add(Aluno(id=aluno['id'],
                                 nome_completo=aluno['nome_completo'],
                                 email=aluno['email'],
                                 endereco_rua=aluno['endereço']['rua'],
                                 endereco_numero=aluno['endereço']['numero'],
                                 endereco_cidade=aluno['endereço']['cidade'],
                                 curso=aluno['curso'],
                                 disciplinas=','.join(aluno['disciplinas'])))

        except KeyError:

            return {'error' : {'status' : 400,
                               'message' : 'The resource couldn\'t be inserted due to lack of valid parameters!'}}, 400
        
        try:
            
            db.session.commit()
            
        except exc.IntegrityError:

            return {'error' : {'status' : 400,
                               'message' : f'A resource Aluno of id={aluno["id"]} already exist in the database!'}}, 400

        return {'ok' : {'status' : 201,
                        'message' : f'Aluno inserted!'}}, 201

    
@bp.route('/curso/<id>', methods=['GET', 'DELETE', 'PUT'])
@jwt_required()
def cursoGetDeleteUpdate(id):

    curso = Curso.query.filter_by(id=id).first()
    
    if curso == None:
        return {'error' : {'status' : 404,
                           'message' : f'Curso of id {id} not found!'}}, 404
    
    if request.method == 'GET':

        return jsonify({'id' : curso.id,
                        'nome' : curso.nome}), 200

    if request.method == 'DELETE':

        db.session.delete(curso)
        db.session.commit()

        return {'ok' : {'status' : 200,
                        'message' : f'Curso of id {curso.id} deleted!'}}, 200

    if request.method == 'PUT':

        columns = {'id' : 'id',
                   'nome' : 'nome'}

        return resourceUpdate(curso, request.get_json(), columns, 'Curso')


@bp.route('/curso', methods=['POST'])
@jwt_required()
def cursoInsert():

    if request.method == 'POST':
        curso = request.get_json()

        try:
            
            db.session.add(Curso(id=curso['id'],
                                 nome=curso['nome']))

        except KeyError:

            return {'error' : {'status' : 400,
                               'message' : 'The resource couldn\'t be inserted due to lack of valid parameters!'}}, 400

        try:
    
            db.session.commit()

        except exc.IntegrityError:

            return {'error' : {'status' : 400,
                               'message' : f'A resource Curso of id={curso["id"]} already exist in the database!'}} 

        return {'ok' : {'status' : 201,
                        'message' : f'Curso inserted!'}}, 201
    
        
# reinicia o banco de dados
@bp.route('/restart')
def restartDataBase():

    db.drop_all()

    db.create_all()

    json_file = open('src/api_veroneze/db.json', 'r', encoding='utf-8')
    data = json.load(json_file)

    for i in data['cursos']:
       db.session.add(Curso(id=i['id'],
                            nome=i['nome']))

    for i in data['alunos']:
       db.session.add(Aluno(id=i['id'],
                            nome_completo=i['nome_completo'],
                            email=i['email'],
                            endereco_rua=i['endereço']['rua'],
                            endereco_numero=i['endereço']['numero'],
                            endereco_cidade=i['endereço']['cidade'],
                            curso=i['curso'],
                            disciplinas=','.join(i['disciplinas'])))

    db.session.commit()
    return {'ok' : {'status' : 200,
                    'message' : 'Database restarted!'}}, 200
