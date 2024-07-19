from flask import render_template, make_response
from flask_restful import Resource
from models.perros import Perros
from db import db

class PerroController(Resource):
    def get(self):
        perros = Perros.query.all()
        return make_response(render_template("perros.html", perros=perros))
    