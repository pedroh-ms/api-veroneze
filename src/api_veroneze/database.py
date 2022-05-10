from flask_sqlalchemy import SQLAlchemy, inspect
from sqlalchemy import exc
import json


db = SQLAlchemy()


class Curso(db.Model):
    __tablename__ = 'curso'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), unique=True, nullable=False)
    alunos = db.relationship("Aluno")
        
    def __repr__(self):
        return f'<Id, {self.id}, Nome {self.nome}>'


class Aluno(db.Model):
    __tablename__ = 'aluno'
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    endereco_rua = db.Column(db.String(60), unique=False, nullable=False)
    endereco_numero = db.Column(db.String(60), unique=False, nullable=False)
    endereco_cidade = db.Column(db.String(60), unique=False, nullable=False)
    curso = db.Column(db.Integer,  db.ForeignKey('curso.id'), nullable=False)
    disciplinas = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return f'<Id {self.id}, Nome_completo {self.nome_completo}, Email {self.email}, Endereco_rua {self.endereco_rua}, Endereco_numero {self.endereco_numero}, Endereco_cidade {self.endereco_cidade}, Curso {self.curso}, Disciplinas {self.disciplinas}>'



def startDataBase(app, db):

    with app.app_context():
        
        inspector = inspect(db.engine)
    
        if inspector.has_table('aluno'):
            Aluno.__table__.drop(db.engine)
        if inspector.has_table('curso'):
            Curso.__table__.drop(db.engine)
    
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
