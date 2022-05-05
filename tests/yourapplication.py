from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../src/api_veroneze/data.db'
db = SQLAlchemy(app)

class Curso(db.Model):
    __tablename__ = 'curso'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), unique=True, nullable=False)
    alunos = db.relationship("Aluno")
        
    def __repr__(self):
        return '<Nome %r>' % self.nome


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
        return '<Nome_completo %r>' % self.nome_completo
    
@app.route('/')
def index():
    return "<h1 style='color: red'>hello flask</h1>"

if __name__ == "__main":
    app.run()
