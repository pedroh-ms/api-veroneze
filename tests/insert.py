import json
from yourapplication import db, Curso, Aluno

db.create_all()

json_file = open('db.json', 'r', encoding='utf-8')
data = json.load(json_file)

for i in data['cursos']:
    db.session.add(Curso(nome=i['nome']))

for i in data['alunos']:
    db.session.add(Aluno(nome_completo=i['nome_completo'],
                         email=i['email'],
                         endereco_rua=i['endereço']['rua'],
                         endereco_numero=i['endereço']['numero'],
                         endereco_cidade=i['endereço']['cidade'],
                         curso=i['curso'],
                         disciplinas=','.join(i['disciplinas'])))

db.session.commit()
