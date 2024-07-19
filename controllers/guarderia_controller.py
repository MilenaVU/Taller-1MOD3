from flask import render_template, make_response
from flask_restful import Resource
from models.guarderias import Guarderias
from db import db

class GuarderiaController(Resource):
    def get(self):
        guarderias = Guarderias.query.all()
        return make_response(render_template("guarderias.html", guarderias=guarderias))
    
    def post(self):
        guarderia = Guarderias(nombre="Guarderia #4", direccion="Calle Guarderia #4", telefono="478")
        db.session.add(guarderia)
        db.session.commit()
        return "Guardería creada con éxito"