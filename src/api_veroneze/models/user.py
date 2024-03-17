from api_veroneze.database import db
from typing import Dict


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def to_view(self):
        return {
            'id': self.id,
            'name': self.name,
            'password': self.password
        }
    
    @classmethod
    def to_model(cls, data):
        return cls(
            name=data['name'],
            password=data['password']
        )
    
    def put(self, data):
        self.name = data['name']
        self.password = data['password']

    def patch(self, data: Dict):
        self.name = data['name'] if 'name' in data.keys() else self.name
        self.password = data['password'] if 'password' in data.keys() else self.password

    def __repr__(self):
        return f'<id {self.id}, name {self.name}, password {self.password}'