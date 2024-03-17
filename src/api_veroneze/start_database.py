from sqlalchemy.inspection import inspect
from api_veroneze.models import *
from api_veroneze.app_bcrypt import app_bcrypt
import json

def start_database(app, db):

    with app.app_context():

        inspector = inspect(db.engine)

        if inspector.has_table('aluno'):
            Aluno.__table__.drop(db.engine)
        if inspector.has_table('curso'):
            Curso.__table__.drop(db.engine)
        if inspector.has_table('user'):
            User.__table__.drop(db.engine)

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
            
        db.session.add(User(
            name='admin',
            password=app_bcrypt.generate_password_hash('password').decode('utf-8', 'strict')
        ))

        db.session.commit()
        return {'ok' : {'status' : 200,
                        'message' : 'Database restarted!'}}, 200