from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc


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
