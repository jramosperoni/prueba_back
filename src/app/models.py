# -*- coding: utf-8 -*-
import os
import logging
from datetime import datetime
from . import db


class Orchard(db.Model):
    __tablename__ = 'orchard'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    csg = db.Column(db.String(64), nullable=False)


class Especie(db.Model):
    __tablename__ = 'especies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)


class Variedad(db.Model):
    __tablename__ = 'variedades'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    plu = db.Column(db.Integer, nullable=False)

    especie_id = db.Column(db.Integer, db.ForeignKey('especies.id'),
                           nullable=False)
    especie = db.relationship("Especie")
    products = db.relationship("Product", back_populates="variedad")

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'plu': self.plu,
            'especie_id': self.especie_id,
        }



class Color(db.Model):
    __tablename__ = 'colores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)


class Calibre(db.Model):
    __tablename__ = 'calibres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    variedad_id = db.Column(db.Integer, db.ForeignKey('variedades.id'))
    color_id = db.Column(db.Integer, db.ForeignKey('colores.id'))
    calibre_id = db.Column(db.Integer, db.ForeignKey('calibres.id'))
    variedad = db.relationship("Variedad")
    color = db.relationship("Color")
    calibre = db.relationship("Calibre")


class Facility(db.Model):
    __tablename__ = 'facility'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    csp = db.Column(db.String(64), nullable=False)


class Packaging(db.Model):
    __tablename__ = 'packagings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    material = db.Column(db.String(64), nullable=False)


class ProductPackaging(db.Model):
    __tablename__ = 'product_packaging'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    peso_neto = db.Column(db.Float, nullable=False, default=0)
    peso_bruto = db.Column(db.Float, nullable=False, default=0)

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product = db.relationship('Product')

    packaging_id = db.Column(db.Integer, db.ForeignKey('packagings.id'))
    packaging = db.relationship('Packaging')

    orchard_id = db.Column(db.Integer, db.ForeignKey('orchard.id'))
    orchard = db.relationship('Orchard')


class PalletStatus:
    Pendiente = 1
    PorIngresar = 2
    Ingresado = 3
    EnManjoInterno = 4
    PorEgresar = 5
    Egresado = 6

    @classmethod
    def as_dict(cls):
        return {cls.Pendiente: "En espera",
                cls.PorIngresar: "Por Ingresar",
                cls.Ingresado: "Ingresado",
                cls.EnManjoInterno: "En Manejor Interno",
                cls.PorEgresar: "Por Egresar",
                cls.Egresado: "Egresado",
                }


class Pallet(db.Model):
    __tablename__ = 'pallets'
    id = db.Column(db.Integer, primary_key=True)
    productpackaging_id = db.Column(db.Integer,
                                    db.ForeignKey('product_packaging.id'))
    productpackaging = db.relationship('ProductPackaging')
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'))
    facility = db.relationship('Facility')
    folio = db.Column(db.String(10), nullable=False, unique=True, default="")
    status = db.Column(db.Integer, nullable=False,
                          default=PalletStatus.Pendiente)
    completed = db.Column(db.Boolean, nullable=False, default=True)
    unidades = db.Column(db.Integer, nullable=False, default=0)
    fecha_embalaje = db.Column(db.DateTime(), default=datetime.utcnow)
    fecha_ingreso = db.Column(db.DateTime(), nullable=True)
    fecha_egreso = db.Column(db.DateTime(), nullable=True)

    @classmethod
    def formatfolio(cls, csp, year, folio):
        return "{0:03d}{1:02d}{2:05d}".format(int(str(csp)[-3:]),
                                              int(str(year)[-2:]),
                                              int(str(folio)[-5:]))
