# models/usuarios.py

class Usuario:
    def __init__(self, id, username, password, es_admin=False):
        self.id = id
        self.username = username
        self.password = password
        self.es_admin = es_admin

    def __repr__(self):
        return f'<Usuario {self.username}>'
