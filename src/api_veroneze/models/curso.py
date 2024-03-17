from api_veroneze.database import db
from typing import Dict


class Curso(db.Model):
    __tablename__ = 'curso'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), unique=True, nullable=False)
    alunos = db.relationship("Aluno")

    def to_view(self):
        return {
            'id': self.id,
            'nome': self.nome
        }

    @classmethod
    def to_model(cls, data):
        return cls(
            nome=data['nome']
        )

    def put(self, data):
        print(data)
        self.nome = data['nome']

    def patch(self, data: Dict):
        self.nome = data['nome'] if 'nome' in data.keys() else self.nome

    def __repr__(self):
        return f'<id {self.id}, nome {self.nome}>'



