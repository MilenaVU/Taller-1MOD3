# models/usuarios.py

from werkzeug.security import generate_password_hash

class Usuario:
    def __init__(self, id, username, password, es_admin=False):
        self.id = id
        self.username = username
        self.password = password
        self.es_admin = es_admin

    def __repr__(self):
        return f'<Usuario {self.username}>'

usuarios = [
    Usuario(id=1, username='user1', password=generate_password_hash('password1', method='pbkdf2:sha256')),
    Usuario(id=2, username='user2', password=generate_password_hash('password2', method='pbkdf2:sha256')),
    Usuario(id=3, username='admin', password=generate_password_hash('adminpass', method='pbkdf2:sha256'), es_admin=True)
]
