from api_veroneze.database import db
from typing import Dict


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

    def to_view(self):
        return {
            'id' : self.id,
            'nome_completo' : self.nome_completo,
            'email' : self.email,
            'endereço' : {
                'rua' : self.endereco_rua,
                'numero' : self.endereco_numero,
                'cidade' : self.endereco_cidade
            },
            'curso' : self.curso,
            'disciplinas' : self.disciplinas.split(',')
        }

    @classmethod
    def to_model(cls, data):
        return cls(
            nome_completo=data['nome_completo'],
            email=data['email'],
            endereco_rua=data['endereço']['rua'],
            endereco_numero=data['endereço']['numero'],
            endereco_cidade=data['endereço']['cidade'],
            curso=data['curso'],
            disciplinas=','.join(data['disciplinas'])
        )

    def put(self, data):
        self.nome_completo = data['nome_completo']
        self.email = data['email']
        self.endereco_rua = data['endereço']['rua']
        self.endereco_numero = data['endereço']['numero']
        self.endereco_cidade = data['endereço']['cidade']
        self.curso = data['curso']
        self.disciplinas = ','.join(data['disciplinas'])

    def patch(self, data: Dict):
        self.nome_completo = data['nome_completo'] if 'nome_completo' in data.keys() else self.nome_completo
        self.email = data['email'] if 'email' in data.keys() else self.email
        self.endereco_rua = data['endereço']['rua'] if 'endereço' in data.keys() and 'rua' in data['endereço'].keys() else self.endereco_rua
        self.endereco_numero = data['endereço']['numero'] if 'endereço' in data.keys() and 'numero' in data['endereço'].keys() and data['endereço'].has_key('numero') else self.endereco_numero
        self.endereco_cidade = data['endereço']['cidade'] if 'endereço' in data.keys() and 'cidade' in data['endereço'].keys() else self.endereco_cidade
        self.curso = data['curso'] if 'curso' in data.keys() else self.curso
        self.disciplinas = ','.join(data['disciplinas']) if 'disciplinas' in data.keys() else self.disciplinas

    def __repr__(self):
        return f'<id {self.id}, nome_completo {self.nome_completo}, email {self.email}, endereco_rua {self.endereco_rua}, endereco_numero {self.endereco_numero}, endereco_cidade {self.endereco_cidade}, curso {self.curso}, disciplinas {self.disciplinas}>'
