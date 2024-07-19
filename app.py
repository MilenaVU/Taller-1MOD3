from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Ch*col4t3.@localhost/TABLAS'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Cambia esto por una clave secreta segura

db = SQLAlchemy(app)

# Definición de las tablas SQLAlchemy
class Perro(db.Model):
    __tablename__ = 'perros'
    ID = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Raza = db.Column(db.String(100), nullable=False)
    Edad = db.Column(db.Integer, nullable=False)
    Peso = db.Column(db.Float, nullable=False)
    ID_CUIDADOR = db.Column(db.Integer, db.ForeignKey('cuidadores.id'), nullable=False)
    cuidador = db.relationship('Cuidador', backref='perros')

class Cuidador(db.Model):
    __tablename__ = 'cuidadores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    id_guarderia = db.Column(db.Integer, db.ForeignKey('guarderias.id'))

# Simulación de usuarios
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

# Ruta de inicio
@app.route('/')
def home():
    if 'username' in session:
        username = session['username']
        user = next((user for user in usuarios if user.username == username), None)
        if user:
            if user.es_admin:
                return redirect(url_for('admin'))
            return f'Bienvenido, {username}!'
    return redirect(url_for('login'))

# Ruta para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((user for user in usuarios if user.username == username), None)
        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            return redirect(url_for('home'))
        flash('Invalid credentials. Please try again.')
        return redirect(url_for('login'))
    return render_template('login.html')

# Ruta para administración
@app.route('/admin')
def admin():
    if 'username' in session:
        username = session['username']
        user = next((user for user in usuarios if user.username == username), None)
        if user and user.es_admin:
            perros = Perro.query.all()
            return render_template('admin.html', perros=perros)
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas en la base de datos
    app.run(debug=True)
